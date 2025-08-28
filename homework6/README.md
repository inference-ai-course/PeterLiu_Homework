# Voice Agent with Function Calling (Local Deployment)

This is a **locally deployable voice assistant** that supports:

- Text or audio input (Streamlit frontend)
- Offline speech-to-text (STT) using `faster-whisper`
- Function calling:
  - `calculate(expression)` → math calculation
  - `search_arxiv(query)` → simulated arXiv paper search
- Text-to-speech (TTS) using `pyttsx3`
- Multi-turn chat history display
- Minimal local setup, no cloud services required

---

## 1️⃣ Install Dependencies


# Recommended: use a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
## 2️⃣ Start Backend FastAPI

uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
Visit http://localhost:8000/docs for API documentation
 ##  3️⃣ Start Frontend Streamlit
In another terminal:


streamlit run app.py
Open browser: http://localhost:8501

Upload a .wav audio file or type your query

Click Send to interact with the voice assistant

Text and TTS audio will be returned

## 4️⃣ Example Queries
User Input	Response Type	Output
"2+3"	Function call calculate	"5"
"Find papers on quantum entanglement"	Function call search_arxiv	"[arXiv snippet related to 'quantum entanglement']"
"Hello!"	Normal text	"Hello! How can I help?"

## 5️⃣ Extensibility
Add more tool functions → just implement in backend.py and register

Swap STT/TTS libraries for streaming real-time voice

Replace LLM call with Llama 3 / GPT-4 function calling API

## 6️⃣ Notes
Make sure audio files are in .wav format to avoid decoding errors

faster-whisper can run on CPU or GPU (GPU recommended for speed)

TTS uses pyttsx3 to generate WAV files, playable directly in Streamlit