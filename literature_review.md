# Literature Review: Is Self-Critique Enough to Get Good AI Story Writers?

## Research Area Overview

This literature review examines whether large language models (LLMs) can significantly improve their story writing abilities through self-critique as their own reward function, without external human feedback. The research sits at the intersection of three active areas: (1) LLM self-improvement and self-reward mechanisms, (2) AI-assisted creative/story writing, and (3) evaluation of creative text generation.

The field has seen rapid progress in LLM self-improvement for tasks with verifiable answers (math, code), but creative writing poses unique challenges: there is no ground truth, quality is subjective, and evaluation requires aesthetic judgment. Recent work has explored various approaches — from iterative self-refinement at inference time to training-time self-reward loops — with mixed results on whether self-critique alone is sufficient.

---

## Key Papers

### 1. Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards
- **Authors**: Jia et al. (Alibaba/Quark LLM), 2025
- **Source**: arXiv:2506.00103
- **Key Contribution**: Converts subjective writing quality into verifiable pairwise preference signals via a Self-Principled Critique Tuning (SPCT) generative reward model (GenRM), combined with Bootstrapped Relative Policy Optimization (BRPO) that uses within-batch responses as dynamic references.
- **Methodology**: Two-stage: (1) Train a pairwise GenRM that generates writing-specific evaluation principles, critiques two responses, and outputs comparative scores; (2) Use BRPO for RL training where one response from the same batch serves as the reference.
- **Datasets**: In-house Chinese writing preference data (~10K pairs), WritingBench, in-house Writing Testset (211 queries).
- **Results**: Writing-Zero (pure RL from base, no SFT) achieves 3.84 on Writing Testset, surpassing Qwen3-32B-Instruct (3.32) and DeepSeek-R1 (3.20). GenRM-based training produces 7x less reward hacking than scalar RM (58 vs 417 tokens of self-justification).
- **Code**: Not released (proprietary).
- **Relevance**: **Most directly relevant paper.** Demonstrates that pairwise self-critique can serve as a viable reward signal for creative writing RL, achieving competitive results without SFT. Key insight: structured critique (generating principles before scoring) is more robust than scalar rewards.

### 2. Self-Rewarding Language Models
- **Authors**: Yuan et al. (Meta/NYU), 2024
- **Source**: arXiv:2401.10020
- **Key Contribution**: A single LLM simultaneously acts as both instruction-follower and reward model, with both capabilities improving through iterative self-training via DPO.
- **Methodology**: Seed model trained on IFT + EFT (evaluation fine-tuning) data. Each iteration: generate N=4 responses, self-score with 5-point rubric, create preference pairs (best vs worst), train with DPO.
- **Datasets**: Open Assistant (3,200 IFT + 1,630 EFT examples), AlpacaEval 2.0, MT-Bench.
- **Results**: After 3 iterations, MT-Bench writing score improves from 8.83→9.58 (strongest category gain). AlpacaEval win rate reaches 20.44%, surpassing Claude 2 and GPT-4 0613.
- **Code**: Not released.
- **Relevance**: **Core foundational paper.** Proves iterative self-reward improves LLM output quality, with writing showing the largest gains. However, response length inflates significantly (1,092→2,552 tokens), raising reward hacking concerns.

