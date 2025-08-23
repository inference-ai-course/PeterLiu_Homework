# src/embedding.py

import numpy as np

def embed_text(text: str) -> np.ndarray:
    """
    模拟文本转embedding向量的函数。
    真实场景用OpenAI或本地模型生成。
    这里简单用字符编码和随机数生成固定长度向量。
    """
    np.random.seed(len(text))  # 让同一句话总是返回相同向量（模拟）
    dim = 128
    vec = np.random.rand(dim)
    return vec / np.linalg.norm(vec)  # 归一化
