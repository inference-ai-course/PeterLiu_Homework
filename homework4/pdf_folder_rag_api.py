# pdf_folder_rag_api.py

from typing import List, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import fitz  # PyMuPDF
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# ------------------ 1. 全局模型初始化 ------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ 2. 批量读取 PDF 文本 ------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def load_pdfs_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    pdf_texts = []
    for pdf_file in pdf_files:
        full_path = os.path.join(folder_path, pdf_file)
        try:
            text = extract_text_from_pdf(full_path)
            pdf_texts.append((pdf_file, text))
        except Exception as e:
            print(f"Failed to read {pdf_file}: {e}")
    return pdf_texts  # List of (filename, full_text)

# ------------------ 3. 分块 ------------------
def chunk_text(text: str, max_tokens: int = 512, overlap: int = 50) -> List[str]:
    tokens = text.split()
    chunks = []
    step = max_tokens - overlap
    for i in range(0, len(tokens), step):
        chunk = tokens[i:i + max_tokens]
        chunks.append(" ".join(chunk))
    return chunks

# ------------------ 4. 嵌入并构建索引 ------------------
def embed_chunks(chunks: List[str]) -> List[List[float]]:
    return embedding_model.encode(chunks, show_progress_bar=True)

def build_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

# ------------------ 5. 查询 ------------------
def search_index(query: str, model: SentenceTransformer, index: faiss.Index, metadata: List[Tuple[str, str]], top_k: int = 5):
    query_vector = model.encode([query])[0].astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    results = []
    for i in indices[0]:
        doc_name, chunk_text = metadata[i]
        results.append({
            "document": doc_name,
            "chunk": chunk_text
        })
    return results

# ------------------ 6. FastAPI ------------------
app = FastAPI()

class QueryRequest(BaseModel):
    q: str

@app.get("/")
def root():
    return {"message": "Multi-PDF RAG Search API"}

@app.post("/search")
def search(request: QueryRequest):
    query = request.q
    results = search_index(query, embedding_model, faiss_index, index_metadata)
    return {"query": query, "results": results}

# ------------------ 7. 初始化 FAISS 索引 ------------------
# 👇在 FastAPI 启动前加载所有 PDF 文件
pdf_folder = "/Users/peterliu/Documents/homework4/arxiv_cs.CL_pdfs"
pdfs = load_pdfs_from_folder(pdf_folder)

# 存储 chunk 及其来源元数据（文档名 + chunk）
all_chunks = []
index_metadata = []  # List of (filename, chunk_text)

for filename, text in pdfs:
    chunks = chunk_text(text)
    all_chunks.extend(chunks)
    index_metadata.extend([(filename, chunk) for chunk in chunks])

embeddings = embed_chunks(all_chunks)
faiss_index = build_faiss_index(embeddings)
