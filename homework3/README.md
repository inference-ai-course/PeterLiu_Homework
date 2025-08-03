# Homework 3 - Voice-Based Personal AI Assistant

## 🗣️ Overview

This assignment focuses on building a voice-driven AI agent capable of natural conversation using:

- 🎤 **ASR**: Automatic Speech Recognition (Whisper or Faster-Whisper)
- 🧠 **LLM**: Local LLM inference (via Ollama running LLaMA3 8B)
- 🔊 **TTS**: Text-to-Speech using Edge-TTS
- 🛜 **FastAPI** backend
- 🧠 **Multi-turn memory** and optional wake-word support

---

## 📁 Folder Structure

homework3/
├── audio/ # Input/output audio files
├── main.py # FastAPI backend
├── llm_client.py # Local Ollama query module
├── tts.py # Edge TTS module
├── asr.py # ASR (Faster-Whisper or Whisper.cpp)
├── memory.py # Session-based memory handler
├── requirements.txt # Python dependencies
├── Dockerfile # Optional Docker deployment
├── README.md # Project instructions (this file)


---

## 🚀 Features

- Upload `.wav` files to `/voice-chat/` API and get `.mp3` replies
- Multi-turn memory using in-memory `session_id`
- Modular structure for ASR / LLM / TTS
- Supports both Whisper (Hugging Face) and Whisper.cpp / Vosk
- Local model inference using Ollama + LLaMA3
- Easily deployable via Docker

---

## 🛠️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt

###  🔁 API Usage
POST /voice-chat/
Send a .wav file and get AI voice reply.

Request:
curl -X POST http://localhost:8000/voice-chat/ \
  -F "audio=@user_input.wav" \
  -F "session_id=session123" \
  --output reply.mp3
🧠 Memory
Each session is tracked via session_id in memory.
You can extend memory.py to use Redis, SQLite, or LangChain memory later.

🐳 Docker Support
To run everything in Docker:

docker build -t voice-agent .
docker run -p 8000:8000 voice-agent
For Ollama model, run it on your host machine and ensure FastAPI inside Docker can reach http://host.docker.internal:11434

🧪 Future Work
Real-time streaming audio (WebSocket or MediaStream)

Wake-word detection via porcupine or VAD

Voice UI with Streamlit or web client

Local embedding + RAG integration

✍️ Author
Peter Liu
Assignment for: Machine Learning Engineer in the Generative AI Era

---

### ✅ 提交到 GitHub

在终端中执行：

```bash
cd ~/PeterLiu_Homework/homework3
touch README.md



git add README.md
git commit -m "Add voice agent README for homework3"
git push origin main
