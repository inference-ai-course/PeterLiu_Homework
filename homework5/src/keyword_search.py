import sqlite3

conn = sqlite3.connect("hybrid_index.db")

def search_keyword(query, top_k=5):
    cur = conn.execute("""
    SELECT chunks.chunk_id, chunks.doc_id, bm25(chunks_fts) AS score
    FROM chunks_fts
    JOIN chunks ON chunks_fts.rowid = chunks.chunk_id
    WHERE chunks_fts MATCH ?
    ORDER BY score LIMIT ?
    """, (query, top_k))
    # bm25 lower score is better, so invert sign for ranking
    results = {row[0]: -row[2] for row in cur.fetchall()}
    return results
