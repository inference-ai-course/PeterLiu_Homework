# 🧠 Machine Learning Engineering Homework

This repository contains my homework submissions for the Machine Learning Engineering (MLE) program.  
Each week's submission is organized into its own folder (e.g., homework1/, homework2/, etc.), with code, documentation, and screenshots (if applicable).

## 🔗 Project Repository
👉 [PeterLiu_Homework on GitHub](https://github.com/inference-ai-course/PeterLiu_Homework)

## 📁 Contents
Folder      | Description
----------- | -----------------------------------------------
homework1/  | LangChain-based AI agent using Ollama and Gradio
homework2/  | End-to-end data pipeline: web/audio scraping, cleaning, deduplication
homework3/  | Voice-based LLM assistant with ASR, local LLM, and TTS via FastAPI
homework4/  | Retrieval-Augmented Generation (RAG) system with arXiv papers
homework5/  | Advanced RAG: hybrid retrieval and evaluation framework
homework6/  | Voice Agent with Function Calling (local deployment)
homework7/  | LLM Fine-Tuning with LoRA / QLoRA
README.md   | This file (overview of all weekly submissions)

---

## ✅ Week 1 – Build Your First AI Agent
🎯 Goal:  
Set up a local LLM workflow and build a plugin-enabled AI assistant.

**What was done:**
- Installed and ran LLMs locally using Ollama  
- Integrated LangChain and Gradio to build an interactive UI  
- Built a plugin-capable agent that could call external tools:
  - Brave Search 🔍
  - Puppeteer for web scraping 📄
  - Filesystem tools 📁
  - Notion and GitHub APIs 🧠🐙  
- (Optional) Automatically scraped and saved data to Notion  

---

## ✅ Week 2 – Data Collection & Cleaning Pipeline
🎯 Goal:  
Create a reproducible pipeline for collecting and cleaning multimodal data (text, audio, image).

**What was done:**
- Performed web scraping (text & PNG) and audio crawling (.mp3)  
- Applied content extraction, language filtering, and standardization  
- Used MinHash + datasketch to detect and remove duplicates  
- Saved final clean dataset in JSONL format  
- All steps implemented as modular Jupyter Notebooks  

---

## ✅ Week 3 – Build a Local Voice-Based AI Assistant
🎯 Goal:  
Create a modular voice-based AI assistant that processes voice input and generates spoken responses using local models.

**What was done:**
- Built an ASR → LLM → TTS pipeline served via FastAPI  
- Used Faster-Whisper or Whisper.cpp to transcribe speech  
- Queried local LLaMA3 model via Ollama for responses  
- Converted output text to speech via Edge-TTS  
- Added multi-turn memory to maintain conversational context  
- Exposed via `/voice-chat/` API endpoint  
- (Optional) Dockerized the entire project for deployment  

---

## ✅ Week 4 – Retrieval-Augmented Generation (RAG) with arXiv Papers
🎯 Goal:  
Build a foundational RAG system tailored to scientific research.

**What was done:**
- Collected 50 recent arXiv cs.CL PDF papers (via scraping or sample set)  
- Extracted and cleaned text from PDFs using PyMuPDF  
- Chunked documents into ≤512-token overlapping segments (sliding window)  
- Generated dense vector embeddings with Sentence-Transformers (`all-MiniLM-L6-v2`)  
- Built a FAISS index (IndexFlatL2) for fast vector similarity search  
- Developed a notebook demo for querying the index and displaying top text chunks  
- Exposed a `/search` FastAPI endpoint to accept queries and return top passages in JSON  

---

## ✅ Week 5 – Advanced RAG with Hybrid Retrieval
🎯 Goal:  
Extend the RAG system with hybrid retrieval (dense + sparse methods) and design an evaluation pipeline for retrieval quality.

**What was done:**
- Integrated BM25 retriever with FAISS dense retriever → hybrid retrieval strategy  
- Implemented weighted scoring and rank fusion to combine dense + sparse results  
- Added evaluation using:
  - Recall@K, MRR (Mean Reciprocal Rank), nDCG  
  - Human-in-the-loop spot checks for relevance  
- Enhanced pipeline modularity (retriever registry, configurable backends)  
- Built an interactive notebook for side-by-side retrieval comparison  
- Extended FastAPI service with `/hybrid-search` endpoint  

---

## ✅ Week 6 – Voice Agent with Function Calling (Local Deployment)
🎯 Goal:  
Build a fully local voice assistant that supports speech input/output and function calling.

**What was done:**
- Implemented text + audio input via Streamlit frontend  
- Offline speech-to-text (STT) with faster-whisper  
- Added function calling support:
  - `calculate(expression)` → math calculation
  - `search_arxiv(query)` → simulated arXiv paper search  
- Integrated text-to-speech (TTS) using pyttsx3  
- Displayed multi-turn chat history in UI  
- Local deployment:
  - FastAPI backend (`/docs` for API testing)  
  - Streamlit frontend (`/voice` for interaction)  
- Extensible design → add new tools in `backend.py`, swap STT/TTS for streaming  

---

## ✅ Week 7 – LLM Fine-Tuning (LoRA & QLoRA)
🎯 Goal:  
Perform parameter-efficient fine-tuning of large language models using LoRA and QLoRA.

**What was done:**
- Set up fine-tuning pipeline with Hugging Face transformers + PEFT  
- Implemented LoRA adapters for efficient training on limited GPU resources  
- Used QLoRA with bitsandbytes for 4-bit quantization → reduced VRAM usage  
- Trained models on domain-specific datasets (instruction-style)  
- Evaluated fine-tuned models vs. base model on benchmark prompts  
- Saved and reloaded fine-tuned adapters for inference & deployment  

---

## 📸 Screenshots
Screenshots for each homework are stored in the respective folders:

- homework1/screenshots/  
- homework2/screenshots/  
- homework3/screenshots/  
- homework4/screenshots/  
- homework5/screenshots/ (run on Inference.ai Cloud Server)  
- homework6/screenshots/  
- homework7/screenshots/ (run on Inference.ai Cloud Server)  

---

## 📞 Contact
For any questions or clarifications, feel free to reach out via Canvas or email.

