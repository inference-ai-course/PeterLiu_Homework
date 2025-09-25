import argparse, os, json, pandas as pd, numpy as np, torch
from evaluate import load
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_reward_model(path):
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return tok, model, device

def score_reward(tok, model, device, texts, bs=16):
    scores = []
    for i in range(0, len(texts), bs):
        batch = texts[i:i+bs]
        enc = tok(batch, truncation=True, padding=True, max_length=512, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model(**enc).logits.squeeze(-1).detach().cpu().numpy().tolist()
        scores.extend(out)
    return scores

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summ", type=str, default="data/summaries")
    ap.add_argument("--reward_model", type=str, default="reward_model")
    ap.add_argument("--report", type=str, default="results/report.csv")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.report), exist_ok=True)

    with open(os.path.join(args.summ, "summaries.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    # Use titles as lightweight references (consistent for ROUGE/BERTScore)
    refs = []
    hyps = []
    ids = []
    which = []
    for d in data:
        ids += [d["id"], d["id"]]
        refs += [d.get("title","")] * 2
        hyps += [d["summary_A"], d["summary_B"]]
        which += ["A", "B"]

    rouge = load("rouge")
    bertscore = load("bertscore")
    rouge_res = rouge.compute(predictions=hyps, references=refs)
    bert_res = bertscore.compute(predictions=hyps, references=refs, lang="en")

    tok, rm, device = load_reward_model(args.reward_model)
    reward_scores = score_reward(tok, rm, device, hyps)

    df = pd.DataFrame({
        "paper_id": ids,
        "which": which,
        "summary": hyps,
        "rougeL": rouge_res.get("rougeLsum", [np.nan]*len(hyps)) if isinstance(rouge_res, dict) else [np.nan]*len(hyps),
        "bertscore_f1": bert_res["f1"],
        "reward_score": reward_scores,
    })
    df.to_csv(args.report, index=False)
    print("Wrote", args.report)

if __name__ == "__main__":
    main()
