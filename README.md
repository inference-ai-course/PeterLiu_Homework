🧠 Peter Liu – Machine Learning Engineering Homework Portfolio

This repository contains my Machine Learning Engineering (MLE) homework submissions. Each week’s submission is organized into its own folder, complete with code, documentation, and screenshots where applicable.

📌 Table of Contents

Week 1 – AI Agent (LangChain + Ollama)

Week 2 – Data Collection & Cleaning Pipeline

Week 3 – Local Voice-Based AI Assistant

Week 4 – Retrieval-Augmented Generation (RAG)

Week 5 – Advanced RAG with Hybrid Retrieval

Week 6 – Voice Agent with Function Calling

Week 7 – LLM Fine-Tuning (LoRA & QLoRA)

Week 8 – Multimodal Summarization + Reward Modeling

TCM Voice Assistant Demo

Contact

Week 1 – AI Agent (LangChain + Ollama)

Goal: Set up a local LLM workflow and build a plugin-enabled AI assistant.

Highlights:

Local LLM setup with Ollama

Interactive UI via LangChain + Gradio

Plugin-capable agent: Brave Search, Puppeteer, filesystem, Notion, GitHub APIs

Optional: Automatic scraping & saving to Notion

📁 Folder: homework1/

Week 2 – Data Collection & Cleaning Pipeline

Goal: Build a reproducible pipeline for multimodal data (text, audio, image).

Highlights:

Web scraping and audio crawling

Content extraction, language filtering, standardization

Deduplication using MinHash + datasketch

Final clean dataset in JSONL

Modular Jupyter notebooks

📁 Folder: homework2/

Week 3 – Local Voice-Based AI Assistant

Goal: Modular voice assistant: ASR → LLM → TTS

Highlights:

Faster-Whisper / Whisper.cpp for transcription

Local LLaMA3 via Ollama

Edge-TTS for spoken responses

Multi-turn memory

FastAPI endpoint /voice-chat/

Optional Docker deployment

📁 Folder: homework3/

Week 4 – Retrieval-Augmented Generation (RAG)

Goal: Build a RAG system for arXiv papers

Highlights:

50 arXiv cs.CL PDFs

Text extraction via PyMuPDF

Chunking ≤512 tokens with sliding window

Embeddings via Sentence-Transformers (all-MiniLM-L6-v2)

FAISS vector similarity search

Notebook demo + FastAPI /search endpoint

📁 Folder: homework4/

Week 5 – Advanced RAG with Hybrid Retrieval

Goal: Hybrid retrieval & evaluation

Highlights:

BM25 + FAISS dense retrieval

Weighted scoring, rank fusion

Evaluation: Recall@K, MRR, nDCG

Human-in-the-loop spot checks

FastAPI /hybrid-search endpoint

📁 Folder: homework5/

Week 6 – Voice Agent with Function Calling

Goal: Local voice assistant with function calling

Highlights:

Streamlit frontend for text + audio input

Offline STT: faster-whisper

Function calls: calculate(expression) & search_arxiv(query)

TTS with pyttsx3, multi-turn chat bubbles

FastAPI backend /docs + Streamlit /voice

📁 Folder: homework6/

Week 7 – LLM Fine-Tuning (LoRA & QLoRA)

Goal: Parameter-efficient fine-tuning

Highlights:

Hugging Face + PEFT pipeline

LoRA adapters & QLoRA 4-bit quantization

Fine-tuned on domain-specific instruction datasets

Evaluation vs base model

Saved adapters for inference

📁 Folder: homework7/

Week 8 – Multimodal Summarization + Reward Modeling

Goal: End-to-end minimal pipeline for multimodal summarization + reward modeling

Pipeline:

Collect 10 arXiv papers

Extract text + figure captions

Generate 2 summaries per paper (A/B)

Human annotation → reward data (reward_data.jsonl)

Train DeBERTa-v3 reward model

Evaluate: ROUGE, BERTScore, Reward score

Notes:

Multimodal: figure captions included in prompt

Configurable LLM: default Meta-Llama-3-8B-Instruct

Reward training via TRL PairwiseRewardTrainer

📁 Folder: wk8_multimodal_reward/

TCM Voice Assistant Demo (RAG + GPT + gTTS)

Goal: Streamlit voice assistant for Traditional Chinese Medicine knowledge

Features:

Text/Voice input → GPT-4o-mini responses + gTTS playback

Multi-turn chat with conversation bubbles

Works with PyAudio or SoundDevice

Cross-platform audio playback via gTTS + playsound

Tech Stack: Streamlit, OpenAI GPT API, gTTS, SpeechRecognition, playsound, numpy, python-dotenv

Setup:

pip install streamlit openai python-dotenv numpy SpeechRecognition gTTS playsound sounddevice
streamlit run voice_tcm_agent/voice_tcm_agent.py


📁 Folder: voice_tcm_agent/

Contact

For questions or clarifications, reach out via Canvas or email.
