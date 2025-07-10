# SAGA: Strategic Adversarial & Constraint-differential Generative workflow for Test Case Generation

[![arXiv](https://img.shields.io/badge/arXiv-2507.06920-b31b1b.svg)](https://arxiv.org/abs/2507.06920)
[![Hugging Face - CodeCompass](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-opencompass/CodeCompass-blue)](https://huggingface.co/datasets/opencompass/CodeCompass)
[![Hugging Face - CodeForce_SAGA](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-opencompass/CodeForce_SAGA-orange)](https://huggingface.co/datasets/opencompass/CodeForce_SAGA)

This repository is the official implementation and supplementary material for the research paper, **"Rethinking Verification for LLM Code Generation: From Generation to Testing."** This work is a proud contribution from the [OpenCompass](https://github.com/open-compass/opencompass) team to advance the robust evaluation of large language models.

## 🚀 Introduction to SAGA

Current benchmarks for evaluating Large Language Model code generation often rely on a limited or homogeneous set of test cases. This can lead to inflated performance metrics and hinder the development of truly robust and reliable models.

To address these critical shortcomings, we introduce **SAGA (Strategic Adversarial & Constraint-differential Generative workflow)**, a novel human-LLM collaborative framework for advanced Test Case Generation (TCG). SAGA systematically integrates deep human programming expertise with the reasoning capabilities of LLMs to produce high-quality, diverse, and discriminative test suites. It achieves this through a dual-pronged analytical approach:

*   **Multidimensional Analysis:** Leveraging profound insights from correct human solutions to engineer challenging test scenarios.
*   **Differential Analysis:** Identifying subtle error patterns by analyzing incorrect human submissions against their corrected versions.

The core mission of SAGA is to significantly enhance the verification of LLM-generated code by maximizing both individual test case potency and overall test suite diversity.

## 🌟 Key Assets

This project provides several key assets to support full reproducibility and further research.

### 📦 Datasets on Hugging Face

We release two major datasets built with the SAGA framework:

#### 🔹 CodeCompass Benchmark
- **URL:** [https://huggingface.co/datasets/opencompass/CodeCompass](https://huggingface.co/datasets/opencompass/CodeCompass)
- **Configuration Name:** `codecompass_v0`
- A high-quality **evaluation benchmark** containing rigorous and diverse verifiers for all problems in TCGBench-Lite, designed for evaluating LLM code generation systems.

#### 🔸 CodeForce_SAGA Training Set
- **URL:** [https://huggingface.co/datasets/opencompass/CodeForce_SAGA](https://huggingface.co/datasets/opencompass/CodeForce_SAGA)
- **Configuration Name:** `default`
- A large-scale **training dataset** constructed using the SAGA framework. It is built from competitive programming problems and enriched via SAGA to produce fine-grained test cases for training code intelligence models.

### 📁 Local Assets in this Repository

*   **TCGBench-Lite Problem Set:**
    - Problem descriptions for the 270 problems used in our experiments.
    - Located at: `data/tcgbenc_lite_problems.jsonl` (demo included)

*   **SAGA Prompt Templates:**
    - Prompt templates for both Multidimensional and Differential Analysis.
    - Located at: `prompts/`

*   **SAGA-Generated Test Case Demo:**
    - A demo Python script showcasing a generated test case.
    - Located at: `demos/parse.py`

## 🛠️ Integration with OpenCompass (Coming Soon)

The **CodeCompass Benchmark** will soon be integrated into the [**OpenCompass**](https://github.com/open-compass/opencompass) evaluation ecosystem, enabling plug-and-play benchmarking of LLMs in code generation tasks.

## 📚 Citation

If you find our work useful, please consider citing:

```bibtex
@misc{ma2025rethinkingverificationllmcode,
      title={Rethinking Verification for LLM Code Generation: From Generation to Testing}, 
      author={Zihan Ma and Taolin Zhang and Maosong Cao and Wenwei Zhang and Minnan Luo and Songyang Zhang and Kai Chen},
      year={2025},
      eprint={2507.06920},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2507.06920}, 
}
