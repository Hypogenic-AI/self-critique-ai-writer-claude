# Research Plan: Is Self-Critique Enough to Get Good AI Story Writers?

## Motivation & Novelty Assessment

### Why This Research Matters
LLMs are increasingly used for creative writing, but their output quality plateaus without external feedback. If self-critique alone can meaningfully improve story quality, it would enable autonomous writing improvement without costly human annotation — democratizing high-quality AI writing assistance.

### Gap in Existing Work
From the literature review: No paper combines self-critique reward with systematic evaluation specifically for English narrative fiction at inference time across multiple iteration depths. Writing-Zero works on Chinese writing with training-time RL. Self-Refine tested broadly but didn't deeply analyze creative writing dimensions. CRITICS uses multi-agent critique but doesn't isolate single-model self-critique effectiveness.

### Our Novel Contribution
We directly measure how much a single LLM improves its own stories through iterative self-critique, across multiple refinement depths (0-3 iterations) and selection strategies (Best-of-N). We use blind LLM-as-judge evaluation with multi-dimensional rubrics to quantify improvement and detect reward hacking (length inflation, style collapse).

### Experiment Justification
- **Experiment 1 (Self-Refine iterations)**: Tests whether iterative self-critique yields monotonic improvement or hits diminishing returns / reward hacking.
- **Experiment 2 (Best-of-N self-selection)**: Tests whether self-ranking multiple generations is more effective than iterative refinement.
- **Experiment 3 (Reward hacking analysis)**: Measures whether self-critique introduces systematic biases (length, verbosity, cliché).

## Research Question
Can an LLM significantly improve its story writing quality by self-critiquing its own output, and how does improvement scale with iteration depth?

## Hypothesis Decomposition
- H1: Self-critique + revision produces stories rated higher than baseline by blind judges.
- H2: Multiple iterations yield diminishing returns (improvement plateaus or reverses).
- H3: Self-critique introduces reward hacking artifacts (length inflation, reduced diversity).
- H4: Best-of-N self-selection is competitive with iterative refinement.

## Proposed Methodology

### Approach
Use GPT-4.1 via OpenAI API for both generation and self-critique. Evaluate with GPT-4.1 as blind pairwise judge (separate context). Use 30 diverse writing prompts from WritingPrompts dataset.

### Experimental Conditions
1. **Baseline**: Direct story generation (temperature=0.8)
2. **Self-Refine x1**: Generate → structured critique → revise
3. **Self-Refine x2**: Two critique-revise iterations
4. **Self-Refine x3**: Three critique-revise iterations
5. **Best-of-4**: Generate 4 stories, self-rank, select best
6. **Best-of-4 + Refine**: Best-of-4, then one refinement pass

### Critique Rubric (HANNA-inspired)
Six dimensions scored 1-5:
- **Coherence**: Plot logic and consistency
- **Creativity**: Originality of ideas and narrative choices
- **Engagement**: How compelling and readable the story is
- **Character**: Depth and believability of characters
- **Prose Quality**: Writing craft, imagery, voice
- **Emotional Impact**: Ability to evoke feelings

### Baselines
- Direct generation (no critique) as primary baseline
- Human-written stories from WritingPrompts as reference ceiling

### Evaluation Metrics
1. **Blind pairwise comparison**: Win rate of each condition vs baseline
2. **Multi-criteria scoring**: 6-dimension rubric scores (1-5 scale)
3. **Reward hacking indicators**: Word count, distinct-n-gram ratios, vocabulary richness

### Statistical Analysis Plan
- Paired Wilcoxon signed-rank tests for pairwise comparisons
- Bonferroni correction for multiple comparisons
- Effect sizes via rank-biserial correlation
- Bootstrap 95% confidence intervals

## Expected Outcomes
- H1 supported: ~60-70% win rate for Self-Refine x1 vs baseline
- H2 supported: Improvement plateaus around 2 iterations
- H3 partially supported: Length increases 20-40% across iterations
- H4: Best-of-N competitive with Self-Refine x1

## Timeline
- Phase 1 (Planning): 15 min ✓
- Phase 2 (Setup): 10 min
- Phase 3 (Implementation): 30 min
- Phase 4 (Experiments): 60-90 min (API calls)
- Phase 5 (Analysis): 30 min
- Phase 6 (Documentation): 20 min

## Potential Challenges
- API rate limits → batch with delays
- Cost (~$30-50 for full experiment) → monitor token usage
- Self-critique may be model-specific → document as limitation
- Blind judge may share biases with generator → use different temperature/system prompt

## Success Criteria
Research succeeds if we can quantify the improvement (or lack thereof) from self-critique with statistical confidence and identify the optimal number of iterations.
