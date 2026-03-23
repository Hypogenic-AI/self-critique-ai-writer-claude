# Resources Catalog

## Summary

This document catalogs all resources gathered for the research project: **"Is self-critique enough to get good AI story writers?"** The hypothesis is that LLMs can significantly improve their story writing abilities by using self-critique as their own reward function, without external feedback.

---

## Papers

Total papers downloaded: **23**

| # | Title | Authors | Year | File | Key Relevance |
|---|-------|---------|------|------|---------------|
| 1 | Writing-Zero | Jia et al. | 2025 | papers/2506.00103_writing_zero.pdf | Pairwise self-critique GenRM for writing RL |
| 2 | Self-Rewarding Language Models | Yuan et al. | 2024 | papers/2401.10020_self_rewarding_language_models.pdf | Iterative self-reward + DPO loop |
| 3 | Collective Critics for Story Gen | Bae & Kim | 2024 | papers/2410.02428_collective_critics_story_gen.pdf | Multi-agent critique for stories |
| 4 | Self-Refine | Madaan et al. | 2023 | papers/2303.17651_self_refine.pdf | Inference-time self-critique loop |
| 5 | Constitutional AI | Bai et al. | 2022 | papers/2212.08073_constitutional_ai.pdf | RLAIF paradigm |
| 6 | RLAIF vs RLHF | Lee et al. | 2023 | papers/2309.00267_rlaif_vs_rlhf.pdf | AI feedback = human feedback |
| 7 | Spontaneous Reward Hacking | - | 2024 | papers/2407.04549_spontaneous_reward_hacking.pdf | Self-critique reward divergence |
| 8 | No Free Lunch | - | 2025 | papers/2506.17219_no_free_lunch_internal_feedback.pdf | Limits of internal feedback |
| 9 | EvolvR | - | 2025 | papers/2508.06046_evolvr_story_evaluation.pdf | Self-evolved story evaluator → reward |
| 10 | PREFINE | - | 2025 | papers/2510.21721_prefine_personalized_story.pdf | Personalized story critique-refine |
| 11 | LLMs Can Self-Improve | Huang et al. | 2022 | papers/2210.11610_llm_can_self_improve.pdf | Self-generated training signal |
| 12 | RL Contemplation | Zhang et al. | 2023 | papers/2305.14483_lm_self_improvement_rl_contemplation.pdf | Self-critique as RL reward |
| 13 | Self-Evolved Reward Learning | - | 2024 | papers/2411.00418_self_evolved_reward_learning.pdf | Self-bootstrapping reward model |
| 14 | DPO | Rafailov et al. | 2023 | papers/2305.18290_dpo_direct_preference_optimization.pdf | Training with preference pairs |
| 15 | Judging LLM-as-Judge | Zheng et al. | 2023 | papers/2306.05685_judging_llm_as_judge.pdf | LLM evaluation biases |
| 16 | LLM Creativity (Literary) | - | 2023 | papers/2312.03746_evaluating_llm_creativity_literary.pdf | Creative writing evaluation |
| 17 | Small But Funny | - | 2024 | papers/2402.18113_small_but_funny_humor.pdf | Feedback-driven humor improvement |
| 18 | Self-Improvement (ISC) | - | 2024 | papers/2404.12253_self_improvement_imagination_searching_criticizing.pdf | Imagination + critique |
| 19 | HoLLMwood | - | 2024 | papers/2406.11683_hollmwood_screenwriting.pdf | Multi-role screenwriting |
| 20 | TF1-EN-3M | - | 2025 | papers/2504.20605_tf1_en_3m_moral_fables.pdf | Synthetic moral fables dataset |
| 21 | Self-RAG | - | 2023 | papers/2310.12921_self_rag.pdf | Self-reflection tokens |
| 22 | SPIN | - | 2024 | papers/2401.01335_spin_self_play_fine_tuning.pdf | Self-play fine-tuning |
| 23 | Writing Quality Benchmark | - | 2025 | papers/2501.11425_writing_quality_benchmark.pdf | Writing quality evaluation |

See `papers/README.md` for detailed descriptions.

---

## Datasets

Total datasets downloaded: **6**

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| WritingPrompts | HuggingFace `euclaise/writingprompts` | 5,000 (subset) | Story generation | datasets/writingprompts/ | Reddit prompts + human stories |
| TinyStories | HuggingFace `roneneldan/TinyStories` | 5,000 (subset) | Story generation | datasets/tinystories/ | Simple short stories |
| ROCStories | HuggingFace `gimmaru/story_cloze-2016` | 1,000 (subset) | Story completion | datasets/rocstories/ | 5-sentence stories |
| HANNA (original) | GitHub dig-team/hanna-benchmark-asg | 3,168 annotations | Story evaluation | datasets/hanna/ | Human annotations: 6 quality dims |
| HANNA (LLM eval) | HuggingFace | 1,000 (subset) | Story evaluation | datasets/hanna_llm/ | LLM evaluation variant |
| OpenMEVA | HuggingFace `Jiann/OpenMEVA` | 1,000 (subset) | Story evaluation | datasets/openmeva/ | Multi-model evaluation |

