# app_gpt4o_voice.py
import streamlit as st
import tempfile, json, re, time
from pathlib import Path
from sympy import sympify
import faster_whisper
import openai
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading

# ------------------ Config ------------------
openai.api_key = "OPENAI_API_KEY"  # GPT-4o Mini API Key

# ------------------ Tool Functions ------------------
def search_arxiv(query: str) -> str:
    return f"[arXiv snippet related to '{query}']"

def calculate(expression: str) -> str:
    try:
        # 清理表达式，只保留数字和运算符
        clean_expr = "".join(re.findall(r"[0-9\+\-\*\/\(\)\.]+", expression))
        if not clean_expr:
            return f"Cannot parse expression: {expression}"
        return str(sympify(clean_expr))
    except Exception as e:
        return f"Error: {e}"

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

# ------------------ GPT-4o Mini 调用 ------------------
def gpt4o_chat_model(user_text: str) -> str:
    """
    调用 GPT-4o Mini，并尝试返回函数调用 JSON 或文本
    """
    # 简单规则判断
    if any(char.isdigit() for char in user_text):
        return json.dumps({"function":"calculate","arguments":{"expression":user_text}})
    if "paper" in user_text.lower() or "arxiv" in user_text.lower():
        return json.dumps({"function":"search_arxiv","arguments":{"query":user_text}})
    
    # 向 GPT-4o Mini API 请求
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_text}],
        temperature=0.7
    )
    return response.choices[0].message["content"]

# ------------------ TTS (流式播放) ------------------
def tts_play_text(reply_text: str):
    """
    使用 pyttsx3 直接播放（非文件）
    """
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(reply_text)
    engine.runAndWait()

def tts_play_text_threaded(reply_text: str):
    t = threading.Thread(target=tts_play_text, args=(reply_text,))
    t.start()

# ------------------ Streamlit 前端 ------------------
st.title("GPT-4o Mini Real-Time Voice Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

audio_file = st.file_uploader("Upload or record your voice (.wav)", type=["wav"])
user_text = st.text_input("Or type your query:")

if st.button("Send"):
    full_text = user_text or ""
    
    # 显示 STT 识别中占位
    placeholder = st.empty()
    
    if audio_file:
        temp_audio = Path(tempfile.gettempdir()) / audio_file.name
        with open(temp_audio, "wb") as f:
            f.write(audio_file.getbuffer())
        
        # faster-whisper ASR
        model_asr = faster_whisper.WhisperModel("base", device="cpu")
        segments, _ = model_asr.transcribe(str(temp_audio))
        partial_text = ""
        for seg in segments:
            partial_text += seg.text + " "
            placeholder.text_area("Recognizing...", value=partial_text, height=100)
        full_text += " " + partial_text.strip()
    
    # GPT-4o Mini 输出
    llm_output = gpt4o_chat_model(full_text)
    reply_text = route_llm_output(llm_output)
    
    # 播放语音（线程）
    tts_play_text_threaded(reply_text)
    
    # 更新聊天记录
    st.session_state.chat_history.append(("user", user_text or "[audio]"))
    st.session_state.chat_history.append(("assistant", reply_text))

# 显示聊天记录
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
