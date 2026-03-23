# Datasets for "Is Self-Critique Enough to Get Good AI Story Writers?"

This directory contains subsets and samples of datasets used for training and evaluating LLM story generation quality.

## Directory Structure

```
datasets/
├── writingprompts/       # Reddit writing prompts + stories (5000 examples)
├── tinystories/          # TinyStories short stories (5000 examples)
├── rocstories/           # Story Cloze Test / ROCStories (1000 examples)
├── hanna/                # HANNA human-annotated story evaluation benchmark
└── openmeva/             # OpenMEVA story generation evaluation benchmark
```

---

## 1. WritingPrompts

**Source:** `euclaise/writingprompts` on HuggingFace
**Paper:** Fan et al. (2018), "Hierarchical Neural Story Generation"
**Size downloaded:** 5000 examples (subset of full training split)

**Schema:**
- `prompt` (str): Reddit writing prompt (e.g., "[ WP ] You've finally managed to discover the secret to immortality...")
- `story` (str): Community-written story response

**Files:**
- `train_subset.json` — 5000 prompt/story pairs
- `samples.json` — first 10 examples for quick inspection

**Load in Python:**
```python
import json
with open("datasets/writingprompts/train_subset.json") as f:
    data = json.load(f)
# Or stream fresh from HuggingFace:
from datasets import load_dataset
ds = load_dataset("euclaise/writingprompts", split="train", streaming=True)
```

**Use in research:** Primary source of creative writing prompts and human-written story pairs. Useful for prompt-conditioned generation and evaluating whether self-critique improves story quality.

---

## 2. TinyStories

**Source:** `roneneldan/TinyStories` on HuggingFace
**Paper:** Eldan & Li (2023), "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?"
**Size downloaded:** 5000 examples (subset of training split)

**Schema:**
- `text` (str): Short story (typically 200–500 words, written at child reading level)

**Files:**
- `train_subset.json` — 5000 stories
- `samples.json` — first 10 examples

**Load in Python:**
```python
import json
with open("datasets/tinystories/train_subset.json") as f:
    data = json.load(f)
# Or from HuggingFace:
from datasets import load_dataset
ds = load_dataset("roneneldan/TinyStories", split="train", streaming=True)
```

**Use in research:** Baseline reference for coherent short story generation. Useful as a lower-complexity benchmark to test whether self-critique adds value on simpler narratives.

---

## 3. ROCStories / Story Cloze Test

**Source:** `gimmaru/story_cloze-2016` on HuggingFace
**Paper:** Mostafazadeh et al. (2016), "A Corpus and Evaluation Framework for Deeper Understanding of Commonsense Stories"
**Size downloaded:** 1000 examples (full test split)

**Schema:**
- `story_id` (str): Unique story identifier
- `input_sentence_1` through `input_sentence_4` (str): Four story context sentences
- `sentence_quiz1`, `sentence_quiz2` (str): Two candidate story endings
- `answer_right_ending` (int): 1 or 2, indicating which ending is correct

**Files:**
- `subset.json` — 1000 story cloze examples
- `samples.json` — first 10 examples

**Load in Python:**
```python
import json
with open("datasets/rocstories/subset.json") as f:
    data = json.load(f)
# Or from HuggingFace:
from datasets import load_dataset
ds = load_dataset("gimmaru/story_cloze-2016")
```

**Note on access:** Many ROCStories variants on HuggingFace use legacy loading scripts (unsupported in recent `datasets` versions) or are gated. The `gimmaru/story_cloze-2016` repo provides a clean Parquet-based version. The original data can also be requested at: https://cs.rochester.edu/nlp/rocstories/

**Use in research:** Story coherence and commonsense understanding evaluation. Tests whether self-critique can improve narrative logical consistency and ending selection.

---

## 4. HANNA (Human-ANnotated NArratives Assessment)

**Sources:**
- Original benchmark: `dig-team/hanna-benchmark-asg` (GitHub) — 3168 human annotations
- LLM evaluation variant: `bay-calibration-llm-evaluators/hanna-annotated-latest` (HuggingFace) — 1000 examples

**Paper:** Chhun et al. (2022), "Of Human Criteria and Automatic Metrics: A Benchmark of the Evaluation of Story Generation" (COLING 2022)
**GitHub:** https://github.com/dig-team/hanna-benchmark-asg

**Schema (original `hanna_stories_annotations.csv`):**
- `Story ID` (str): Story identifier
- `Prompt` (str): Writing prompt
- `Human` (bool): Whether story was human-written
- `Story` (str): Full story text
- `Model` (str): Generating model name
- `Relevance`, `Coherence`, `Empathy`, `Surprise`, `Engagement`, `Complexity` (int, 1-5): Human annotation scores on 6 quality dimensions
- `Worker ID`, `Assignment ID`, `Work time in seconds` (str/int): Crowdwork metadata

**Schema (LLM eval variant):**
- `task` (str): Task identifier
- `worker` (str): Annotator ID
- `human_label` (int): Human preference label
- `llm_label` (int): LLM preference label
- `generator_1`, `generator_2` (str): Story generator names in comparison
- `premise` (str): Story premise

**Files:**
- `hanna_stories_annotations.csv` — full original dataset (3168 annotations of 1056 stories)
- `samples_original.json` — first 10 rows of original CSV
- `subset.json` — 1000 rows from LLM eval variant
- `samples.json` — first 10 from LLM eval variant

