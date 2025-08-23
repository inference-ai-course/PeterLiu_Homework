import faiss
import numpy as np

DIM = 768

# Load FAISS index and chunk_ids
index = faiss.read_index("faiss.index")
with open("chunk_ids.txt") as f:
    chunk_ids = [int(line.strip()) for line in f]

def search_faiss(query_embedding, top_k=5):
    D, I = index.search(query_embedding.reshape(1, -1), top_k)
    results = {}
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        chunk_id = chunk_ids[idx]
        results[chunk_id] = dist
    return results
