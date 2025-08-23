from fastapi import FastAPI
from embedding import embed_text
from faiss_search import search_faiss
from keyword_search import search_keyword
from hybrid_search import hybrid_search
import sqlite3

app = FastAPI()
conn = sqlite3.connect("hybrid_index.db")

@app.get("/hybrid_search")
async def hybrid_search_api(query: str, k: int = 3):
    query_embedding = embed_text(query)
    results = hybrid_search(query_embedding, search_faiss, search_keyword, query, top_k=k)

    out = []
    for chunk_id, score in results:
        cur = conn.execute("SELECT doc_id, chunk_text FROM chunks WHERE chunk_id=?", (chunk_id,))
        doc_id, chunk_text = cur.fetchone()
        cur2 = conn.execute("SELECT title, author FROM documents WHERE doc_id=?", (doc_id,))
        title, author = cur2.fetchone()
        out.append({
            "doc_id": doc_id,
            "chunk_id": chunk_id,
            "title": title,
            "author": author,
            "chunk_text": chunk_text,
            "score": score
        })
    return {"results": out}
