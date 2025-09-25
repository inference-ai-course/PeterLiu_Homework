import argparse, os, json, time, random
import arxiv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", type=str, default="cs.CL OR cs.LG")
    ap.add_argument("--max_results", type=int, default=10)
    ap.add_argument("--out", type=str, default="data/papers")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    random.seed(args.seed)

    search = arxiv.Search(
        query=args.query,
        max_results=args.max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    meta = []
    for r in search.results():
        paper_id = r.entry_id.split("/")[-1]
        safe_id = paper_id.replace(":", "_")
        pdf_path = os.path.join(args.out, f"{safe_id}.pdf")
        print("Downloading:", r.title)
        r.download_pdf(filename=pdf_path)
        meta.append({
            "id": safe_id,
            "title": r.title,
            "summary": r.summary,
            "authors": [a.name for a in r.authors],
            "published": r.published.strftime("%Y-%m-%d"),
            "primary_category": r.primary_category,
        })
        time.sleep(1)  # be polite
    with open(os.path.join(args.out, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
