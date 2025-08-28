# backend.py
from fastapi import FastAPI, File, Form, UploadFile
import json
import tempfile
from pathlib import Path
from sympy import sympify
import soundfile as sf
import pyttsx3
import faster_whisper

app = FastAPI()


# -------- 工具函数 --------
def search_arxiv(query: str) -> str:
    return f"[arXiv snippet related to '{query}']"

def calculate(expression: str) -> str:
    try:
        return str(sympify(expression))
    except Exception as e:
        return f"Error: {e}"

# -------- 函数调用路由 --------
def route_llm_output(llm_output: str) -> str:
    try:
        output = json.loads(llm_output)
        func_name = output.get("function")
        args = output.get("arguments", {})
    except:
        return llm_output
    if func_name == "search_arxiv":
        return search_arxiv(args.get("query",""))
    if func_name == "calculate":
        return calculate(args.get("expression",""))
    return f"Error: Unknown function '{func_name}'"

# -------- LLM 模拟调用 --------
def llama3_chat_model(user_text: str) -> str:
    if any(char.isdigit() for char in user_text):
        return json.dumps({"function":"calculate","arguments":{"expression":"2+2"}})
    if "paper" in user_text or "arxiv" in user_text:
        return json.dumps({"function":"search_arxiv","arguments":{"query":"quantum entanglement"}})
    return "Hello! How can I help?"

# -------- API Endpoint --------
@app.post("/api/voice-query/")
async def voice_query_endpoint(text: str = Form(...), audio: UploadFile = File(None)):
    user_text = text
    if audio:
        # 保存音频
        temp_file = Path(tempfile.gettempdir()) / audio.filename
        with open(temp_file, "wb") as f:
            f.write(audio.file.read())
        # 使用 faster-whisper 进行 ASR
        model = faster_whisper.WhisperModel("base", device="cpu")  # 选 cpu / cuda
        segments, _ = model.transcribe(str(temp_file))
        user_text += " " + " ".join([seg.text for seg in segments])

    # LLM 输出函数调用或文本
    llm_output = llama3_chat_model(user_text)
    reply_text = route_llm_output(llm_output)

    # TTS 输出音频文件
    tts_file = Path(tempfile.gettempdir()) / "response.wav"
    engine = pyttsx3.init()
    engine.save_to_file(reply_text, str(tts_file))
    engine.runAndWait()

    return {"response": reply_text, "tts_path": str(tts_file)}