### 3. Collective Critics for Creative Story Generation (CRITICS)
- **Authors**: Bae & Kim (UNIST), 2024
- **Source**: arXiv:2410.02428, EMNLP 2024
- **Key Contribution**: Multi-agent critique framework with diverse critics (3 for plans, 2 for text), adaptive personas, a leader for selection, and an evaluator for the creativity-coherence trade-off.
- **Methodology**: Two stages: CRPLAN (critique story plan with 3 creativity criteria) and CRTEXT (critique individual sentences for imagery and voice). Each stage uses multiple rounds of critique with a leader selecting the best feedback.
- **Datasets**: 300 premises from DOC dataset.
- **Results**: +27pp improvement in creativity and interestingness over DOC baseline. Ablations show multiple criteria, personas, and leaders are all essential.
- **Code**: Released at [GitHub](https://github.com/EMNLP-2024-CritiCS/Collective-Critics-for-Creative-Story-Generation)
- **Relevance**: **Key counterpoint to our hypothesis.** Demonstrates that *single-agent* self-critique is insufficient; diverse multi-agent critique with structured roles is needed for meaningful creative improvement. Also shows creativity-coherence trade-off requiring careful management.

### 4. Self-Refine: Iterative Refinement with Self-Feedback
- **Authors**: Madaan et al. (CMU/Allen AI), 2023
- **Source**: arXiv:2303.17651
- **Key Contribution**: Foundational framework for LLM self-critique: generate → critique → refine loop, all with the same model, no training required.
- **Methodology**: Single model generates output, provides structured feedback, then revises. Tested on 7 tasks.
- **Results**: ~20% average improvement across tasks (5-40% range) using GPT-3.5 and GPT-4.
- **Relevance**: Establishes that inference-time self-critique works for improving quality. However, this is test-time refinement, not training — the model doesn't permanently improve.

### 5. Constitutional AI: Harmlessness from AI Feedback
- **Authors**: Bai et al. (Anthropic), 2022
- **Source**: arXiv:2212.08073
- **Key Contribution**: Two-phase approach: (1) model self-critiques and revises outputs using written principles, (2) AI-generated preference labels train a reward model for RL (RLAIF).
- **Relevance**: Establishes the paradigm of using AI feedback (including self-critique) as a substitute for human feedback in training loops.

### 6. RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback
- **Authors**: Lee et al. (Google), 2023
- **Source**: arXiv:2309.00267
- **Key Contribution**: Systematic comparison showing RLAIF matches RLHF performance. Direct-RLAIF (bypassing reward model) actually outperforms standard RLAIF.
- **Relevance**: Validates that AI-generated feedback is a viable substitute for human feedback — core justification for self-critique as reward signal.

### 7. Spontaneous Reward Hacking in Iterative Self-Refinement
- **Authors**: 2024
- **Source**: arXiv:2407.04549
- **Key Contribution**: Demonstrates that LLM evaluator ratings diverge from human judgments over refinement iterations — reward hacking emerges spontaneously without adversarial intent.
- **Results**: Essay editing tasks show LLM evaluator scores increase while human quality assessments plateau or decline. Larger models and shared context amplify the problem.
- **Relevance**: **Critical warning.** Self-critique loops for story writing may produce inflated quality scores that don't reflect actual improvement. Mitigation strategies are essential.

### 8. No Free Lunch: Rethinking Internal Feedback for LLM Reasoning
- **Authors**: 2025
- **Source**: arXiv:2506.17219
- **Key Contribution**: Examines when and why LLM self-critique fails to improve outputs, finding that internal feedback alone has fundamental limitations.
- **Relevance**: Provides theoretical grounding for understanding the boundaries of self-critique effectiveness.

### 9. EvolvR: Self-Evolving Pairwise Reasoning for Story Evaluation to Enhance Generation
- **Authors**: 2025
- **Source**: arXiv:2508.06046
- **Key Contribution**: Framework to improve LLM-as-judge for story evaluation via self-synthesized CoT reasoning data with multi-persona strategy. The trained evaluator serves as a reward model for generation improvement.
- **Results**: SOTA on StoryER, HANNA, and OpenMEVA benchmarks. When used as reward model, significantly improves story quality.
- **Relevance**: **Directly relevant.** Shows a concrete pipeline from self-evolved story evaluation to generation improvement via reward modeling.

### 10. PREFINE: Personalized Story Generation via Simulated User Critics
- **Authors**: 2025
- **Source**: arXiv:2510.21721
- **Key Contribution**: Critique-and-refine framework for personalized story generation with simulated user agents and user-specific rubrics.
- **Results**: Outperforms existing methods on PerDOC and PerMPST benchmarks.
- **Relevance**: Demonstrates critique-refine loop applied specifically to story writing with personalized evaluation criteria.

### 11. Small But Funny: A Feedback-Driven Approach to Humor Distillation
- **Authors**: 2024
- **Source**: arXiv:2402.18113
- **Key Contribution**: Uses LLM feedback to distill humor-writing ability from large to small models through iterative refinement.
- **Relevance**: Shows self-critique/feedback loops can improve a specific creative writing skill (humor), analogous to story quality.

### 12. Evaluating Large Language Model Creativity from a Literary Perspective
- **Authors**: 2023
- **Source**: arXiv:2312.03746
- **Key Contribution**: Framework for evaluating LLM creative writing using literary criticism and computational creativity criteria.
- **Relevance**: Provides evaluation methodology essential for measuring story quality improvements.

### 13. Direct Preference Optimization (DPO)
- **Authors**: Rafailov et al. (Stanford), 2023
- **Source**: arXiv:2305.18290
- **Key Contribution**: Eliminates need for explicit reward model by extracting optimal policy directly from preference pairs via classification loss.
- **Relevance**: Key training algorithm — self-critique-derived preference pairs (better/worse story pairs) can directly fine-tune the generator without a separate reward model.

### 14. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Authors**: Zheng et al. (UC Berkeley/LMSYS), 2023
- **Source**: arXiv:2306.05685
- **Key Contribution**: Validates LLM-as-judge achieves >80% agreement with humans. Identifies key biases: position bias, verbosity bias, self-enhancement bias.
- **Relevance**: Establishes both the viability and the risks of using LLM self-evaluation as a quality signal for story writing.

### 15. Large Language Models Can Self-Improve
- **Authors**: Huang et al. (Google), 2022
- **Source**: arXiv:2210.11610
- **Key Contribution**: Uses CoT + self-consistency to generate pseudo-labels, then fine-tunes on own outputs.
- **Results**: GSM8K: 74.4%→82.1% through self-generated training data alone.
- **Relevance**: Demonstrates self-evaluation can generate training signal strong enough for genuine model improvement.

### 16. Language Model Self-improvement by RL Contemplation
- **Authors**: Zhang et al., 2023
- **Source**: arXiv:2305.14483
- **Key Contribution**: Unsupervised RL framework (SIRLC) where the LM assigns quality scores to its own outputs and optimizes to maximize those self-scores.
- **Results**: ~5.6% accuracy on reasoning; BERTScore 0.82→0.86 on translation.
- **Relevance**: Directly implements self-critique as RL reward, showing it works beyond reasoning to open-ended generation.

### 17. Self-Evolved Reward Learning for LLMs
- **Authors**: 2024
- **Source**: arXiv:2411.00418
- **Key Contribution**: Reward model generates additional training data to iteratively improve itself, reducing dependence on human-labeled preferences.
- **Relevance**: Shows how self-generated feedback can bootstrap reward model quality alongside the generator.

---

## Common Methodologies

### Self-Critique Approaches
1. **Inference-time self-refinement** (Self-Refine): Generate → Critique → Revise loop. No training, immediate improvement, but no permanent learning.
2. **Self-rewarding training loops** (Self-Rewarding LMs, Writing-Zero): Model generates preference data via self-evaluation, then trains on it via DPO/RL. Permanent improvement but risk of reward hacking.
3. **Multi-agent critique** (CRITICS, PREFINE): Multiple specialized critic agents provide diverse feedback. More robust but more complex.
4. **Constitutional/principle-based critique** (Constitutional AI, Writing-Zero SPCT): Self-critique guided by explicit principles or rubrics.

### Training Paradigms
- **DPO** (most common): Preference pairs from self-evaluation → direct policy optimization.
- **GRPO/PPO**: RL with self-generated reward signal.
- **BRPO** (Writing-Zero): Bootstrapped within-batch reference for RL on non-verifiable tasks.
- **SFT on filtered outputs**: Fine-tune on high-quality self-generated examples only.

---

## Standard Baselines

For story generation evaluation:
- **DOC** (Detailed Outline Control): Hierarchical plan-then-generate pipeline
- **Re3**: Recursive reprompting and revision for long stories
- Standard LLMs (GPT-4, Claude, Llama) in zero/few-shot

For self-improvement evaluation:
- **SFT-only models**: Supervised fine-tuning without self-reward loop
- **Scalar RM + GRPO/PPO**: Traditional reward model approach
- **RLHF**: Human feedback baseline

---

## Evaluation Metrics

### Automatic Metrics for Story Quality
- **WritingBench** (Wu et al., 2025): 6 core domains, 100 subdomains (note: hackable per Writing-Zero)
- **StoryER, HANNA, OpenMEVA**: Story evaluation benchmarks used by EvolvR
- **MT-Bench writing category**: Part of broader instruction-following benchmark
- **AlpacaEval**: General instruction-following win rate

### LLM-as-Judge Metrics
- GPT-4 pairwise comparison (most common)
- Multi-criteria rubrics (creativity, coherence, interestingness, relevance)
- Mozaffari's rubric: Image, Voice, Originality (used by CRITICS)

### Human Evaluation
- Pairwise preference comparisons (most reliable)
- Multi-dimensional scoring (interesting, coherent, creative, relevant)
- Inter-annotator agreement via Fleiss' Kappa or Cohen's Kappa

---

## Gaps and Opportunities

1. **No direct test of self-critique for English story writing**: Writing-Zero works on Chinese writing; CRITICS uses inference-time critique without training. No paper combines self-critique reward + RL/DPO specifically for English narrative fiction.

2. **Reward hacking is under-addressed**: Spontaneous reward hacking paper shows the problem; Writing-Zero offers a partial solution (pairwise GenRM); but robust solutions for story-specific hacking (length, purple prose, cliché exploitation) are missing.

3. **Creative dimensions poorly captured**: Most self-reward rubrics focus on helpfulness/correctness. Story-specific dimensions (plot coherence, character development, narrative arc, emotional impact, prose style) need specialized rubrics.

4. **Small model capability**: Most work uses 70B+ models. Whether self-critique works for smaller models (7B-13B) on creative tasks is unclear.

5. **Evaluation reliability**: LLM-as-judge for story quality has known biases. EvolvR addresses this but the trained evaluator hasn't been validated as a reward model for training loops.

---

## Recommendations for Our Experiment

### Recommended Datasets
1. **WritingPrompts** (Reddit, via HuggingFace): Large corpus of writing prompts with human-written stories — good for training and baseline comparison
2. **HANNA** / **OpenMEVA**: Story evaluation benchmarks for measuring critique quality
3. **DOC premises** (300 premises): Standard evaluation set for story generation

### Recommended Baselines
1. **No self-critique**: Direct generation (temperature sampling)
2. **Self-Refine** (inference-time): Single-pass self-critique + revision
3. **Multi-iteration self-reward + DPO**: Following Self-Rewarding LMs methodology
4. **Multi-agent critique**: Following CRITICS methodology

### Recommended Metrics
1. **Human pairwise preference**: Gold standard
2. **GPT-4 pairwise comparison**: Scalable proxy
3. **Multi-criteria scoring**: Creativity, coherence, interestingness, character, plot (5-point scales)
4. **Reward hacking indicators**: Response length, self-justification length, diversity metrics

### Methodological Considerations
- Use **pairwise** comparison rather than scalar scoring to reduce reward hacking (per Writing-Zero)
- Design **story-specific rubrics** covering narrative dimensions, not just general quality
- Monitor for **length inflation** and **style collapse** across iterations
- Consider **multi-criteria critique** rather than single-dimension evaluation
- Include **diversity metrics** to detect mode collapse
- Use **held-out human evaluation** as ground truth, not just LLM-as-judge scores
