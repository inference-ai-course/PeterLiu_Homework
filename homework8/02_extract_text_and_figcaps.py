import argparse, os, json, re
import fitz

CAP_RE = re.compile(r"^\s*(Figure|Fig\.?)\s*\d+[:.\)]", re.IGNORECASE)

def extract_text_and_figcaps(pdf_path, max_pages=8):
    doc = fitz.open(pdf_path)
    text_chunks = []
    captions = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text = page.get_text("text")
        text_chunks.append(text)

        # crude caption detection
        for line in text.splitlines():
            if CAP_RE.search(line):
                captions.append(line.strip())
    return "\n".join(text_chunks), captions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", type=str, default="data/papers")
    ap.add_argument("--out", type=str, default="data/parsed")
    ap.add_argument("--max_pages", type=int, default=8)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.inp, "metadata.json"), "r", encoding="utf-8") as f:
        meta = json.load(f)

    out_meta = []
    for m in meta:
        pdf = os.path.join(args.inp, f"{m['id']}.pdf")
        if not os.path.exists(pdf):
            continue
        text, caps = extract_text_and_figcaps(pdf, args.max_pages)
        record = {
            "id": m["id"],
            "title": m["title"],
            "abstract": m["summary"],
            "text_excerpt": text,
            "figure_captions": caps[:8],
        }
        out_meta.append(record)

    with open(os.path.join(args.out, "parsed.json"), "w", encoding="utf-8") as f:
        json.dump(out_meta, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
