import argparse, os, json
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

TEMPLATE_A = """Summarize the following research paper for a technical audience.
- Be concise (150-220 words).
- Cover: problem, method, key results, and limitations.
- Use figure captions if helpful.

Title: {title}

Abstract:
{abstract}

Figure captions (text-only):
{captions}

Short excerpt:
{text}
"""

TEMPLATE_B = """You are an expert research assistant. Write a crisp, factual summary (150-220 words).
Prioritize: contributions, experimental setup, datasets, and takeaway findings.
Do not speculate. If uncertain, say so.

Title: {title}

Abstract:
{abstract}

Selected figure captions:
{captions}

Key excerpt:
{text}
"""

def build_inputs(rec):
    caps = "\n".join(rec.get("figure_captions", [])[:5]) or "(none)"
    excerpt = rec.get("text_excerpt", "")[:3000]
    return (
        TEMPLATE_A.format(title=rec["title"], abstract=rec["abstract"], captions=caps, text=excerpt),
        TEMPLATE_B.format(title=rec["title"], abstract=rec["abstract"], captions=caps, text=excerpt),
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", type=str, default="data/parsed")
    ap.add_argument("--out", type=str, default="data/summaries")
    ap.add_argument("--model", type=str, default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--device", type=str, default=None)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.inp, "parsed.json"), "r", encoding="utf-8") as f:
        records = json.load(f)

    device = 0 if torch.cuda.is_available() and args.device is None else args.device
    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32, device_map="auto"
    )
    genpipe = pipeline("text-generation", model=model, tokenizer=tok, device=device)

    out = []
    for rec in records:
        a,b = build_inputs(rec)
        out_a = genpipe(a, max_new_tokens=220, temperature=0.7, top_p=0.9, do_sample=True)[0]["generated_text"]
        out_b = genpipe(b, max_new_tokens=220, temperature=1.0, top_p=0.95, do_sample=True)[0]["generated_text"]
        out.append({
            "id": rec["id"],
            "title": rec["title"],
            "summary_A": out_a[-900:],
            "summary_B": out_b[-900:],
        })

    with open(os.path.join(args.out, "summaries.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
