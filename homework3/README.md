# Homework 3 - Voice-Based AI Assistant (LLM + ASR + TTS)

## 📚 Project Overview

This project implements a local, modular **Voice Agent** powered by:

- 🎤 **ASR**: Converts speech to text (using Faster-Whisper or Whisper.cpp)
- 🧠 **LLM**: Responds intelligently using local Ollama (LLaMA3 or similar)
- 🔊 **TTS**: Converts text responses to speech using Edge TTS
- 🛜 **FastAPI**: Exposes the agent as a web API
- 🧠 **Memory**: Maintains multi-turn conversation history

---

## 📁 Folder Structure

bash

homework3/
├── audio/ # Stores input .wav and output .mp3 audio files
├── main.py # FastAPI backend: handles API requests
├── llm_client.py # Queries the local Ollama LLM
├── tts.py # Edge-TTS: converts text to speech
├── asr.py # ASR: transcribes audio via Faster-Whisper or Whisper.cpp
├── memory.py # In-memory conversation history manager
├── requirements.txt # Python dependencies
├── Dockerfile # Optional: build and run via Docker
├── README.md # Project documentation (this file)

---

## 🛠️ Setup & Installation

### 1. Install Python dependencies


pip install -r requirements.txt
### 2. Start your LLM (Ollama)

ollama run llama3
Make sure Ollama is installed and running: https://ollama.com
## 🚀 Run the API

uvicorn main:app --reload
Once running, access your API at:
http://localhost:8000/docs

## 🎧 Example: Voice Chat API
POST /voice-chat/
Send a .wav file and get a .mp3 voice response from the LLM.
curl -X POST http://localhost:8000/voice-chat/ \
  -F "audio=@audio/user_input.wav" \
  -F "session_id=test123" \
  --output audio/reply.mp3
Response:
A synthesized .mp3 audio file

Auto-saved multi-turn memory for the session

## 🧠 Memory Module
memory.py handles per-session conversation history.

Each session has its own list of message turns, useful for multi-turn LLM context.

Want persistent memory? Swap in Redis, SQLite, or LangChain.

## 🔊 ASR Options
You can choose:

Faster-Whisper (default): asr.py loads model via Hugging Face

Whisper.cpp or Vosk: supported with slight config changes

## 🔈 TTS: Edge-TTS
Uses Microsoft's edge-tts for fast and natural speech

Generates reply.mp3 in audio/ folder

## 🐳 Docker Support (Optional)
Build and run the entire service in a container:

docker build -t voice-agent .
docker run -p 8000:8000 voice-agent
Ollama must run outside Docker on your host machine
Inside container, access Ollama at http://host.docker.internal:11434

## 🧪 Future Work
✅ Real-time streaming audio input

✅ WebSocket API for live dialogue

🔴 Wake-word detection (e.g., with Porcupine or VAD)

🔴 UI client (React / Streamlit)

🔴 RAG with vector store + embeddings (personal docs)

## ✍️ Author
Peter Liu
Assignment for: Machine Learning Engineer in the Generative AI Era
GitHub: @Petercgliu
  


