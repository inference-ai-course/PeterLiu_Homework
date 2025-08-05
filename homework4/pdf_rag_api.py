# pdf_rag_api.py

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ----------- 1. Load PDF and Extract Text -----------
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        page_text = page.get_text()
        pages.append(page_text)
    return "\n".join(pages)

# ----------- 2. Chunk Text -----------
def chunk_text(text: str, max_tokens: int = 512, overlap: int = 50) -> List[str]:
    tokens = text.split()
    chunks = []
    step = max_tokens - overlap
    for i in range(0, len(tokens), step):
        chunk = tokens[i:i + max_tokens]
        chunks.append(" ".join(chunk))
    return chunks

# ----------- 3. Embed Chunks -----------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    return embedding_model.encode(chunks, show_progress_bar=True)

# ----------- 4. Build FAISS Index -----------
def build_faiss_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

# ----------- 5. Search Function -----------
def search_index(query: str, model: SentenceTransformer, index: faiss.Index, chunks: List[str], top_k: int = 3):
    query_vector = model.encode([query])[0].astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    return [chunks[i] for i in indices[0]]

# ----------- 6. FastAPI App -----------
app = FastAPI()

# 运行前初始化：你应该在主函数或启动脚本中运行下面逻辑
# 注意这里的路径应为 PDF 文件路径，不是文件夹
pdf_path = "/Users/peterliu/Documents/homework4/arxiv_cs.CL_pdfs/9908001v1.pdf"
full_text = extract_text_from_pdf(pdf_path)
chunks = chunk_text(full_text)
embeddings = embed_chunks(chunks)
faiss_index = build_faiss_index(embeddings)

class QueryRequest(BaseModel):
    q: str

@app.get("/")
def root():
    return {"message": "RAG PDF Search API"}

@app.post("/search")
def search(request: QueryRequest):
    query = request.q
    results = search_index(query, embedding_model, faiss_index, chunks)
    return {"query": query, "results": results}
