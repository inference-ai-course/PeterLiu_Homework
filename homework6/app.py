# app.py
import streamlit as st
import requests
import tempfile
from pathlib import Path

st.title("Voice Agent (Streaming STT + TTS)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 前端实时录音：上传音频或文本
audio_file = st.file_uploader("Record or upload your voice (wav)", type=["wav"])
user_text = st.text_input("Or type your query:")

if st.button("Send"):
    if audio_file:
        temp_audio = Path(tempfile.gettempdir()) / audio_file.name
        with open(temp_audio, "wb") as f:
            f.write(audio_file.getbuffer())
        resp = requests.post(
            "http://localhost:8000/api/voice-query/",
            files={"audio": open(temp_audio, "rb")},
            data={"text": user_text}
        ).json()
    else:
        resp = requests.post(
            "http://localhost:8000/api/voice-query/",
            data={"text": user_text}
        ).json()
    
    st.session_state.chat_history.append(("user", user_text or "[audio]"))
    st.session_state.chat_history.append(("assistant", resp.get("response", "")))

# 显示聊天记录
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