**Load in Python:**
```python
import csv, json

# Original HANNA (full dataset, all 3168 annotations)
with open("datasets/hanna/hanna_stories_annotations.csv") as f:
    reader = csv.DictReader(f)
    data = list(reader)

# LLM eval variant (JSON)
with open("datasets/hanna/subset.json") as f:
    llm_eval_data = json.load(f)

# Or from HuggingFace:
from datasets import load_dataset
ds = load_dataset("bay-calibration-llm-evaluators/hanna-annotated-latest")
```

**Use in research:** Primary evaluation benchmark for this project. HANNA's six quality dimensions (Relevance, Coherence, Empathy, Surprise, Engagement, Complexity) can be used as rubrics for self-critique prompts. The human scores serve as ground truth to evaluate whether self-critiqued stories score higher.

---

## 5. OpenMEVA

**Source:** `Jiann/OpenMEVA` on HuggingFace (files), originally `thu-coai/OpenMEVA` on GitHub
**Paper:** Guan et al. (2021), "OpenMEVA: A Benchmark for Evaluating Open-ended Story Generation Metrics" (ACL 2021)
**GitHub:** https://github.com/thu-coai/OpenMEVA

**Schema (flattened `subset_flat.json`):**
- `story_id` (str): Story identifier (from ROCStories or WritingPrompts)
- `model` (str): Name of generation model (e.g., `fusion`, `s2s`, `gpt2`)
- `text` (str): Generated story text
- `human_scores` (list[int]): List of 5 human quality ratings

**Files:**
- `data/mans_data/mans_roc.json` — Human annotation scores for ROCStories-based generations (200 stories, multiple models)
- `data/mans_data/mans_wp.json` — Human annotation scores for WritingPrompts-based generations
- `back_trans_data/roc_bt.json` — Back-translated ROCStories augmentation data
- `subset_flat.json` — Flattened version of mans_roc data (1000 records)
- `samples.json` — First 10 flattened records

**Load in Python:**
```python
import json

# Flattened subset (easiest to use)
with open("datasets/openmeva/subset_flat.json") as f:
    data = json.load(f)
# Each record: {story_id, model, text, human_scores}

# Original nested format
with open("datasets/openmeva/data/mans_data/mans_roc.json") as f:
    raw = json.load(f)
# raw[story_id]["gen"][model_name] = {"text": ..., "score": [int, int, int, int, int]}
```

**Use in research:** Provides human scores for stories generated by multiple models (on the same prompts), enabling direct comparison. Also provides perturbation test cases for evaluating whether automatic metrics (including self-critique) correctly rank story quality.

---

## Download Instructions for Restricted Datasets

### ROCStories (Full Training Set)
The full ROCStories training corpus (~49k 5-sentence stories) requires a request form:
1. Visit: https://cs.rochester.edu/nlp/rocstories/
2. Fill in the request form to receive a download link
3. Save to `datasets/rocstories/rocstories_winter2017.csv`

### Story Cloze Test (Official)
The official test set with labels requires LDC agreement. Easier alternatives:
- `gimmaru/story_cloze-2016` (already downloaded — test split, 1000 examples)
- `chenxwh/gen-storycloze` for generated story cloze data

### WritingPrompts (Full Dataset)
The full dataset (~300k examples) can be streamed:
```python
from datasets import load_dataset
ds = load_dataset("euclaise/writingprompts", split="train", streaming=True)
```
Or downloaded in full (warning: ~2GB):
```python
ds = load_dataset("euclaise/writingprompts")
ds.save_to_disk("datasets/writingprompts/full/")
```

### HANNA Alternative Download
If HuggingFace access is unavailable:
```bash
git clone https://github.com/dig-team/hanna-benchmark-asg
cp hanna-benchmark-asg/hanna_stories_annotations.csv datasets/hanna/
```

---

## Quick Validation Script

```python
import json, csv

datasets_info = {}

with open("datasets/writingprompts/train_subset.json") as f:
    wp = json.load(f)
datasets_info["WritingPrompts"] = len(wp)

with open("datasets/tinystories/train_subset.json") as f:
    ts = json.load(f)
datasets_info["TinyStories"] = len(ts)

with open("datasets/rocstories/subset.json") as f:
    roc = json.load(f)
datasets_info["ROCStories"] = len(roc)

with open("datasets/hanna/hanna_stories_annotations.csv") as f:
    hanna = list(csv.DictReader(f))
datasets_info["HANNA"] = len(hanna)

with open("datasets/openmeva/subset_flat.json") as f:
    openmeva = json.load(f)
datasets_info["OpenMEVA"] = len(openmeva)

for name, count in datasets_info.items():
    print(f"{name}: {count} examples")
```

---

## Summary Table

| Dataset | Examples Downloaded | Format | Key Fields | Primary Use |
|---|---|---|---|---|
| WritingPrompts | 5,000 | JSON | prompt, story | Prompt-conditioned story generation |
| TinyStories | 5,000 | JSON | text | Simple story baseline |
| ROCStories/Story Cloze | 1,000 | JSON | 4 context sentences + 2 endings | Coherence evaluation |
| HANNA (original) | 3,168 annotations | CSV | Story, 6 quality dimensions | Human evaluation ground truth |
| HANNA (LLM eval) | 1,000 | JSON | pairwise comparisons | LLM vs human preference |
| OpenMEVA | 1,000 (flattened) | JSON | text, model, human_scores | Multi-model quality comparison |
