# Is Self-Critique Enough to Get Good AI Story Writers?

An empirical study testing whether LLMs can significantly improve their story writing through self-critique, using GPT-4.1 as both writer and critic with blind pairwise evaluation.

## Key Findings

- **Self-critique works remarkably well**: One critique-revise cycle achieves an **80% win rate** over uncritiqued baselines (p < 0.001, Cohen's d = 2.02)
- **One iteration is optimal**: Additional iterations yield diminishing returns; the third iteration shows slight quality decline
- **Creativity benefits most**: Largest improvements in creativity (+0.93) and character development (+0.87) on a 5-point scale
- **Self-selection without critique is ineffective**: Best-of-4 sampling achieves only 60% win rate (near chance), showing the critique-revise loop — not generation diversity — drives improvement
- **Minimal reward hacking**: Only 11% word count increase with improved vocabulary diversity, unlike the 2.3× inflation reported in prior work

## Project Structure

```
├── REPORT.md              # Full research report with results and analysis
├── planning.md            # Research plan and hypothesis decomposition
├── literature_review.md   # Comprehensive literature review (23 papers)
├── resources.md           # Catalog of datasets, papers, and code
├── src/
│   ├── experiment.py      # Main experiment (async, concurrent API calls)
│   └── analyze.py         # Statistical analysis and visualization
├── results/
│   ├── full_results.json  # Complete experiment data
│   ├── analysis.json      # Computed statistics
│   └── plots/             # Visualizations (win rates, heatmaps, etc.)
├── datasets/              # WritingPrompts, HANNA, ROCStories, etc.
├── papers/                # 23 downloaded research papers
└── code/                  # Baseline implementations (Self-Refine, CRITICS, etc.)
```

## Reproduce

```bash
# Setup
uv venv && source .venv/bin/activate
uv add openai numpy scipy matplotlib seaborn

# Set API key
export OPENAI_API_KEY=your_key

# Run experiment (~20 min, ~$15-25 API cost)
python src/experiment.py

# Run analysis
python src/analyze.py
```

## Full Report

See [REPORT.md](REPORT.md) for complete methodology, results, and discussion.
