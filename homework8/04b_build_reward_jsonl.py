import argparse, os, json
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=str, default="data/annotate/pairs.csv")
    ap.add_argument("--out", type=str, default="data/reward_data.jsonl")
    args = ap.parse_args()

    df = pd.read_csv(args.pairs)
    n_ok = 0
    with open(args.out, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            pref = str(row["preferred"]).strip().upper()
            if pref not in {"A","B"}:
                continue
            chosen = row["summary_A"] if pref=="A" else row["summary_B"]
            rejected = row["summary_B"] if pref=="A" else row["summary_A"]
            rec = {"chosen": chosen, "rejected": rejected}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_ok += 1
    print(f"Wrote {n_ok} preference pairs to {args.out}")

if __name__ == "__main__":
    main()
