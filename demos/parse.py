import os
import json
import importlib.util
import sys
import threading
import _thread
from pathlib import Path
from time import time
import re
from tqdm import tqdm
from collections import defaultdict
import multiprocessing
import math
from concurrent.futures import ThreadPoolExecutor


INPUT_DIR = ""
OUTPUT_DIR = ""


# Execution time limit (seconds)
TIME_LIMIT = 8.0

# Ensure output directory exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Define timeout exception
class TimeoutException(Exception):
    pass

def load_json_file(file_path):
    """Load and return data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return {}

def execute_prediction_code(prediction_code, file_index):
    """Dynamically execute Python code from prediction and return validation and test case generation functions."""
    module_name = f"temp_module_{file_index}_{time()}"  # Add timestamp to make unique
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    exec(prediction_code, module.__dict__)

    validate_func = getattr(module, "validate_all_inputs", None)
    if not validate_func:
        raise AttributeError("validate_all_inputs function not found")
        
    gen_funcs = {
        name: getattr(module, name)
        for name in dir(module)
        if name.startswith("gen_TC") and callable(getattr(module, name))
    }

    return validate_func, gen_funcs

# Thread-based timeout function
def run_with_timeout(func, *args, timeout_sec=TIME_LIMIT):
    """Execute a function with a timeout using thread."""
    result = [None]
    error = [None]
    elapsed = [0]
    
    def target():
        try:
            start_time = time()
            result[0] = func(*args)
            elapsed[0] = time() - start_time
        except Exception as e:
            error[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_sec)
    
    if thread.is_alive():
        # Thread is still running after timeout
        raise TimeoutException("Execution timed out")
    
    if error[0] is not None:
        raise error[0]
        
    return result[0], elapsed[0]

def extract_question_id(item_data):
    """Extract question_id from a JSON item."""
    if "gold" in item_data and "question_id" in item_data["gold"]:
        return item_data["gold"]["question_id"]
    return None

def extract_code_from_prediction(prediction):
    """Extract Python code from a prediction string."""
    if not prediction or not isinstance(prediction, str):
        return None
    
    code_start = prediction.find("```python")
    code_end = prediction.rfind("```")
    if code_start == -1 or code_end == -1:
        return None
    
    return prediction[code_start + 9:code_end].strip()

def process_test_case(gen_func, validate_func, output_path, item_lock):
    """Process a single test case generation function."""
    try:
        # Generate test case with timeout
        test_input, gen_time = run_with_timeout(gen_func, timeout_sec=TIME_LIMIT)
        
        # Validate test case with timeout
        validation_result, val_time = run_with_timeout(validate_func, test_input, timeout_sec=TIME_LIMIT)
        
        is_valid = validation_result[0] if isinstance(validation_result, tuple) else validation_result
        
        if is_valid:
            output_data = {"input": test_input}
            with item_lock:
                with open(output_path, 'a', encoding='utf-8') as output_file:
                    output_file.write(json.dumps(output_data) + "\n")
            return True
        return False
    except TimeoutException:
        return False
    except Exception as e:
        return False

def process_json_item(item_data, file_index, item_index, question_id, output_path, item_lock):
    """Process a single JSON item, validate test cases, write to output file, and return statistics."""
    total_test_cases = 0  # Total test cases
    saved_test_cases = 0  # Saved test cases

    prediction = item_data.get("prediction")
    prediction_code = extract_code_from_prediction(prediction)
    
    if not prediction_code:
        return total_test_cases, saved_test_cases

    try:
        validate_func, gen_funcs = execute_prediction_code(prediction_code, f"{file_index}_{item_index}")
        
        # Use ThreadPoolExecutor for concurrent test case generation
        with ThreadPoolExecutor(max_workers=min(8, len(gen_funcs))) as executor:
            futures = []
            
            for gen_func_name, gen_func in gen_funcs.items():
                total_test_cases += 1
                futures.append(executor.submit(
                    process_test_case, gen_func, validate_func, output_path, item_lock
                ))
            
            # Collect results
            for future in futures:
                if future.result():
                    saved_test_cases += 1

    except Exception as e:
        pass

    return total_test_cases, saved_test_cases

def process_chunk(chunk_data, file_index, chunk_index, file_name, output_dir):
    """Process a chunk of items from a JSON file."""
    chunk_total = 0
    chunk_saved = 0
    
    # Create a dictionary to store locks for each output file
    output_locks = defaultdict(threading.Lock)
    
    # Set up progress bar for items in this chunk
    chunk_progress = tqdm(
        chunk_data, 
        desc=f"File {file_name} - Chunk {chunk_index}",
        position=chunk_index % 10,  # Position the progress bars in a cycling manner
        leave=False
    )
    
    for item_index, (key, item) in enumerate(chunk_progress):
        question_id = extract_question_id(item)
        if not question_id:
            continue
            
        output_path = os.path.join(output_dir, f"{question_id}.jsonl")
        
        # Get the lock for this output file
        item_lock = output_locks[output_path]
        
        # Process the item
        total, saved = process_json_item(item, file_index, item_index, question_id, output_path, item_lock)
        chunk_total += total
        chunk_saved += saved
        
        # Update progress bar description with stats
        chunk_progress.set_description(
            f"File {file_name} - Chunk {chunk_index} (Total: {chunk_total}, Saved: {chunk_saved})"
        )
    
    # Print summary for this chunk
    print(f"Completed File {file_name} - Chunk {chunk_index}: Generated {chunk_total} test cases, Saved {chunk_saved}")
    
    return chunk_total, chunk_saved

def split_json_file(json_data, num_chunks):
    """Split a JSON file into chunks for processing."""
    items = list(json_data.items())
    chunk_size = math.ceil(len(items) / num_chunks)
    
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunks.append(items[i:i + chunk_size])
    
    return chunks

def worker(args):
    """Worker function to process a file chunk."""
    chunk, chunk_index, file_index, file_name, output_dir = args
    try:
        chunk_total, chunk_saved = process_chunk(chunk, file_index, chunk_index, file_name, output_dir)
        return chunk_total, chunk_saved
    except Exception as e:
        print(f"Error in worker processing chunk {chunk_index} of file {file_name}: {str(e)}")
        return 0, 0

def main():
    """Main function to process JSON files using improved chunking and multiprocessing."""
    # Filter for json files
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json')]

    if not json_files:
        print(f"No JSON files found in {INPUT_DIR}")
        return

    # Available CPU cores
    cpu_count = multiprocessing.cpu_count()
    
    # Create process pool with optimal number of processes
    num_processes = min(80, cpu_count)  # Set to 20 based on your output
    print(f"Starting processing with {num_processes} processes on {cpu_count} available CPU cores")
    
    # Prepare tasks for multiprocessing
    all_tasks = []
    
    for file_index, json_file in enumerate(json_files):
        input_path = os.path.join(INPUT_DIR, json_file)
        print(f"Preparing file {file_index+1}/{len(json_files)}: {json_file}")
        
        json_data = load_json_file(input_path)
        
        if not json_data:
            continue
        
        # Calculate number of chunks per file based on size
        file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
        num_chunks = max(100, min(16, int(file_size_mb / 10)))  # Adjust based on file size
        
        print(f"  - File size: {file_size_mb:.2f} MB, splitting into {num_chunks} chunks")
        
        # Split file into chunks
        chunks = split_json_file(json_data, num_chunks)
        
        # Add tasks for each chunk
        for chunk_idx, chunk in enumerate(chunks):
            print(f"  - Created chunk {chunk_idx+1}/{num_chunks} with {len(chunk)} items")
            all_tasks.append((chunk, chunk_idx, file_index, json_file, OUTPUT_DIR))
    
    print(f"Total chunks to process: {len(all_tasks)}")
    
    # Use a multiprocessing pool to process all chunks
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Execute tasks with progress tracking for overall progress
        results = list(tqdm(
            pool.imap_unordered(worker, all_tasks),
            total=len(all_tasks),
            desc="Overall progress",
            position=0
        ))

    # Clear progress bars
    print("\n" * 15)  # Add some newlines to clear progress bars
    
    # Aggregate statistics
    global_total_test_cases = 0
    global_saved_test_cases = 0
    for total, saved in results:
        global_total_test_cases += total
        global_saved_test_cases += saved

    # Print per-problem statistics
    problem_count = 0
    problem_cases = {}
    for file_path in os.listdir(OUTPUT_DIR):
        if file_path.endswith('.jsonl'):
            problem_id = file_path.replace('.jsonl', '')
            file_path = os.path.join(OUTPUT_DIR, file_path)
            
            # Count lines more efficiently
            with open(file_path, 'r', encoding='utf-8') as f:
                total_lines = sum(1 for _ in f)
                
            problem_cases[problem_id] = total_lines
            problem_count += 1
            print(f"Output for {problem_id} finalized at {file_path} with {total_lines} test cases")

    # Print global statistics
    retention_rate = (global_saved_test_cases / global_total_test_cases * 100) if global_total_test_cases > 0 else 0
    print(f"\nGlobal Statistics:")
    print(f"Total problems processed: {problem_count}")
    print(f"Total test cases generated: {global_total_test_cases}")
    print(f"Total test cases saved: {global_saved_test_cases}")
    print(f"Retention rate: {retention_rate:.2f}%")

if __name__ == "__main__":
    main()