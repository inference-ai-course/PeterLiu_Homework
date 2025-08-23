# src/search.py

import numpy as np

def search_faiss(embedding: np.ndarray, top_k=3):
    """
    模拟FAISS向量搜索
    返回[(doc_id, score), ...]，score越大越相关
    """
    np.random.seed(42)  # 复现
    db_size = 10
    dim = embedding.shape[0]
    db_embeddings = np.random.rand(db_size, dim)
    scores = db_embeddings @ embedding  # 点积模拟相似度
    ranked_idx = np.argsort(scores)[::-1][:top_k]
    return [(int(i), float(scores[i])) for i in ranked_idx]


def search_keyword(query: str, top_k=3):
    """
    模拟关键词搜索（比如SQLite FTS或BM25）
    返回[(doc_id, score), ...]
    """
    np.random.seed(len(query))  # 保证同query同结果
    db_size = 10
    doc_ids = list(range(db_size))
    scores = np.random.rand(db_size)
    ranked_idx = np.argsort(scores)[::-1][:top_k]
    return [(doc_ids[i], float(scores[i])) for i in ranked_idx]


def hybrid_search(embedding: np.ndarray, vector_search_fn, keyword_search_fn, query: str, top_k=3):
    """
    简单加权融合向量和关键词搜索结果，返回[(doc_id, combined_score), ...]
    """
    vec_res = vector_search_fn(embedding, top_k=top_k)
    key_res = keyword_search_fn(query, top_k=top_k)

    combined_scores = {}

    # 先归一化分数方便融合
    def normalize(scores):
        min_s = min(scores)
        max_s = max(scores)
        return [(s - min_s) / (max_s - min_s + 1e-8) for s in scores]

    vec_scores = [s for _, s in vec_res]
    key_scores = [s for _, s in key_res]

    norm_vec_scores = normalize(vec_scores)
    norm_key_scores = normalize(key_scores)

    for (doc_id, _), norm_s in zip(vec_res, norm_vec_scores):
        combined_scores[doc_id] = combined_scores.get(doc_id, 0) + 0.6 * norm_s

    for (doc_id, _), norm_s in zip(key_res, norm_key_scores):
        combined_scores[doc_id] = combined_scores.get(doc_id, 0) + 0.4 * norm_s

    ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return ranked
