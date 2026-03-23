"""
Analysis script for self-critique story writing experiment.
Produces statistics, visualizations, and summary tables.
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_DIR = Path("results")
PLOTS_DIR = RESULTS_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

RUBRIC_DIMENSIONS = [
    "Coherence", "Creativity", "Engagement",
    "Character", "Prose Quality", "Emotional Impact"
]

CONDITION_LABELS = {
    "refine_x1": "Self-Refine ×1",
    "refine_x2": "Self-Refine ×2",
    "refine_x3": "Self-Refine ×3",
    "best_of_4": "Best-of-4",
    "best_of_4_refine": "Best-of-4 + Refine",
}


def load_results():
    with open(RESULTS_DIR / "full_results.json") as f:
        return json.load(f)


def compute_win_rates(results):
    """Compute win rates for each condition vs baseline."""
    eval_conditions = list(CONDITION_LABELS.keys())
    win_rates = {}

    for cond in eval_conditions:
        wins, losses, ties = 0, 0, 0
        for ev in results["evaluations"]:
            if cond not in ev:
                continue
            w = ev[cond].get("winner_label", "tie")
            if w == cond:
                wins += 1
            elif w == "baseline":
                losses += 1
            else:
                ties += 1
        total = wins + losses + ties
        win_rates[cond] = {
            "wins": wins, "losses": losses, "ties": ties, "total": total,
            "win_rate": wins / max(total, 1),
            "loss_rate": losses / max(total, 1),
            "tie_rate": ties / max(total, 1),
        }

    return win_rates


def compute_score_differences(results):
    """Compute score differences (condition - baseline) per dimension."""
    eval_conditions = list(CONDITION_LABELS.keys())
    diffs = {cond: {dim: [] for dim in RUBRIC_DIMENSIONS} for cond in eval_conditions}

    for ev in results["evaluations"]:
        for cond in eval_conditions:
            if cond not in ev:
                continue
            b_scores = ev[cond].get("baseline_scores", {})
            c_scores = ev[cond].get("condition_scores", {})
            for dim in RUBRIC_DIMENSIONS:
                if dim in b_scores and dim in c_scores:
                    diffs[cond][dim].append(c_scores[dim] - b_scores[dim])

    return diffs


def compute_text_metric_comparison(results):
    """Compare text metrics across conditions."""
    conditions = ["baseline", "refine_x1", "refine_x2", "refine_x3", "best_of_4", "best_of_4_refine"]
    metrics_by_cond = {c: [] for c in conditions}

    for gen in results["generations"]:
        for cond in conditions:
            if cond in gen["conditions"]:
                metrics_by_cond[cond].append(gen["conditions"][cond]["metrics"])

    summary = {}
    for cond in conditions:
        if not metrics_by_cond[cond]:
            continue
        metric_keys = metrics_by_cond[cond][0].keys()
        summary[cond] = {}
        for mk in metric_keys:
            values = [m[mk] for m in metrics_by_cond[cond]]
            summary[cond][mk] = {
                "mean": np.mean(values),
                "std": np.std(values),
                "median": np.median(values),
            }

    return summary


def statistical_tests(results):
    """Run paired statistical tests for each condition vs baseline."""
    eval_conditions = list(CONDITION_LABELS.keys())
    test_results = {}

    for cond in eval_conditions:
        cond_total_scores = []
        base_total_scores = []

        for ev in results["evaluations"]:
            if cond not in ev:
                continue
            b = ev[cond].get("baseline_scores", {})
            c = ev[cond].get("condition_scores", {})
            if b and c:
                b_avg = np.mean([b.get(d, 3) for d in RUBRIC_DIMENSIONS])
                c_avg = np.mean([c.get(d, 3) for d in RUBRIC_DIMENSIONS])
                base_total_scores.append(b_avg)
                cond_total_scores.append(c_avg)

        if len(cond_total_scores) >= 5:
            # Wilcoxon signed-rank test
            try:
                stat, p_val = stats.wilcoxon(cond_total_scores, base_total_scores, alternative='two-sided')
            except ValueError:
                stat, p_val = 0, 1.0

            diff = np.array(cond_total_scores) - np.array(base_total_scores)
            effect_size = np.mean(diff) / max(np.std(diff), 0.001)  # Cohen's d analog

            # Bootstrap CI
            boot_means = []
            for _ in range(1000):
                idx = np.random.choice(len(diff), len(diff), replace=True)
                boot_means.append(np.mean(diff[idx]))
            ci_lower, ci_upper = np.percentile(boot_means, [2.5, 97.5])

            test_results[cond] = {
                "n": len(cond_total_scores),
                "mean_diff": float(np.mean(diff)),
                "std_diff": float(np.std(diff)),
                "wilcoxon_stat": float(stat),
                "p_value": float(p_val),
                "effect_size_d": float(effect_size),
                "ci_95_lower": float(ci_lower),
                "ci_95_upper": float(ci_upper),
                "cond_mean": float(np.mean(cond_total_scores)),
                "base_mean": float(np.mean(base_total_scores)),
            }

    return test_results


# ──────────────────────────────────────────────────────────────────────
# Visualizations
# ──────────────────────────────────────────────────────────────────────

def plot_win_rates(win_rates):
    """Bar chart of win/tie/loss rates."""
    fig, ax = plt.subplots(figsize=(10, 5))
    conditions = list(CONDITION_LABELS.keys())
    labels = [CONDITION_LABELS[c] for c in conditions]
    wins = [win_rates[c]["win_rate"] * 100 for c in conditions]
    ties = [win_rates[c]["tie_rate"] * 100 for c in conditions]
    losses = [win_rates[c]["loss_rate"] * 100 for c in conditions]

    x = np.arange(len(labels))
    width = 0.25

    ax.bar(x - width, wins, width, label="Win vs Baseline", color="#2ecc71")
    ax.bar(x, ties, width, label="Tie", color="#95a5a6")
    ax.bar(x + width, losses, width, label="Loss vs Baseline", color="#e74c3c")

    ax.set_ylabel("Percentage (%)")
    ax.set_title("Win Rate vs Baseline (Blind Pairwise Judging)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.legend()
    ax.set_ylim(0, 100)
    for i, (w, t, l) in enumerate(zip(wins, ties, losses)):
        ax.text(i - width, w + 1, f"{w:.0f}%", ha="center", fontsize=8)
        ax.text(i + width, l + 1, f"{l:.0f}%", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "win_rates.png", dpi=150)
    plt.close()
    print(f"  Saved {PLOTS_DIR / 'win_rates.png'}")


def plot_score_differences(diffs):
    """Heatmap of mean score differences by condition and dimension."""
    conditions = list(CONDITION_LABELS.keys())
    labels = [CONDITION_LABELS[c] for c in conditions]

    matrix = np.zeros((len(conditions), len(RUBRIC_DIMENSIONS)))
    for i, cond in enumerate(conditions):
        for j, dim in enumerate(RUBRIC_DIMENSIONS):
            vals = diffs[cond][dim]
            matrix[i, j] = np.mean(vals) if vals else 0

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        matrix, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
        xticklabels=RUBRIC_DIMENSIONS, yticklabels=labels,
        vmin=-1.5, vmax=1.5, ax=ax
    )
    ax.set_title("Mean Score Difference vs Baseline (Condition − Baseline)")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "score_diffs_heatmap.png", dpi=150)
    plt.close()
    print(f"  Saved {PLOTS_DIR / 'score_diffs_heatmap.png'}")


def plot_text_metrics(text_summary):
    """Plot word count and diversity metrics across conditions."""
    conditions = ["baseline", "refine_x1", "refine_x2", "refine_x3", "best_of_4", "best_of_4_refine"]
    labels = ["Baseline", "Refine ×1", "Refine ×2", "Refine ×3", "Best-of-4", "BoN+Refine"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Word count
    means = [text_summary[c]["word_count"]["mean"] for c in conditions if c in text_summary]
    stds = [text_summary[c]["word_count"]["std"] for c in conditions if c in text_summary]
    axes[0].bar(labels[:len(means)], means, yerr=stds, color="#3498db", alpha=0.8, capsize=3)
    axes[0].set_title("Word Count by Condition")
    axes[0].set_ylabel("Words")
    axes[0].tick_params(axis='x', rotation=30)

    # Vocabulary richness
    means = [text_summary[c]["vocab_richness"]["mean"] for c in conditions if c in text_summary]
    axes[1].bar(labels[:len(means)], means, color="#e67e22", alpha=0.8)
    axes[1].set_title("Vocabulary Richness (Unique/Total)")
    axes[1].set_ylabel("Ratio")
    axes[1].tick_params(axis='x', rotation=30)

    # Distinct-2
    means = [text_summary[c]["distinct_2"]["mean"] for c in conditions if c in text_summary]
    axes[2].bar(labels[:len(means)], means, color="#9b59b6", alpha=0.8)
    axes[2].set_title("Distinct-2 (Bigram Diversity)")
    axes[2].set_ylabel("Ratio")
    axes[2].tick_params(axis='x', rotation=30)

    plt.suptitle("Reward Hacking Indicators", fontsize=14)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "text_metrics.png", dpi=150)
    plt.close()
    print(f"  Saved {PLOTS_DIR / 'text_metrics.png'}")


def plot_iteration_trajectory(results):
    """Plot how self-critique scores evolve across refinement iterations."""
    # Collect per-iteration scores from self-critique history
    conditions = ["baseline", "refine_x1", "refine_x2", "refine_x3"]
    cond_labels = ["Iter 0\n(Baseline)", "Iter 1\n(Refine ×1)", "Iter 2\n(Refine ×2)", "Iter 3\n(Refine ×3)"]

    # Use judge scores averaged across dimensions
    scores_per_iter = {c: [] for c in conditions}
    for ev in results["evaluations"]:
        for cond in ["refine_x1", "refine_x2", "refine_x3"]:
            if cond in ev:
                c_scores = ev[cond].get("condition_scores", {})
                if c_scores:
                    avg = np.mean([c_scores.get(d, 3) for d in RUBRIC_DIMENSIONS])
                    scores_per_iter[cond].append(avg)
                b_scores = ev[cond].get("baseline_scores", {})
                if b_scores and cond == "refine_x1":  # Use baseline scores from first comparison
                    avg = np.mean([b_scores.get(d, 3) for d in RUBRIC_DIMENSIONS])
                    scores_per_iter["baseline"].append(avg)

    fig, ax = plt.subplots(figsize=(8, 5))
    means = []
    stds = []
    for c in conditions:
        vals = scores_per_iter[c]
        if vals:
            means.append(np.mean(vals))
            stds.append(np.std(vals) / np.sqrt(len(vals)))
        else:
            means.append(0)
            stds.append(0)

    ax.errorbar(range(len(conditions)), means, yerr=stds, marker='o', linewidth=2,
                markersize=8, capsize=5, color="#2c3e50")
    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(cond_labels)
    ax.set_ylabel("Mean Judge Score (1-5)")
    ax.set_title("Story Quality Across Self-Critique Iterations")
    ax.set_ylim(1, 5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "iteration_trajectory.png", dpi=150)
    plt.close()
    print(f"  Saved {PLOTS_DIR / 'iteration_trajectory.png'}")


def generate_summary_table(win_rates, test_results, text_summary):
    """Generate markdown summary table."""
    lines = ["## Summary Results Table\n"]
    lines.append("| Condition | Win% | Tie% | Loss% | Mean Δ Score | p-value | Effect Size (d) | Mean Words |")
    lines.append("|-----------|------|------|-------|-------------|---------|----------------|------------|")

    for cond, label in CONDITION_LABELS.items():
        wr = win_rates.get(cond, {})
        tr = test_results.get(cond, {})
        ts = text_summary.get(cond, {}).get("word_count", {})

        win_pct = f"{wr.get('win_rate', 0)*100:.0f}%"
        tie_pct = f"{wr.get('tie_rate', 0)*100:.0f}%"
        loss_pct = f"{wr.get('loss_rate', 0)*100:.0f}%"
        mean_diff = f"{tr.get('mean_diff', 0):+.2f}"
        p_val = f"{tr.get('p_value', 1):.3f}"
        effect = f"{tr.get('effect_size_d', 0):.2f}"
        words = f"{ts.get('mean', 0):.0f}"

        lines.append(f"| {label} | {win_pct} | {tie_pct} | {loss_pct} | {mean_diff} | {p_val} | {effect} | {words} |")

    # Add baseline row
    baseline_words = text_summary.get("baseline", {}).get("word_count", {}).get("mean", 0)
    lines.append(f"| Baseline | — | — | — | 0.00 | — | — | {baseline_words:.0f} |")

    return "\n".join(lines)


def run_analysis():
    """Run full analysis pipeline."""
    print("Loading results...")
    results = load_results()

    print("Computing win rates...")
    win_rates = compute_win_rates(results)
    for cond, wr in win_rates.items():
        print(f"  {CONDITION_LABELS[cond]}: {wr['win_rate']*100:.0f}% win, "
              f"{wr['tie_rate']*100:.0f}% tie, {wr['loss_rate']*100:.0f}% loss")

    print("\nComputing score differences...")
    diffs = compute_score_differences(results)

    print("Computing text metrics...")
    text_summary = compute_text_metric_comparison(results)

    print("Running statistical tests...")
    test_results = statistical_tests(results)
    for cond, tr in test_results.items():
        sig = "***" if tr["p_value"] < 0.001 else "**" if tr["p_value"] < 0.01 else "*" if tr["p_value"] < 0.05 else "ns"
        print(f"  {CONDITION_LABELS[cond]}: Δ={tr['mean_diff']:+.2f}, p={tr['p_value']:.4f} {sig}, d={tr['effect_size_d']:.2f}")

    print("\nGenerating plots...")
    plot_win_rates(win_rates)
    plot_score_differences(diffs)
    plot_text_metrics(text_summary)
    plot_iteration_trajectory(results)

    print("\nGenerating summary table...")
    summary_table = generate_summary_table(win_rates, test_results, text_summary)
    print(summary_table)

    # Save analysis results
    analysis = {
        "win_rates": win_rates,
        "test_results": test_results,
        "text_metrics": text_summary,
        "summary_table": summary_table,
    }
    with open(RESULTS_DIR / "analysis.json", "w") as f:
        json.dump(analysis, f, indent=2, default=str)

    print(f"\nAnalysis complete. Results saved to {RESULTS_DIR}")
    return analysis


if __name__ == "__main__":
    run_analysis()
