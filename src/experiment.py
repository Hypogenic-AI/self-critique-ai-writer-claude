"""
Self-Critique Story Writing Experiment
Tests whether LLMs can improve story quality through iterative self-critique.
Uses async concurrency to speed up API calls.
"""

import json
import os
import random
import asyncio
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from openai import AsyncOpenAI

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

MODEL = "gpt-4.1"
JUDGE_MODEL = "gpt-4.1"
TEMPERATURE = 0.8
JUDGE_TEMPERATURE = 0.3
MAX_STORY_TOKENS = 800
NUM_PROMPTS = 15
BEST_OF_N = 4
MAX_REFINE_ITERATIONS = 3
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)
CONCURRENCY = 5  # Max concurrent API calls

client = AsyncOpenAI()
semaphore = asyncio.Semaphore(CONCURRENCY)

RUBRIC_DIMENSIONS = [
    "Coherence", "Creativity", "Engagement",
    "Character", "Prose Quality", "Emotional Impact"
]

# ──────────────────────────────────────────────────────────────────────
# Prompt Templates
# ──────────────────────────────────────────────────────────────────────

STORY_SYSTEM = """You are a skilled fiction writer. Write a compelling short story (400-600 words) based on the given prompt. Focus on vivid prose, engaging characters, and a satisfying narrative arc. Do not include any meta-commentary — just write the story."""

CRITIQUE_SYSTEM = """You are a thoughtful literary critic. Provide specific, actionable feedback on the story below. Evaluate each dimension on a 1-5 scale and give concrete suggestions for improvement.

Dimensions:
- Coherence (1-5): Plot logic, internal consistency, and narrative flow
- Creativity (1-5): Originality of ideas, premise, and narrative choices
- Engagement (1-5): How compelling, readable, and page-turning the story is
- Character (1-5): Depth, believability, and distinctiveness of characters
- Prose Quality (1-5): Writing craft, imagery, word choice, and voice
- Emotional Impact (1-5): Ability to evoke genuine feelings in the reader

Format your response as:
SCORES: Coherence=X, Creativity=X, Engagement=X, Character=X, Prose Quality=X, Emotional Impact=X
OVERALL: X/5

STRENGTHS:
[2-3 specific strengths]

WEAKNESSES:
[2-3 specific weaknesses with actionable suggestions]"""

REVISE_SYSTEM = """You are a skilled fiction writer revising your own story based on feedback. Rewrite the story to address the critique while preserving what works well. Write the full revised story (400-600 words). Do not include any meta-commentary — just write the revised story."""

RANK_SYSTEM = """You are a literary critic ranking stories. Given multiple stories written for the same prompt, rank them from best to worst. Consider coherence, creativity, engagement, character depth, prose quality, and emotional impact.

Respond with ONLY a JSON array of indices (0-based) from best to worst. Example: [2, 0, 3, 1]"""

JUDGE_SYSTEM = """You are an expert literary judge conducting a blind evaluation. You will compare two stories written for the same prompt. Judge ONLY on literary merit — do not favor longer stories or more elaborate vocabulary for their own sake.

Evaluate on these dimensions (1-5 each):
- Coherence: Plot logic, internal consistency, narrative flow
- Creativity: Originality of ideas, premise, narrative choices
- Engagement: How compelling and readable
- Character: Depth and believability
- Prose Quality: Writing craft, imagery, voice
- Emotional Impact: Ability to evoke feelings

Respond in this exact format:
STORY_A_SCORES: Coherence=X, Creativity=X, Engagement=X, Character=X, Prose Quality=X, Emotional Impact=X
STORY_B_SCORES: Coherence=X, Creativity=X, Engagement=X, Character=X, Prose Quality=X, Emotional Impact=X
WINNER: A or B or TIE
REASONING: [1-2 sentences explaining your choice]"""


# ──────────────────────────────────────────────────────────────────────
# API Helpers
# ──────────────────────────────────────────────────────────────────────

