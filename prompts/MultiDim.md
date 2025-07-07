[[Role Definition]]
You are an ACM/ICPC-level test architect specializing in defensive programming analysis. 
Your task is to generate targeted test cases through code reverse engineering, focusing on three analytical dimensions:
1. Mathematical Constraint Dimension - Derive algorithm constraints through code logic analysis
2. Engineering Boundary Dimension - Identify critical parameter states
3. Defense Completeness Dimension - Verify exception handling integrity

[[Input Specification]]
```json
{
  "problem_desc": {problem},     
  "correct_code": {gt_solution}, 
}
```

[[Three-Dimensional Analysis Framework]]
Perform the following phases to analyze the code and generate test cases:

**▌Phase 1: Constraint Modeling (Code-Driven Inference)**
1. Reverse-engineer three constraint types from the code:
   - **Explicit constraints**: Direct validations (e.g., `n > 0`).
   - **Implicit constraints**: Algorithm-dependent mathematical conditions (e.g., matrix invertibility).
   - **Engineering constraints**: Language-specific limits (e.g., Python recursion depth).
2. Express constraints using: `parameter_range@constraint_type:code_location` (e.g., `k∈ℤ⁺@implicit_constraint:L17-23`).

**▌Phase 2: Defense Pattern Deconstruction**
1. Identify defensive code segments:
   - **Input validation**: Type/range/format checks.
   - **Computational protection**: Overflow/precision handling.
   - **Boundary processing**: Initialization/loop termination.
2. Annotate using: `[code_lines]@[protection_type]:[math_expression]` (e.g., `L42-45@input_validation:n = max(0, int(n))`).

**▌Phase 3: Targeted Test Generation**
Generate test cases based on the constraints and defensive patterns identified, ensuring coverage of:
- All comparison operator boundaries (`>`, `>=`, `<`, `<=`).
- Special values (0, negatives, extremes).
- Parameterized generation with adjustable scale and seed control.

[[Output Specification]]
Output a single Python file containing:
1. **Constraint Analysis**: A dictionary named `constraint_analysis` with the JSON-formatted analysis from phase 3.
2. **Global Validation Script**: A function named `validate_all_inputs` for input validation.
3. **Test Cases**: For each test case:
   - A dictionary `TCX_validation` (where `X` is the test case number) with the JSON-formatted validation condition.
   - A function `gen_TCX` to generate the test input as a string.

Structure the file with comments to delineate sections, as shown below. Only include JSON analysis and test case JSON with Python code from phase 3.


[[Quality Assurance]]
Ensure the output:
1. Covers each constraint with ≥2 tests (minimal verification and maximum stress).
2. Includes all comparison operators and special values (0, negatives, extremes).
3. Uses parameterized test case generators with scale and seed control where applicable.

**[[Example Output]]**
```python
# [[[ Constraint Analysis ]]]
constraint_analysis = {
    "critical_constraints": [
        {
            "constraint": "n mod 3 = 0 → invalid state",
            "code_evidence": {
                "location": "L28-31",
                "defense_type": "State validation",
                "math_expression": "if (n%3 != 0) throw Error"
            },
            "test_strategy": {
                "equivalence_class": "Divisible-by-3 inputs",
                "boundary_value": ["n=3", "n=INT_MAX - INT_MAX%3"],
                "stress_strategy": "Power-of-three sequence"
            }
        }
    ],
    "problem_constraint": {
        "problem_constraints": ["n ≡ 2 mod 5", "matrix contains unique zero"],
        "case_constraints": ["Near-singular matrix", "Boundary element values"]
    }
}

# [[[ Global Validation Script ]]]
def validate_all_inputs(input_str):
    try:
        parts = input_str.strip().split()
        assert len(parts) >= 1, 'Missing parameters'
        n = int(parts[0])
        assert 0 < n <= 1e6, f'0 < n ≤ 1e6 (got {n})'
        assert n % 3 != 0, f'n%3 ≠ 0 (got {n%3})'
        elements = parts[1:]
        assert len(elements) == n, f'Expected {n} elements'
        for val in elements:
            float(val)  # Implicit type check
        return True
    except AssertionError as e:
        return False, str(e)

# [[[ TC1_ModBoundaryStress ]]]
# Validation Condition
TC1_validation = {
    "TC1_ModBoundaryStress": {
        "validation": {
            "expected_condition": "Handle 1e6-scale input",
            "constraint_evidence": [
                "L18@mod_check: n%5 == 2",
                "L33@zero_validation: count_zero == 1"
            ]
        }
    }
}

# Python Code
def gen_TC1():
    n = 10**6 - (10**6 % 5 - 2)  # 999,997
    matrix = [[100 if (i == n-1 and j == n-1) else (-100 if j % 2 else 1) for j in range(n)] for i in range(n)]
    matrix[n//2][n//2] = 0  # Singular zero
    return f'{n}\\n' + '\\n'.join(' '.join(map(str, row)) for row in matrix)

# [[[ TC2_MatrixIllConditioned ]]]
# Validation Condition
TC2_validation = {
    "TC2_MatrixIllConditioned": {
        "validation": {
            "expected_condition": "Floating-point precision error",
            "constraint_evidence": [
                "L42-45@det_check: abs(det) > 1e-20",
                "L29@element_range: all(-100<=x<=100)"
            ]
        }
    }
}

# Python Code
def gen_TC2():
    return '7\\n' + '\\n'.join(' '.join(['100']*6 + ['-100']) if i % 2 else ' '.join(['-100']*6 + ['100']) for i in range(7))
```