See `datasets/README.md` for download instructions and detailed descriptions.

### Key Dataset Features for Our Research

- **WritingPrompts**: Best for training — large-scale prompt→story pairs for self-critique experiments
- **HANNA**: Best for evaluation — human annotations across 6 quality dimensions (Relevance, Coherence, Empathy, Surprise, Engagement, Complexity) that can serve as self-critique rubric dimensions
- **OpenMEVA**: Useful for comparing model outputs on the same prompts
- **TinyStories/ROCStories**: Useful for smaller-scale experiments and ablations

---

## Code Repositories

Total repositories cloned: **4**

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| CritiCS | github.com/EMNLP-2024-CritiCS/Collective-Critics-for-Creative-Story-Generation | Multi-agent story critique | code/critics-collective/ | Primary comparison system |
| Self-Refine | github.com/madaan/self-refine | Inference-time self-critique | code/self-refine/ | Core self-critique baseline |
| DOC-StoryGen-v2 | github.com/facebookresearch/doc-storygen-v2 | Story generation baseline | code/doc-storygen-v2/ | Plan-then-generate pipeline |
| HANNA Benchmark | github.com/dig-team/hanna-benchmark-asg | Story evaluation | code/hanna-benchmark/ | Human annotation benchmark |

See `code/README.md` for detailed descriptions.

### Missing Code (Not Released)
- **Writing-Zero**: Proprietary (Alibaba/Quark LLM)
- **Self-Rewarding Language Models**: Not released (Meta)
- **EvolvR**: Not yet released (2025 paper)
- **PREFINE**: Not yet released (2025 paper)

---

## Resource Gathering Notes

### Search Strategy
1. Used paper-finder service with 3 targeted queries in "diligent" mode (~520 papers scanned)
2. Prioritized papers by topic relevance score combining: (a) search relevance, (b) keyword matches for story/writing + self-critique/self-reward, (c) citation count
3. Resolved arXiv IDs via Semantic Scholar API + direct arXiv search
4. Datasets identified from literature review + HuggingFace search

### Selection Criteria
- Papers: Direct relevance to self-critique AND creative writing/story generation
- Datasets: Story generation training data + story quality evaluation benchmarks with human annotations
- Code: Implementations of key baselines and evaluation frameworks

### Challenges Encountered
1. Three arXiv downloads initially returned wrong PDFs (IDs resolved to different papers) — corrected
2. EvolvR has no public code despite being a 2025 paper
3. Most self-reward training code (Writing-Zero, Self-Rewarding LMs) is proprietary
4. ROCStories full dataset requires registration; used available HuggingFace mirror

### Gaps and Workarounds
- No single paper combines self-critique reward + RL/DPO specifically for English narrative fiction → this IS our research gap
- No public implementation of Writing-Zero's BRPO or Self-Rewarding LMs' training loop → will need to implement from paper descriptions
- Story evaluation benchmarks (HANNA, OpenMEVA) focus on shorter stories → may need adaptation for longer narratives

---

## Recommendations for Experiment Design

### 1. Primary Dataset
**WritingPrompts** — large-scale English prompt→story pairs. Use prompts as generation seeds; human-written stories as quality reference.

### 2. Evaluation Datasets
- **HANNA** dimensions (Relevance, Coherence, Empathy, Surprise, Engagement, Complexity) as the multi-criteria rubric for self-critique
- **GPT-4 pairwise comparison** as scalable evaluation proxy

### 3. Experimental Conditions
1. **Baseline**: Direct generation (no critique)
2. **Self-Refine** (inference-time): Single-model critique → revise loop
3. **Self-Rewarding DPO** (training-time): Generate N stories, self-score, create preference pairs, DPO train
4. **Multi-agent critique** (CRITICS-style): Multiple specialized critics, as comparison

### 4. Evaluation Metrics
- Human pairwise preference (gold standard)
- GPT-4 pairwise comparison
- HANNA-style multi-criteria scoring
- Reward hacking indicators: response length, diversity (distinct-n), style collapse detection

### 5. Code to Adapt/Reuse
- **Self-Refine** (`code/self-refine/`): Adapt critique loop for story-specific rubric
- **DOC** (`code/doc-storygen-v2/`): Use as story generation baseline
- **HANNA** (`code/hanna-benchmark/`): Use evaluation framework and criteria
- **CritiCS** (`code/critics-collective/`): Multi-agent critique comparison system