async def call_llm(system: str, user: str, temperature: float = TEMPERATURE,
                   max_tokens: int = MAX_STORY_TOKENS, seed: int = SEED) -> str:
    """Call OpenAI API with concurrency control and retry."""
    async with semaphore:
        for attempt in range(3):
            try:
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    seed=seed,
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
                else:
                    print(f"  API error after 3 attempts: {e}")
                    return ""
    return ""


async def call_judge(system: str, user: str) -> str:
    """Call judge model."""
    async with semaphore:
        for attempt in range(3):
            try:
                response = await client.chat.completions.create(
                    model=JUDGE_MODEL,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=JUDGE_TEMPERATURE,
                    max_tokens=600,
                    seed=SEED + 1000,
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
                else:
                    return ""
    return ""


# ──────────────────────────────────────────────────────────────────────
# Story Generation Pipelines
# ──────────────────────────────────────────────────────────────────────

async def generate_story(prompt: str, seed_offset: int = 0) -> str:
    return await call_llm(STORY_SYSTEM, f"Writing prompt: {prompt}", seed=SEED + seed_offset)


async def critique_story(prompt: str, story: str) -> str:
    user_msg = f"Writing prompt: {prompt}\n\nStory to critique:\n{story}"
    return await call_llm(CRITIQUE_SYSTEM, user_msg, temperature=0.4, max_tokens=500)


async def revise_story(prompt: str, story: str, critique: str) -> str:
    user_msg = (
        f"Writing prompt: {prompt}\n\n"
        f"Original story:\n{story}\n\n"
        f"Critique and feedback:\n{critique}\n\n"
        f"Please rewrite the story addressing the feedback."
    )
    return await call_llm(REVISE_SYSTEM, user_msg)


async def self_refine(prompt: str, iterations: int = 1) -> dict:
    """Generate → critique → revise for N iterations (sequential by nature)."""
    story = await generate_story(prompt, seed_offset=iterations * 100)
    history = [{"iteration": 0, "story": story}]

    for i in range(iterations):
        critique = await critique_story(prompt, story)
        revised = await revise_story(prompt, story, critique)
        history.append({"iteration": i + 1, "story": revised, "critique": critique})
        story = revised

    return {"final_story": story, "history": history}


async def best_of_n(prompt: str, n: int = BEST_OF_N) -> dict:
    """Generate N stories concurrently, self-rank, return best."""
    # Generate all N stories concurrently
    tasks = [generate_story(prompt, seed_offset=200 + i) for i in range(n)]
    stories = await asyncio.gather(*tasks)

    # Self-rank
    stories_text = "\n\n---\n\n".join(f"STORY {i}:\n{s}" for i, s in enumerate(stories))
    user_msg = f"Writing prompt: {prompt}\n\n{stories_text}"
    ranking_response = await call_llm(RANK_SYSTEM, user_msg, temperature=0.3, max_tokens=100)

    try:
        match = re.search(r'\[[\d,\s]+\]', ranking_response)
        best_idx = json.loads(match.group())[0] if match else 0
    except (json.JSONDecodeError, IndexError):
        best_idx = 0

    return {"final_story": stories[best_idx], "all_stories": stories,
            "ranking": ranking_response, "best_idx": best_idx}


async def best_of_n_plus_refine(prompt: str, n: int = BEST_OF_N) -> dict:
    """Best-of-N followed by one refinement pass."""
    bon = await best_of_n(prompt, n)
    critique = await critique_story(prompt, bon["final_story"])
    revised = await revise_story(prompt, bon["final_story"], critique)
    return {"final_story": revised, "critique": critique, "bon_result": bon}


# ──────────────────────────────────────────────────────────────────────
# Text Metrics
# ──────────────────────────────────────────────────────────────────────

def compute_text_metrics(text: str) -> dict:
    words = text.split()
    word_count = len(words)
    lower_words = [w.lower().strip(".,!?;:'\"") for w in words]

    def distinct_n(tokens, n):
        ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
        return len(set(ngrams)) / max(len(ngrams), 1)

    return {
        "word_count": word_count,
        "char_count": len(text),
        "unique_words": len(set(lower_words)),
        "vocab_richness": len(set(lower_words)) / max(word_count, 1),
        "distinct_1": distinct_n(lower_words, 1),
        "distinct_2": distinct_n(lower_words, 2),
        "distinct_3": distinct_n(lower_words, 3),
        "avg_word_length": float(np.mean([len(w) for w in words])) if words else 0,
        "avg_sentence_length": word_count / max(text.count('.') + text.count('!') + text.count('?'), 1),
    }


# ──────────────────────────────────────────────────────────────────────
# Evaluation
# ──────────────────────────────────────────────────────────────────────

def parse_judge_scores(response: str) -> dict:
    result = {"raw": response, "winner": None, "a_scores": {}, "b_scores": {}}

    winner_match = re.search(r'WINNER:\s*(A|B|TIE)', response, re.IGNORECASE)
    if winner_match:
        result["winner"] = winner_match.group(1).upper()

    for prefix, key in [("STORY_A_SCORES:", "a_scores"), ("STORY_B_SCORES:", "b_scores")]:
        line_match = re.search(rf'{prefix}.*', response)
        if line_match:
            line = line_match.group()
            for dim in RUBRIC_DIMENSIONS:
                score_match = re.search(rf'{dim}\s*=\s*(\d)', line)
                if score_match:
                    result[key][dim] = int(score_match.group(1))

    return result


async def judge_pairwise(prompt: str, story_a: str, story_b: str) -> dict:
    user_msg = f"Writing prompt: {prompt}\n\n=== STORY A ===\n{story_a}\n\n=== STORY B ===\n{story_b}"
    response = await call_judge(JUDGE_SYSTEM, user_msg)
    return parse_judge_scores(response)


# ──────────────────────────────────────────────────────────────────────
# Main Experiment
# ──────────────────────────────────────────────────────────────────────

def load_prompts(n: int = NUM_PROMPTS) -> list:
    with open("datasets/writingprompts/train_subset.json") as f:
        data = json.load(f)
    candidates = [d["prompt"] for d in data if 30 < len(d["prompt"]) < 300]
    random.seed(SEED)
    return random.sample(candidates, min(n, len(candidates)))


async def process_prompt(pi: int, prompt: str, total: int) -> dict:
    """Process all conditions for a single prompt."""
    print(f"\n[Prompt {pi+1}/{total}] {prompt[:70]}...")

    # Run all conditions concurrently where possible
    # Baseline, best_of_4 can run in parallel
    # Self-refine iterations are sequential internally but can run in parallel with each other
    baseline_task = generate_story(prompt)
    sr1_task = self_refine(prompt, 1)
    sr2_task = self_refine(prompt, 2)
    sr3_task = self_refine(prompt, 3)
    bon_task = best_of_n(prompt, BEST_OF_N)

    baseline, sr1, sr2, sr3, bon = await asyncio.gather(
        baseline_task, sr1_task, sr2_task, sr3_task, bon_task
    )

    # Best-of-4+Refine depends on bon result, but we can start it now
    critique = await critique_story(prompt, bon["final_story"])
    revised = await revise_story(prompt, bon["final_story"], critique)
    bonr = {"final_story": revised, "critique": critique, "bon_result": bon}

    prompt_results = {
        "prompt_idx": pi, "prompt": prompt,
        "conditions": {
            "baseline": {"final_story": baseline, "metrics": compute_text_metrics(baseline)},
            "refine_x1": {"final_story": sr1["final_story"], "history": sr1["history"],
                          "metrics": compute_text_metrics(sr1["final_story"])},
            "refine_x2": {"final_story": sr2["final_story"], "history": sr2["history"],
                          "metrics": compute_text_metrics(sr2["final_story"])},
            "refine_x3": {"final_story": sr3["final_story"], "history": sr3["history"],
                          "metrics": compute_text_metrics(sr3["final_story"])},
            "best_of_4": {"final_story": bon["final_story"], "ranking": bon["ranking"],
                          "best_idx": bon["best_idx"],
                          "metrics": compute_text_metrics(bon["final_story"])},
            "best_of_4_refine": {"final_story": bonr["final_story"], "critique": bonr["critique"],
                                  "metrics": compute_text_metrics(bonr["final_story"])},
        }
    }
    print(f"  [Prompt {pi+1}] Generation complete")
    return prompt_results


async def evaluate_prompt(pi: int, gen: dict, total: int) -> dict:
    """Evaluate all conditions for a prompt against baseline."""
    print(f"  Evaluating prompt {pi+1}/{total}...")
    baseline_story = gen["conditions"]["baseline"]["final_story"]
    prompt = gen["prompt"]
    eval_conditions = ["refine_x1", "refine_x2", "refine_x3", "best_of_4", "best_of_4_refine"]

    prompt_evals = {"prompt_idx": pi}

    # Run all evaluations concurrently
    async def eval_one(cond):
        cond_story = gen["conditions"][cond]["final_story"]
        # Randomize order to avoid position bias
        random.seed(SEED + pi * 10 + hash(cond) % 100)
        if random.random() < 0.5:
            jr = await judge_pairwise(prompt, baseline_story, cond_story)
            order = "baseline_first"
            if jr["winner"] == "B":
                winner = cond
            elif jr["winner"] == "A":
                winner = "baseline"
            else:
                winner = "tie"
            jr["baseline_scores"] = jr.pop("a_scores", {})
            jr["condition_scores"] = jr.pop("b_scores", {})
        else:
            jr = await judge_pairwise(prompt, cond_story, baseline_story)
            order = "condition_first"
            if jr["winner"] == "A":
                winner = cond
            elif jr["winner"] == "B":
                winner = "baseline"
            else:
                winner = "tie"
            jr["baseline_scores"] = jr.pop("b_scores", {})
            jr["condition_scores"] = jr.pop("a_scores", {})

        jr["order"] = order
        jr["winner_label"] = winner
        return cond, jr

    tasks = [eval_one(c) for c in eval_conditions]
    eval_results = await asyncio.gather(*tasks)

    for cond, jr in eval_results:
        prompt_evals[cond] = jr

    return prompt_evals


async def run_experiment():
    prompts = load_prompts(NUM_PROMPTS)
    print(f"Loaded {len(prompts)} writing prompts")
    print(f"Model: {MODEL}, Concurrency: {CONCURRENCY}")

    results = {
        "config": {
            "model": MODEL, "judge_model": JUDGE_MODEL,
            "temperature": TEMPERATURE, "judge_temperature": JUDGE_TEMPERATURE,
            "max_story_tokens": MAX_STORY_TOKENS, "num_prompts": len(prompts),
            "best_of_n": BEST_OF_N, "max_refine_iterations": MAX_REFINE_ITERATIONS,
            "seed": SEED, "timestamp": datetime.now().isoformat(),
        },
        "prompts": prompts,
        "generations": [],
        "evaluations": [],
    }

    # Phase 1: Generate stories (process 3 prompts concurrently)
    print("\n" + "=" * 60)
    print("GENERATION PHASE")
    print("=" * 60)

    # Process in batches of 3 prompts
    batch_size = 3
    for batch_start in range(0, len(prompts), batch_size):
        batch = list(range(batch_start, min(batch_start + batch_size, len(prompts))))
        tasks = [process_prompt(i, prompts[i], len(prompts)) for i in batch]
        batch_results = await asyncio.gather(*tasks)
        results["generations"].extend(batch_results)

        # Save incrementally
        with open(RESULTS_DIR / "generations.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"  Batch {batch_start // batch_size + 1} saved ({len(results['generations'])}/{len(prompts)} prompts)")

    # Phase 2: Evaluate
    print("\n" + "=" * 60)
    print("EVALUATION PHASE")
    print("=" * 60)

    for batch_start in range(0, len(results["generations"]), batch_size):
        batch = results["generations"][batch_start:batch_start + batch_size]
        tasks = [evaluate_prompt(g["prompt_idx"], g, len(prompts)) for g in batch]
        batch_evals = await asyncio.gather(*tasks)
        results["evaluations"].extend(batch_evals)

        with open(RESULTS_DIR / "full_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

    print("\nExperiment complete!")
    return results


if __name__ == "__main__":
    results = asyncio.run(run_experiment())
    print(f"\nResults saved to {RESULTS_DIR}")
