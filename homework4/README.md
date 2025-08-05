✅ Week 4 – Retrieval-Augmented Generation (RAG) with arXiv Papers

🎯 Goal:

Build a foundational Retrieval-Augmented Generation (RAG) system tailored to scientific research.  
Instead of relying solely on LLM memory, create a semantic index to enable document-aware, grounded answers.

✅ What was done:

- Collected 50 recent arXiv cs.CL PDF papers (via scraping or sample set)  
- Extracted and cleaned text from PDFs using PyMuPDF  
- Chunked documents into ≤512-token overlapping segments (sliding window approach)  
- Generated dense vector embeddings for chunks using Sentence-Transformers ('all-MiniLM-L6-v2')  
- Built a FAISS index (IndexFlatL2) to enable fast vector similarity search  
- Developed a notebook demo for querying the index and displaying top relevant text chunks  
- Created a FastAPI service exposing a `/search` endpoint that accepts queries, performs embedding & retrieval, and returns top passages in JSON  
- Laid the groundwork for building a private research knowledge base to be extended in Week 5

📚 Key Concepts & Techniques:

- Retriever-Reader QA pipeline components  
- Document chunking strategies and their impact on retrieval quality  
- Semantic indexing with vector embeddings & FAISS  
- Serving semantic search via FastAPI API endpoint  

---

