# SAGA: Strategic Adversarial & Constraint-differential Generative workflow for Test Case Generation

[![arXiv](https://img.shields.io/badge/arXiv-XXXXX-b31b1b.svg)](https://arxiv.org/abs/xxxxx)
[![CodeCompass/SAGA Codeforces Data on Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-CodeCompass-blue)](https://huggingface.co/datasets/MichaelErchi/CodeCompass)

This repository is the official implementation and supplementary material for the research paper, **"Rethinking Verification for LLM Code Generation: From Generation to Testing."** This work is a proud contribution to the robust evaluation of large language models from the team at OpenCompass.

## 🚀 Introduction to SAGA

Current benchmarks for evaluating Large Language Model code generation often rely on a limited or homogeneous set of test cases. This can lead to inflated performance metrics and hinder the development of truly robust and reliable models.

To address these critical shortcomings, we introduce **SAGA (Strategic Adversarial & Constraint-differential Generative workflow)**, a novel human-LLM collaborative framework for advanced Test Case Generation (TCG). SAGA systematically integrates deep human programming expertise with the reasoning capabilities of LLMs to produce high-quality, diverse, and discriminative test suites. It achieves this through a dual-pronged analytical approach:

*   **Multidimensional Analysis:** Leveraging profound insights from correct human solutions to engineer challenging test scenarios.
*   **Differential Analysis:** Identifying subtle error patterns by analyzing incorrect human submissions against their corrected versions.

The core mission of SAGA is to significantly enhance the verification of LLM-generated code by maximizing both individual test case potency and overall test suite diversity.

## 🌟 Key Assets

This repository provides the following key assets to support full reproducibility and further research:

*   **TCGBench-Lite Dataset:**
    *   Contains the problem descriptions for the 270 problems utilized in our primary experiments.
    *   This dataset is meticulously curated from recent competitive programming contests to ensure contemporary relevance and minimize data leakage.
    *   **Location:** `data/tcgbenc_lite_problems.jsonl` (A demo is provided)
*   **CodeCompass Verifiers:**
    *   A comprehensive collection of the SAGA-generated verifiers for all problems in TCGBench-Lite, showcasing the powerful output of our framework.
    *   **Location:** `data/codecompass_verifiers_sample/` (A representative sample)
    *   **Full Dataset:** [**CodeCompass on Hugging Face**](Yhttps://huggingface.co/datasets/MichaelErchi/CodeCompass)
*   **SAGA Codeforces Training Data:**
    *   The dataset used to train our specialist TCG models, generated using the SAGA framework.
    *   **Full Dataset:** [**SAGA Codeforces Data on Hugging Face**](https://huggingface.co/datasets/MichaelErchi/CodeCompass)
*   **SAGA Prompt Templates:**
    *   The detailed and structured prompt templates for both Multidimensional and Differential Analysis that guide the LLM in the SAGA framework.
    *   **Location:** `prompts/`
*   **Demo of a SAGA-Generated Test Case:**
    *   A concrete example of a Python script for a generated test case, illustrating its structure and complexity.
    *   **Location:** `demos/parse.py`

## 🛠️ Coming Soon to OpenCompass

We are excited to announce that **CodeCompass**, our high-quality, SAGA-generated benchmark, is in the process of being integrated into the [**OpenCompass**](https://github.com/open-compass/opencompass) evaluation framework. This will provide the community with a powerful new tool for rigorously assessing the capabilities of code generation models. Stay tuned for the official release!

## Citation

If you find our work useful in your research, please consider citing our paper:

```bibtex
@misc{ma2025rethinking,
      title={Rethinking Verification for LLM Code Generation: From Generation to Testing},
      author={Zihan Ma and Taolin Zhang and Maosong Cao and Wenwei Zhang and Minnan Luo and Songyang Zhang and Kai Chen},
      year={2025},
      eprint={XXXXX},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}