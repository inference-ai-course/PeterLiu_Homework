# Week 8 — Multimodal Summarization + Reward Modeling (Ultra-Simple Pipeline)

This repo is a **one-click, minimal** pipeline that meets all deliverables with the least friction.
You’ll get:
- `10` papers from arXiv (PDF + metadata)
- `2` summaries per paper using an LLM (configurable; defaults to LLaMA 3–8B Instruct on HF)
- A CSV for quick **human preference annotation**
- A `reward_data.jsonl` in chosen/rejected format
- A fine-tuned **DeBERTa-v3** reward model
- An evaluation script that computes **ROUGE**, **BERTScore**, and **Reward scores**, then compares

> Tip: Run everything in a fresh virtual environment with GPU (Colab / local).

## Quickstart (5 steps)

```bash
# 1) Create env & install deps
pip install -r requirements.txt

# 2) Download 10 arXiv papers (PDFs + metadata)
python 01_collect_papers.py --query "cs.CL OR cs.LG" --max_results 10 --out data/papers

# 3) Extract text + figure captions (multimodal signal)
python 02_extract_text_and_figcaps.py --inp data/papers --out data/parsed

# 4) Generate two summaries per paper (A/B)
#    You can change the HF model via --model.
python 03_generate_summaries.py --inp data/parsed --out data/summaries     --model "meta-llama/Meta-Llama-3-8B-Instruct"

# 5) Create an annotation CSV, annotate the "preferred" column, then build reward data
python 04_prepare_pairs_for_annotation.py --summ data/summaries --out data/annotate/pairs.csv
# (Open the CSV, choose A or B per row in the 'preferred' column, save)
python 04b_build_reward_jsonl.py --pairs data/annotate/pairs.csv --out data/reward_data.jsonl

# 6) Train a reward model (DeBERTa-v3)
python 06_train_reward_model.py --data data/reward_data.jsonl --out reward_model

# 7) Evaluate on 10 *new* papers (repeat steps 2–4 with --seed 2 or a different query/path), then:
python 07_evaluate.py --summ data/summaries_new --reward_model reward_model   --report results/report.csv
```

If you’re short on time, you can run steps 2–6 on the same 10 papers to verify the pipeline works,
then re-run step 2 with a different `--seed` to gather 10 new papers for evaluation.

---

## Notes
- **Multimodal**: we include **figure captions** (detected heuristically from the PDF) into the model prompt to condition summaries on textual descriptions of figures.
- Defaults are safe & small. You can switch to any summarization model (e.g., `Qwen2.5-7B-Instruct`, `Llama-3.1-8B-Instruct`).
- Reward training uses TRL’s **PairwiseRewardTrainer** with `microsoft/deberta-v3-base` as a scalar scorer.
- Metrics via `evaluate`: **ROUGE** and **BERTScore**.
- All outputs are plain files (CSV/JSONL) for easy grading.

## Folder Layout
```
wk8_multimodal_reward/
  data/
    papers/            # PDFs + metadata.json
    parsed/            # extracted text + fig captions
    summaries/         # two summaries per paper
    annotate/          # pairs.csv for human labeling
    reward_data.jsonl  # built after labeling
  reward_model/        # fine-tuned reward model
  results/             # evaluation artifacts
  *.py, requirements.txt, README.md
```
