# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel
import requests, uuid, os, asyncio
import edge_tts
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

app = FastAPI(title="🧠 Voice Agent API")

# 🔧 Init components
asr_model = WhisperModel("base", device="cpu", compute_type="int8")
chat_history = {}  # {session_id: [turns]}


# ========== 🔊 TTS ==========
async def text_to_speech(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await communicate.save(output_path)


# ========== 🤖 LLM ==========
def query_ollama(prompt: str, session_id: str):
    history = chat_history.get(session_id, [])
    full_prompt = "\n".join(history + [f"User: {prompt}", "Assistant:"])
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1:8b", "prompt": full_prompt, "stream": False}
    )
    response = res.json()["response"].strip()
    # Update history
    history.append(f"User: {prompt}")
    history.append(f"Assistant: {response}")
    chat_history[session_id] = history[-10:]  # Keep last 5 turns
    return response


# ========== 🎧 Voice Chat Endpoint ==========
@app.post("/voice-chat/")
async def voice_chat(audio: UploadFile = File(...), session_id: str = None):
    session_id = session_id or str(uuid.uuid4())

    # Save uploaded audio
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_in:
        audio_bytes = await audio.read()
        tmp_in.write(audio_bytes)
        tmp_in_path = tmp_in.name

    # --- 1. ASR ---
    segments, _ = asr_model.transcribe(tmp_in_path)
    text = "".join([seg.text for seg in segments]).strip()
    print(f"[ASR] {text}")

    # --- 2. LLM ---
    reply = query_ollama(text, session_id)
    print(f"[LLM] {reply}")

    # --- 3. TTS ---
    output_audio_path = f"reply_{session_id}.mp3"
    await text_to_speech(reply, output_audio_path)

    return FileResponse(output_audio_path, media_type="audio/mpeg")


# ========== 🧹 Reset Session ==========
@app.post("/reset/")
def reset(session_id: str):
    chat_history.pop(session_id, None)
    return {"message": f"Session {session_id} cleared."}
