# 🧠 Peter Liu – Machine Learning Engineering Homework Portfolio

This repository contains my **Machine Learning Engineering (MLE) homework submissions**. Each week’s work is organized in its own folder, complete with code, documentation, and screenshots where applicable.

---

## 📌 Table of Contents

<details>
<summary>Week 1 – AI Agent (LangChain + Ollama)</summary>

- **Goal:** Set up a local LLM workflow and build a plugin-enabled AI assistant.
- **Highlights:**
  - Local LLM setup with Ollama
  - Interactive UI via LangChain + Gradio
  - Plugin-capable agent: Brave Search, Puppeteer, filesystem, Notion, GitHub APIs
  - Optional: Automatic scraping & saving to Notion
- **Folder:** `homework1/`
- **Screenshot:** ![Week1 Screenshot]
</details>

<details>
<summary>Week 2 – Data Collection & Cleaning Pipeline</summary>

- **Goal:** Build a reproducible pipeline for multimodal data (text, audio, image)
- **Highlights:**
  - Web scraping and audio crawling
  - Content extraction, language filtering, standardization
  - Deduplication using MinHash + datasketch
  - Final clean dataset in JSONL
  - Modular Jupyter notebooks
- **Folder:** `homework2/`
- **Screenshot:** 
</details>

<details>
<summary>Week 3 – Local Voice-Based AI Assistant</summary>

- **Goal:** Modular voice assistant: ASR → LLM → TTS
- **Highlights:**
  - Faster-Whisper / Whisper.cpp for transcription
  - Local LLaMA3 via Ollama
  - Edge-TTS for spoken responses
  - Multi-turn memory
  - FastAPI endpoint `/voice-chat/`
  - Optional Docker deployment
- **Folder:** `homework3/`
- **Screenshot:** ![Week3 Screenshot](homework3/screenshot.png)
</details>

<details>
<summary>Week 4 – Retrieval-Augmented Generation (RAG)</summary>

- **Goal:** Build a RAG system for arXiv papers
- **Highlights:**
  - 50 arXiv cs.CL PDFs
  - Text extraction via PyMuPDF
  - Chunking ≤512 tokens with sliding window
  - Embeddings via Sentence-Transformers (`all-MiniLM-L6-v2`)
  - FAISS vector similarity search
  - Notebook demo + FastAPI `/search` endpoint
- **Folder:** `homework4/`
- **Screenshot:** ![Week4 Screenshot](homework4/screenshot.png)
</details>

<details>
<summary>Week 5 – Advanced RAG with Hybrid Retrieval</summary>

- **Goal:** Hybrid retrieval & evaluation
- **Highlights:**
  - BM25 + FAISS dense retrieval
  - Weighted scoring, rank fusion
  - Evaluation: Recall@K, MRR, nDCG
  - Human-in-the-loop spot checks
  - FastAPI `/hybrid-search` endpoint
- **Folder:** `homework5/`
- **Screenshot:** ![Week5 Screenshot](homework5/screenshot.png)
</details>

<details>
<summary>Week 6 – Voice Agent with Function Calling</summary>

- **Goal:** Local voice assistant with function calling
- **Highlights:**
  - Streamlit frontend for text + audio input
  - Offline STT: faster-whisper
  - Function calls: `calculate(expression)` & `search_arxiv(query)`
  - TTS with pyttsx3, multi-turn chat bubbles
  - FastAPI backend `/docs` + Streamlit `/voice`
- **Folder:** `homework6/`
- **Screenshot:** ![Week6 Screenshot](homework6/screenshot.png)
</details>

<details>
<summary>Week 7 – LLM Fine-Tuning (LoRA & QLoRA)</summary>

- **Goal:** Parameter-efficient fine-tuning
- **Highlights:**
  - Hugging Face + PEFT pipeline
  - LoRA adapters & QLoRA 4-bit quantization
  - Fine-tuned on domain-specific instruction datasets
  - Evaluation vs base model
  - Saved adapters for inference
- **Folder:** `homework7/`
- **Screenshot:** ![Week7 Screenshot]
</details>

<details>
<summary>Week 8 – Multimodal Summarization + Reward Modeling</summary>

- **Goal:** Minimal end-to-end pipeline for multimodal summarization + reward modeling
- **Pipeline:**
  - Collect 10 arXiv papers
  - Extract text + figure captions
  - Generate 2 summaries per paper (A/B)
  - Human annotation → reward data (`reward_data.jsonl`)
  - Train DeBERTa-v3 reward model
  - Evaluate: ROUGE, BERTScore, Reward score
- **Notes:**
  - Multimodal: figure captions included in prompt
  - Configurable LLM: default `Meta-Llama-3-8B-Instruct`
  - Reward training via TRL `PairwiseRewardTrainer`
- **Folder:** `homework8/`
- **Screenshot:** 
</details>

<details>
<summary>Week 9-10 – TCM Voice Assistant Demo</summary>

- **Goal:** Streamlit voice assistant for Traditional Chinese Medicine knowledge
- **Features:**
  - Text/Voice input → GPT-4o-mini responses + gTTS playback
  - Multi-turn chat with conversation bubbles
  - Works with PyAudio or SoundDevice
  - Cross-platform audio playback via gTTS + playsound
- **Tech Stack:** Streamlit, OpenAI GPT API, gTTS, SpeechRecognition, playsound, numpy, python-dotenv
- **Setup:**  
  ```bash
  pip install streamlit openai python-dotenv numpy SpeechRecognition gTTS playsound sounddevice
  streamlit run voice_tcm_agent/voice_tcm_agent.py
Folder: homework910/

Screenshot:![Week910 Screenshot](homework910/TCM_voice_screenshots)

</details>
📫 Contact
For questions or clarifications, reach out via Canvas or email.

⚡ Suggested GitHub Badges
less
Copy code
![Python](https://img.shields.io/badge/python-3.12-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.24-orange)
![HuggingFace](https://img.shields.io/badge/HuggingFace-🤗-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
