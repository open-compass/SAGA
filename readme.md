# SAGA: Strategic Adversarial & Constraint-differential Generative workflow for Test Case Generation

[![arXiv](https://img.shields.io/badge/arXiv-2507.06920-b31b1b.svg)](https://arxiv.org/abs/2507.06920)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-opencompass/CodeCompass-blue)](https://huggingface.co/datasets/opencompass/CodeCompass)

This repository is the official implementation and supplementary material for the research paper, **"Rethinking Verification for LLM Code Generation: From Generation to Testing."** This work is a proud contribution from the [OpenCompass](https://github.com/open-compass/opencompass) team to advance the robust evaluation of large language models.

## 🚀 Introduction to SAGA

Current benchmarks for evaluating Large Language Model code generation often rely on a limited or homogeneous set of test cases. This can lead to inflated performance metrics and hinder the development of truly robust and reliable models.

To address these critical shortcomings, we introduce **SAGA (Strategic Adversarial & Constraint-differential Generative workflow)**, a novel human-LLM collaborative framework for advanced Test Case Generation (TCG). SAGA systematically integrates deep human programming expertise with the reasoning capabilities of LLMs to produce high-quality, diverse, and discriminative test suites. It achieves this through a dual-pronged analytical approach:

*   **Multidimensional Analysis:** Leveraging profound insights from correct human solutions to engineer challenging test scenarios.
*   **Differential Analysis:** Identifying subtle error patterns by analyzing incorrect human submissions against their corrected versions.

The core mission of SAGA is to significantly enhance the verification of LLM-generated code by maximizing both individual test case potency and overall test suite diversity.

## 🌟 Key Assets

This project provides several key assets to support full reproducibility and further research.

### The Unified CodeCompass Dataset on Hugging Face

Our primary contribution is a unified dataset hosted on Hugging Face, containing both the evaluation benchmark and the training data generated via the SAGA framework.

➡️ **[Access the dataset at `opencompass/CodeCompass`](https://huggingface.co/datasets/opencompass/CodeCompass)** ⬅️

This dataset has two main configurations:

1.  **The CodeCompass Benchmark (`name="codecompass_v0"`)**
    *   This is the high-quality **evaluation benchmark** generated using the SAGA framework. It contains a comprehensive collection of verifiers for all problems in TCGBench-Lite, designed for rigorously testing LLM code generation.
2.  **The CodeForce-SAGA Training Set (`name="codeforce_saga"`)**
    *   This is the large-scale **training dataset** used to train our specialist TCG models. It provides a rich source of problems and solutions for fine-tuning models on code intelligence tasks.

### Local Assets in this Repository

*   **TCGBench-Lite Problem Set:**
    *   Contains the problem descriptions for the 270 problems utilized in our primary experiments. This dataset is meticulously curated from recent competitive programming contests to ensure contemporary relevance and minimize data leakage.
    *   **Location:** `data/tcgbenc_lite_problems.jsonl` (A demo is provided)
*   **SAGA Prompt Templates:**
    *   The detailed and structured prompt templates for both Multidimensional and Differential Analysis that guide the LLM in the SAGA framework.
    *   **Location:** `prompts/`
*   **Demo of a SAGA-Generated Test Case:**
    *   A concrete example of a Python script for a generated test case, illustrating its structure and complexity.
    *   **Location:** `demos/parse.py`

## 🛠️ Integration with OpenCompass (Coming Soon)

The **CodeCompass Benchmark** will be a component of the OpenCompass ecosystem. It is designed for seamless integration into the [**OpenCompass**](https://github.com/open-compass/opencompass) evaluation framework, providing the community with a powerful new tool for rigorously assessing the capabilities of code generation models.

## Citation

If you find our work useful in your research, please consider citing our paper:

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
```
