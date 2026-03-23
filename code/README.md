# Code Repositories

This directory contains cloned repositories relevant to the research question:
**"Is self-critique enough to get good AI story writers?"**

All repos were cloned with `--depth 1` (shallow clone) to save space.

---

## 1. CRITICS — Collective Critics for Creative Story Generation

**Directory:** `critics-collective/`
**URL:** https://github.com/EMNLP-2024-CritiCS/Collective-Critics-for-Creative-Story-Generation
**Paper:** [Collective Critics for Creative Story Generation](https://arxiv.org/abs/2410.02428), EMNLP 2024. Minwook Bae, Hyounghun Kim.

### Purpose
CritiCS is the most directly relevant system to the research question. It replaces single-model self-critique with a **collective of critics** — multiple LLM agents that critique story drafts from different angles. Each critic provides targeted feedback (e.g., plot coherence, character consistency), and the critiques are aggregated before a revision pass. This directly tests whether multi-agent critique outperforms self-critique.

### Key Files
- `critics/` — Core critic agent implementations (plan-level and text-level critics)
- `scripts/` — Pipeline scripts: `server_load.sh`, `start_servers.py`, `close_servers.py`; subdirs `premise/`, `plan/`, `story/`
- `storygen/` — Story generation modules
- `evaluation/evaluation_gpt4.py` — GPT-4-based automatic evaluation script
- `evaluation/run_evaluation.sh` — Evaluation runner
- `app.sh` + `home.py` — Streamlit interface for visualizing generated stories and critic outputs
- `requirements.txt` — Dependencies

### Dependencies
- Python 3.9, conda environment
- langchain 0.2.x, langchain-openai, langchain-community
- openai 0.28.0 (GPT-4 access required)
- vllm 0.1.7 (for serving open-source models)
- transformers 4.33.2, ray, streamlit

### Relation to Research Question
This is the **primary experimental system**. It directly challenges the sufficiency of self-critique by introducing collective criticism. Comparing CritiCS outputs against self-critique baselines (e.g., Self-Refine) on story quality metrics answers the central question. Note: its base code is forked from DOC story generation (see repo 4 below).

---

## 2. Self-Refine — Iterative Refinement with Self-Feedback

**Directory:** `self-refine/`
**URL:** https://github.com/madaan/self-refine
**Paper:** [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651), NeurIPS 2023. Madaan et al. (CMU/Allen AI/Google).

### Purpose
Self-Refine is the canonical implementation of **single-model self-critique and revision**. A single LLM generates an output, critiques its own output, then refines it — looping until a stopping criterion is met. Evaluated across 7 tasks including dialogue, math, and code; story generation is not a primary task but the framework is general. This is the main **baseline** for the research question.

### Key Files
- `src/` — Task implementations: `acronym/`, `commongen/`, `gsm/`, `pie/`, `readability/`, `responsegen/`, `sentiment_reversal/`
- Each task has three prompt files: `task_init.py` (generate), `feedback.py` (critique), `task_iterate.py` (refine)
- Each task has a `run.py` entry point
- `colabs/Visual-Self-Refine-GPT4V.ipynb` — Visual self-refine demo
- `data/` — Task-specific datasets and prompts

### Dependencies
- [prompt-lib](https://github.com/reasoning-machines/prompt-lib) (must be cloned separately and installed)
- OpenAI API key required (uses GPT-3.5, ChatGPT, GPT-4)
- No `requirements.txt` in root; install prompt-lib manually

### Relation to Research Question
Self-Refine **is the self-critique hypothesis made concrete**. It shows ~20% improvement over one-shot generation on several tasks using only self-critique. For story writing specifically, this repo provides the architecture to adapt or compare against. The core question is whether this loop is sufficient for story quality, or whether external/collective critique (CritiCS) is needed.

---

## 3. EvolvR — Self-Evolving Pairwise Reasoning for Story Evaluation

**Directory:** N/A (no public GitHub repository found)
**Paper:** [EvolvR: Self-Evolving Pairwise Reasoning for Story Evaluation to Enhance Generation](https://arxiv.org/abs/2508.06046), August 2025.

### Purpose
EvolvR trains open-source models to act as story **evaluators** using pairwise comparison rather than pointwise scoring. It self-synthesizes Chain-of-Thought evaluation data via a multi-persona strategy, filters it with multi-agent consistency checks, and trains an evaluator that can serve as a reward model for story generation. Achieves state-of-the-art on StoryER, HANNA, and OpenMEVA benchmarks.

### Key Files
No code repository has been publicly released as of March 2026. The paper is available at the arXiv link above.

### Dependencies
Unknown (no code released).

### Relation to Research Question
EvolvR is relevant as an **evaluation methodology**: it provides a more reliable automated judge for story quality than GPT-4 pointwise scoring. Its pairwise reward model could be used to measure whether self-critique or collective critique produces better stories. Also relevant as a case study in "self-evolving" systems — the evaluator itself improves through a self-critique-like data synthesis loop.

---

## 4. DOC Story Generation V2 — Detailed Outline Control

**Directory:** `doc-storygen-v2/`
**URL:** https://github.com/facebookresearch/doc-storygen-v2
**Original:** https://github.com/yangkevin2/doc-story-generation
**Paper:** [DOC: Improving Long Story Coherence With Detailed Outline Control](https://arxiv.org/abs/2212.10077), ACL 2023. Kevin Yang et al.

### Purpose
DOC is a **story generation baseline** and foundational architecture. It generates multi-thousand-word stories using a three-stage pipeline: Premise → Plan (hierarchical outline) → Story. The v2 rewrite (Facebook Research) supports modern open-source LLMs and chat-based models. CritiCS (repo 1) is built directly on top of DOC's architecture.

### Key Files
- `scripts/` — Main entry point; subdirs `premise/`, `plan/`, `story/` each with `generate.py`
- `scripts/start_servers.py` / `close_servers.py` — VLLM server management
- `storygen/` — Core library: `common/`, `plan/`, `premise/`, `story/`
- `config.yaml` files in each step subdirectory — Model and generation configuration (fill in TODO fields for model selection)
- `prompts.json` — All generation prompts in one file
- `requirements.txt` — Dependencies

### Dependencies
- Python 3.9
- vllm 0.1.7 (requires one-line patch; see README)
- openai 0.28.0
- langchain 0.0.329, transformers 4.33.2, ray 2.8.0
- GPU required for VLLM-served open-source models

### Relation to Research Question
DOC represents the **outline-controlled generation baseline** — no critique loop, just structured planning. Comparing story quality between DOC (no critique), Self-Refine (self-critique), and CritiCS (collective critique) isolates the contribution of critique mechanisms. DOC also provides the 3-stage pipeline architecture that CritiCS inherits.

---

## 5. HANNA Benchmark — Human-ANnotated NArratives for ASG Evaluation

**Directory:** `hanna-benchmark/`
**URL:** https://github.com/dig-team/hanna-benchmark-asg
**Paper:** [Do Language Models Enjoy Their Own Stories? Prompting Large Language Models for Automatic Story Evaluation](https://doi.org/10.1162/tacl_a_00689), TACL 2024. Chhun, Suchanek, Clavel.

### Purpose
HANNA is the primary **evaluation benchmark** for automated story generation (ASG). It provides 1,056 human-annotated stories generated from 96 WritingPrompts prompts, each annotated by 3 crowdworkers on 6 criteria: Relevance, Coherence, Empathy, Surprise, Engagement, and Complexity — totaling 19,008 annotations. Also includes scores from 72 automatic metrics and 4 LLM evaluators (Beluga-13B, Llama-13B, Mistral-7B, ChatGPT).

### Key Files
- `hanna_stories_annotations.csv` — Raw per-story per-annotator scores across 6 criteria
- `hanna_metric_scores_llm.csv` — Average human scores, LLM scores, and 72 automatic metric scores per system
- `hanna_llm_stories.csv` — 576 stories from 6 modern LLMs (Llama-7B through Platypus2-70B)
- `llm_answers/` — Complete LLM evaluation responses
- `user_study.csv` — ~1,500 human annotations on LLM-generated explanations
- `data_visualization.ipynb` — Analysis notebook reproducing paper results
- `fdr.py` — Statistical analysis utilities
- `requirements.txt` — Dependencies

### Dependencies
- Python 3.9.7
- pandas, numpy, scipy, scikit-learn, statsmodels, seaborn, matplotlib
- pingouin (statistical tests), irrcac (inter-rater reliability)
- [nlp-williams](https://github.com/inmoonlight/nlp-williams/) — must be downloaded separately (licensing reasons)

### Relation to Research Question
HANNA provides the **gold standard evaluation dataset** for the research. To test whether self-critique produces good stories, we need a reliable human-grounded metric. HANNA's 6 criteria (especially Coherence, Engagement) can be used to evaluate outputs from DOC, Self-Refine, and CritiCS. The benchmark also tests whether LLM evaluators agree with human judgments — critical for automated evaluation of self-critique loops.

---

## Summary Table

| Repo | Role | Critique Type | Has Code |
|------|------|---------------|----------|
| `critics-collective/` | Primary system | Multi-agent collective critique | Yes |
| `self-refine/` | Primary baseline | Single-model self-critique | Yes |
| EvolvR | Evaluation methodology | Self-evolving evaluator | No (paper only) |
| `doc-storygen-v2/` | Generation baseline | No critique | Yes |
| `hanna-benchmark/` | Evaluation benchmark | Human + LLM annotations | Yes (data + code) |

## Research Question Mapping

**"Is self-critique enough to get good AI story writers?"**

- **Self-critique** = Self-Refine loop (repo 2)
- **"Enough"** measured against = HANNA benchmark criteria (repo 5)
- **Alternative** = CritiCS collective critique (repo 1), which adds multi-agent criticism on top of DOC (repo 4)
- **Automated evaluation validity** = EvolvR paper (no code) shows LLM-as-judge works better with pairwise comparison

The experimental pipeline would be: generate stories with DOC / Self-Refine / CritiCS, evaluate on HANNA criteria (human or automated), compare.
