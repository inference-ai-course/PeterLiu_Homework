# 🧠 Machine Learning Engineering Homework

This repository contains my homework submissions for the Machine Learning Engineering (MLE) program.  
Each week's submission is organized into its own folder (e.g., `homework1/`, `homework2/`, etc.), with code, documentation, and screenshots (if applicable).

---

## 🔗 Project Repository

👉 [PeterLiu_Homework on GitHub](https://github.com/inference-ai-course/PeterLiu_Homework)

---

## 📁 Contents

| Folder     | Description                                                                                  |
|------------|----------------------------------------------------------------------------------------------|
| homework1/ | LangChain-based AI agent using Ollama and Gradio                                             |
| homework2/ | End-to-end data pipeline: web/audio scraping, cleaning, deduplication                        |
| homework3/ | Voice-based LLM assistant with ASR, local LLM, and TTS via FastAPI                           |
| homework4/ | Retrieval-Augmented Generation (RAG) system with arXiv papers                                |
| README.md  | This file (overview of all weekly submissions)                                               |

---

## ✅ Week 1 – Build Your First AI Agent

🎯 **Goal:**  
Set up a local LLM workflow and build a plugin-enabled AI assistant.

✅ **What was done:**

- Installed and ran LLMs locally using Ollama  
- Integrated LangChain and Gradio to build an interactive UI  
- Built a plugin-capable agent that could call external tools:  
  - Brave Search 🔍  
  - Puppeteer for web scraping 📄  
  - Filesystem tools 📁  
  - Notion and GitHub APIs 🧠🐙  
- *(Optional)* Automatically scraped and saved data to Notion

---

## ✅ Week 2 – Data Collection & Cleaning Pipeline

🎯 **Goal:**  
Create a reproducible pipeline for collecting and cleaning multimodal data (text, audio, image).

✅ **What was done:**

- Performed web scraping (text & PNG) and audio crawling (.mp3)  
- Applied content extraction, language filtering, and standardization  
- Used MinHash + `datasketch` to detect and remove duplicates  
- Saved final clean dataset in JSONL format  
- All steps implemented as modular Jupyter Notebooks

---

## ✅ Week 3 – Build a Local Voice-Based AI Assistant

🎯 **Goal:**  
Create a modular voice-based AI assistant that processes voice input and generates spoken responses using local models.

✅ **What was done:**

- Built an ASR → LLM → TTS pipeline served via FastAPI  
- Used Faster-Whisper or Whisper.cpp to transcribe speech  
- Queried local LLaMA3 model via Ollama for responses  
- Converted output text to speech via Edge-TTS  
- Added multi-turn memory to maintain conversational context  
- Exposed via `/voice-chat/` API endpoint  
- *(Optional)* Dockerized the entire project for deployment

---

## ✅ Week 4 – Retrieval-Augmented Generation (RAG) with arXiv Papers

🎯 **Goal:**  
Build a foundational Retrieval-Augmented Generation (RAG) system tailored to scientific research.  
Instead of relying solely on LLM memory, create a semantic index to enable document-aware, grounded answers.

✅ **What was done:**

- Collected 50 recent arXiv cs.CL PDF papers (via scraping or sample set)  
- Extracted and cleaned text from PDFs using PyMuPDF  
- Chunked documents into ≤512-token overlapping segments (sliding window approach)  
- Generated dense vector embeddings for chunks using Sentence-Transformers (`all-MiniLM-L6-v2`)  
- Built a FAISS index (`IndexFlatL2`) to enable fast vector similarity search  
- Developed a notebook demo for querying the index and displaying top relevant text chunks  
- Created a FastAPI service exposing a `/search` endpoint that accepts queries, performs embedding & retrieval, and returns top passages in JSON  
- Laid the groundwork for building a private research knowledge base to be extended in Week 5

📚 **Key Concepts & Techniques:**

- Retriever-Reader QA pipeline components  
- Document chunking strategies and their impact on retrieval quality  
- Semantic indexing with vector embeddings & FAISS  
- Serving semantic search via FastAPI API endpoint

---

## 📸 Screenshots

You can find relevant screenshots in each week’s folder:

- `homework1/screenshots/`  
- `homework2/screenshots/`  
- `homework3/screenshots/` (if applicable)  
- `homework4/screenshots/` (if applicable)

---

## 📞 Contact

For any questions or clarifications, feel free to reach out via Canvas or email.
