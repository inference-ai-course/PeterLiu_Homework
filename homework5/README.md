

# Hybrid Retrieval Project

This project implements a **hybrid document retrieval system** that combines dense vector search (using FAISS) with sparse keyword search (using SQLite FTS5 or BM25). The goal is to leverage the strengths of both semantic search and exact keyword matching to improve retrieval effectiveness.

---

## 📂 Project Structure

```text
homework5/
├── src/
│   ├── embedding.py   # Text embedding function (simulated)
│   ├── search.py      # Vector search, keyword search, hybrid fusion logic
│   ├── api.py         # FastAPI app exposing /hybrid_search endpoint
├── notebooks/
│   └── evaluation.ipynb   # Jupyter notebook to evaluate retrieval methods
├── data/
│   └── ...   # Document data and SQLite + FAISS indexes
├── requirements.txt   # Python dependencies
└── README.md          # This file
````

---

## ⚙️ Setup Instructions

1. **Create and activate Python environment (Anaconda recommended):**

   ```bash
   conda create -n class5_env python=3.10 -y
   conda activate class5_env
   ```

2. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Prepare your document dataset and build SQLite + FAISS indexes**
   Follow your indexing scripts or pipeline to prepare data.

---

## 🚀 Usage

### 1. Run Evaluation Notebook

Start Jupyter and open the evaluation notebook to test retrieval quality:

```bash
jupyter notebook notebooks/evaluation.ipynb
```

This notebook runs sample queries and computes **Recall\@3** for:

* Vector-only search
* Keyword-only search
* Hybrid search

---

### 2. Launch FastAPI Server

From the project root directory:

```bash
uvicorn src.api:app --reload
```

Open API docs at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** or call:

```http
GET /hybrid_search?query=your+search+terms&k=3
```

**Example response:**

```json
{
  "results": [
    {"doc_id": 2, "score": 0.89, "title": "Example Document Title", "author": "Author Name", "year": 2023}
  ]
}
```

---

## 📄 Code Overview

* **`src/embedding.py`**: Generates simulated embeddings from text queries
* **`src/search.py`**: Implements vector search, keyword search, and hybrid fusion methods
* **`notebooks/evaluation.ipynb`**: Notebook to evaluate retrieval methods on example queries
* **`src/api.py`**: FastAPI server exposing `/hybrid_search` endpoint

---

## 📚 References & Further Reading

* [FAISS](https://github.com/facebookresearch/faiss)
* [SQLite FTS5 Documentation](https://www.sqlite.org/fts5.html)
* [BM25 Ranking](https://en.wikipedia.org/wiki/Okapi_BM25)
* [Reciprocal Rank Fusion](https://en.wikipedia.org/wiki/Reciprocal_rank_fusion)
* [FastAPI Framework](https://fastapi.tiangolo.com)

---

## 👩‍💻 Contact & Contribution

Feel free to open issues or pull requests if you want to contribute or have questions.

**Happy hybrid searching! 🚀**


