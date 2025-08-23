import numpy as np

def normalize_scores(scores):
    vals = np.array(list(scores.values()))
    min_v, max_v = vals.min(), vals.max()
    if max_v - min_v < 1e-6:
        return {k: 1.0 for k in scores}
    return {k: (v - min_v) / (max_v - min_v) for k, v in scores.items()}

def hybrid_weighted_sum(faiss_scores, keyword_scores, alpha=0.6):
    faiss_norm = normalize_scores(faiss_scores)
    keyword_norm = normalize_scores(keyword_scores)
    all_docs = set(faiss_norm) | set(keyword_norm)
    combined = {}
    for doc in all_docs:
        v = faiss_norm.get(doc, 0.0)
        k = keyword_norm.get(doc, 0.0)
        combined[doc] = alpha * v + (1 - alpha) * k
    return combined

def hybrid_search(query_embedding, faiss_search_fn, keyword_search_fn, query, top_k=5, alpha=0.6):
    faiss_res = faiss_search_fn(query_embedding, top_k)
    keyword_res = keyword_search_fn(query, top_k)
    combined = hybrid_weighted_sum(faiss_res, keyword_res, alpha)
    sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return sorted_combined[:top_k]
