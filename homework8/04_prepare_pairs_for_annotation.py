import argparse, os, json
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summ", type=str, default="data/summaries")
    ap.add_argument("--out", type=str, default="data/annotate/pairs.csv")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(os.path.join(args.summ, "summaries.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for d in data:
        rows.append({
            "paper_id": d["id"],
            "title": d["title"],
            "summary_A": d["summary_A"],
            "summary_B": d["summary_B"],
            "preferred": ""  # fill with 'A' or 'B'
        })
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print("Wrote:", args.out)

if __name__ == "__main__":
    main()
