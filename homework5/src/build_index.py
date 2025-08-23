import sqlite3
import faiss
import numpy as np
from embedding import embed_text

DB_PATH = "hybrid_index.db"
DIM = 768

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
conn.executescript("""
CREATE TABLE IF NOT EXISTS documents (
    doc_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER,
    keywords TEXT
);
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER,
    chunk_text TEXT,
    FOREIGN KEY(doc_id) REFERENCES documents(doc_id)
);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    chunk_text, content='chunks', content_rowid='chunk_id'
);
""")
conn.commit()

# Sample documents and chunking (replace with real chunking)
documents = [
    (1, "Doc One", "Author A", 2020, "keyword1, keyword2",
     ["chunk text one part 1", "chunk text one part 2"]),
    (2, "Doc Two", "Author B", 2021, "keyword3, keyword4",
     ["chunk text two part 1", "chunk text two part 2"]),
]

def insert_document(doc):
    doc_id, title, author, year, keywords, chunks = doc
    cur.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?)",
                (doc_id, title, author, year, keywords))
    for chunk_text in chunks:
        cur.execute("INSERT INTO chunks(doc_id, chunk_text) VALUES (?, ?)", (doc_id, chunk_text))
    conn.commit()
    # Insert chunks into FTS index
    cur.execute("SELECT chunk_id, chunk_text FROM chunks WHERE doc_id=?", (doc_id,))
    for chunk_id, chunk_text in cur.fetchall():
        cur.execute("INSERT INTO chunks_fts(rowid, chunk_text) VALUES (?, ?)", (chunk_id, chunk_text))
    conn.commit()

for doc in documents:
    insert_document(doc)

# Build FAISS index for chunk embeddings
cur.execute("SELECT chunk_id, chunk_text FROM chunks ORDER BY chunk_id")
rows = cur.fetchall()

chunk_ids = []
embeddings = []

for chunk_id, chunk_text in rows:
    vec = embed_text(chunk_text)
    chunk_ids.append(chunk_id)
    embeddings.append(vec)

embeddings = np.vstack(embeddings).astype('float32')

index = faiss.IndexFlatIP(DIM)
index.add(embeddings)

# Save index and chunk_id mapping
faiss.write_index(index, "faiss.index")
with open("chunk_ids.txt", "w") as f:
    for cid in chunk_ids:
        f.write(str(cid) + "\n")

print("Index built and saved.")
