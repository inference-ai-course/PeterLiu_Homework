# voice_tcm_agent.py
import os
import numpy as np
import streamlit as st
import speech_recognition as sr
import openai
from dotenv import load_dotenv
from pathlib import Path
from tempfile import NamedTemporaryFile
from gtts import gTTS

# ---------- 初始化 ----------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="TCM Voice Assistant", page_icon="🌿", layout="wide")

# 本地知识库
KB_TEXTS = [
"感冒多风寒，宜生姜红糖水。针灸穴位：风池、合谷、足三里。",
"咳嗽痰多，常用二陈汤。针灸穴位：肺俞、列缺、天突。",
"失眠多因心脾两虚，可用酸枣仁汤。针灸穴位：神门、三阴交、百会。",
"肝火旺盛，容易头痛，常用龙胆泻肝汤。针灸穴位：太冲、风池、百会。",
"脾胃虚弱，食欲不振，可用参苓白术散。针灸穴位：足三里、中脘、三阴交。",
"风热感冒，咽喉肿痛，可用银翘散。针灸穴位：风池、曲池、合谷。",
"湿热下注，带下异常，可用二妙丸。针灸穴位：关元、三阴交、阴陵泉。",
"肾虚腰痛，夜间频尿，可用右归丸。针灸穴位：肾俞、命门、腰阳关。",
"血虚面色萎黄，心悸失眠，可用归脾汤。针灸穴位：心俞、脾俞、神门。",
"肝气郁结，情绪抑郁，可用柴胡疏肝散。针灸穴位：太冲、期门、合谷。",
"痰湿阻肺，咳嗽痰多，胸闷气短，可用二陈汤加减。针灸穴位：肺俞、中府、足三里。",
"气虚乏力，易出汗，可用补中益气汤。针灸穴位：足三里、气海、中脘。",
"心脾两虚，健忘失眠，可用酸枣仁汤加养心汤。针灸穴位：神门、心俞、三阴交。",
"肝阳上亢，头晕目眩，可用天麻钩藤饮。针灸穴位：风池、太冲、百会。",
"痰湿中阻，身体肥胖，舌苔厚腻，可用防己黄芪汤。针灸穴位：足三里、丰隆、中脘。",
"风湿痹痛，关节酸麻，可用独活寄生汤。针灸穴位：阳陵泉、阿是穴、三阴交。",
"肾阴虚，口燥咽干，潮热盗汗，可用知柏地黄丸。针灸穴位：肾俞、太溪、三阴交。",
"气滞血瘀，胸闷痛经，可用血府逐瘀汤。针灸穴位：膻中、血海、太冲。",
"痰热内扰，小儿惊风，可用安神定惊丸。针灸穴位：百会、风池、涌泉。",
"湿热痢疾，腹泻脓血，可用葛根芩连汤。针灸穴位：天枢、足三里、大肠俞。",
"胃阴虚，口干咽燥，消化不良，可用沙参麦冬汤。针灸穴位：中脘、足三里、内关。",
"风寒湿痹，关节疼痛，可用桂枝芍药知母汤。针灸穴位：阿是穴、风市、曲池。",
"肝血虚，面色苍白，头晕眼花，可用四物汤。针灸穴位：太冲、血海、足三里。",
"肾阳虚，畏寒肢冷，腰膝酸软，可用肾气丸。针灸穴位：肾俞、命门、腰阳关。",
"气血两虚，倦怠乏力，面色无华，可用八珍汤。针灸穴位：足三里、气海、三阴交。",
"痰湿困脾，胸闷恶心，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"肝火上炎，目赤口苦，可用龙胆泻肝汤。针灸穴位：太冲、睛明、风池。",
"肺阴虚，干咳少痰，可用沙参麦冬汤。针灸穴位：肺俞、尺泽、列缺。",
"风寒表证，头痛发热，可用麻黄汤。针灸穴位：风池、合谷、曲池。",
"风热表证，咳嗽咽痛，可用银翘散。针灸穴位：风池、曲池、大椎。",
"脾气虚，食少乏力，可用补中益气汤。针灸穴位：足三里、气海、中脘。",
"血瘀痛经，经行不畅，可用血府逐瘀汤。针灸穴位：关元、三阴交、血海。",
"肾阴虚，腰膝酸软，潮热盗汗，可用六味地黄丸。针灸穴位：肾俞、太溪、三阴交。",
"心火亢盛，失眠多梦，可用黄连阿胶汤。针灸穴位：神门、心俞、三阴交。",
"脾虚泄泻，腹泻久不愈，可用参苓白术散。针灸穴位：中脘、足三里、脾俞。",
"肝气郁结，胸闷胁痛，可用柴胡疏肝散。针灸穴位：期门、太冲、膻中。",
"痰湿阻络，眩晕耳鸣，可用半夏白术天麻汤。针灸穴位：风池、足三里、百会。",
"气滞血瘀，胸痹心痛，可用丹参饮。针灸穴位：膻中、心俞、内关。",
"风寒咳嗽，咳痰白稀，可用杏苏散。针灸穴位：肺俞、列缺、合谷。",
"风热咳嗽，咽喉肿痛，可用桑菊饮。针灸穴位：肺俞、列缺、风池。",
"湿热黄疸，口苦身黄，可用茵陈蒿汤。针灸穴位：肝俞、胆俞、三阴交。",
"肾虚耳鸣，听力下降，可用左归丸。针灸穴位：肾俞、听会、太溪。",
"气虚自汗，易感冒，可用玉屏风散。针灸穴位：足三里、气海、肺俞。",
"血虚头晕，面色苍白，可用当归补血汤。针灸穴位：血海、足三里、三阴交。",
"肝阳偏亢，眩晕头痛，可用天麻钩藤饮。针灸穴位：风池、太冲、百会。",
"痰浊困脾，胸闷纳呆，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"湿热带下，阴痒色黄，可用二妙丸。针灸穴位：关元、三阴交、阴陵泉。",
"风湿痹痛，肢体酸麻，可用独活寄生汤。针灸穴位：阿是穴、阳陵泉、三阴交。",
"肾阳不足，腰膝冷痛，可用右归丸。针灸穴位：肾俞、命门、腰阳关。",
"肾阴不足，潮热盗汗，可用知柏地黄丸。针灸穴位：肾俞、太溪、三阴交。",
"心脾两虚，失眠健忘，可用归脾汤。针灸穴位：心俞、神门、三阴交。",
"气血两虚，倦怠乏力，可用八珍汤。针灸穴位：足三里、气海、三阴交。",
"肝血虚，目眩，面色苍白，可用四物汤。针灸穴位：太冲、血海、足三里。",
"脾虚湿盛，肢体沉重，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"气滞血瘀，痛经胸闷，可用血府逐瘀汤。针灸穴位：关元、三阴交、血海。",
"痰热扰心，惊悸多梦，可用安神定惊丸。针灸穴位：百会、风池、神门。",
"风寒表证，头痛身痛，可用桂枝汤。针灸穴位：风池、合谷、曲池。",
"风热表证，咳嗽咽痛，可用银翘散。针灸穴位：风池、曲池、大椎。",
"脾胃虚弱，食少纳呆，可用参苓白术散。针灸穴位：足三里、中脘、脾俞。",
"气虚乏力，出汗自汗，可用补中益气汤。针灸穴位：气海、足三里、中脘。",
"肝郁气滞，胸胁胀痛，可用柴胡疏肝散。针灸穴位：期门、太冲、膻中。",
"痰湿阻肺，咳痰胸闷，可用二陈汤加减。针灸穴位：肺俞、中府、足三里。",
"肾虚腰痛，夜尿频多，可用右归丸。针灸穴位：肾俞、命门、腰阳关。",
"心血虚，失眠多梦，可用酸枣仁汤加养心汤。针灸穴位：神门、心俞、三阴交。",
"肝火上炎，头痛目赤，可用龙胆泻肝汤。针灸穴位：太冲、风池、睛明。",
"脾虚泄泻，腹泻久不愈，可用参苓白术散。针灸穴位：中脘、足三里、脾俞。",
"风湿痹痛，关节酸麻，可用独活寄生汤。针灸穴位：阿是穴、阳陵泉、三阴交。",
"痰湿中阻，眩晕耳鸣，可用半夏白术天麻汤。针灸穴位：风池、足三里、百会。",
"血瘀痛经，经行不畅，可用血府逐瘀汤。针灸穴位：关元、三阴交、血海。",
"气虚自汗，易感冒，可用玉屏风散。针灸穴位：足三里、气海、肺俞。",
"湿热黄疸，口苦身黄，可用茵陈蒿汤。针灸穴位：肝俞、胆俞、三阴交。",
"肾虚耳鸣，听力下降，可用左归丸。针灸穴位：肾俞、听会、太溪。",
"风寒咳嗽，咳痰白稀，可用杏苏散。针灸穴位：肺俞、列缺、合谷。",
"风热咳嗽，咽喉肿痛，可用桑菊饮。针灸穴位：肺俞、列缺、风池。",
"脾气虚，食少乏力，可用补中益气汤。针灸穴位：足三里、气海、中脘。",
"肝阳偏亢，眩晕头痛，可用天麻钩藤饮。针灸穴位：风池、太冲、百会。",
"痰浊困脾，胸闷纳呆，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"湿热带下，阴痒色黄，可用二妙丸。针灸穴位：关元、三阴交、阴陵泉。",
"肾阳不足，腰膝冷痛，可用右归丸。针灸穴位：肾俞、命门、腰阳关。",
"肾阴不足，潮热盗汗，可用知柏地黄丸。针灸穴位：肾俞、太溪、三阴交。",
"心脾两虚，失眠健忘，可用归脾汤。针灸穴位：心俞、神门、三阴交。",
"气血两虚，倦怠乏力，可用八珍汤。针灸穴位：足三里、气海、三阴交。",
"肝血虚，目眩，面色苍白，可用四物汤。针灸穴位：太冲、血海、足三里。",
"脾虚湿盛，肢体沉重，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"气滞血瘀，痛经胸闷，可用血府逐瘀汤。针灸穴位：关元、三阴交、血海。",
"痰热扰心，惊悸多梦，可用安神定惊丸。针灸穴位：百会、风池、神门。",
"风寒表证，头痛身痛，可用桂枝汤。针灸穴位：风池、合谷、曲池。",
"风热表证，咳嗽咽痛，可用银翘散。针灸穴位：风池、曲池、大椎。",
"脾胃虚弱，食少纳呆，可用参苓白术散。针灸穴位：足三里、中脘、脾俞。",
"气虚乏力，出汗自汗，可用补中益气汤。针灸穴位：气海、足三里、中脘。",
"肝郁气滞，胸胁胀痛，可用柴胡疏肝散。针灸穴位：期门、太冲、膻中。",
"痰湿阻肺，咳痰胸闷，可用二陈汤加减。针灸穴位：肺俞、中府、足三里。",
"肾虚腰痛，夜尿频多，可用右归丸。针灸穴位：肾俞、命门、腰阳关。",
"心血虚，失眠多梦，可用酸枣仁汤加养心汤。针灸穴位：神门、心俞、三阴交。",
"肝火上炎，头痛目赤，可用龙胆泻肝汤。针灸穴位：太冲、风池、睛明。",
"脾虚泄泻，腹泻久不愈，可用参苓白术散。针灸穴位：中脘、足三里、脾俞。",
"风湿痹痛，关节酸麻，可用独活寄生汤。针灸穴位：阿是穴、阳陵泉、三阴交。",
"痰湿中阻，眩晕耳鸣，可用半夏白术天麻汤。针灸穴位：风池、足三里、百会。",
"血瘀痛经，经行不畅，可用血府逐瘀汤。针灸穴位：关元、三阴交、血海。",
"气虚自汗，易感冒，可用玉屏风散。针灸穴位：足三里、气海、肺俞。",
"湿热黄疸，口苦身黄，可用茵陈蒿汤。针灸穴位：肝俞、胆俞、三阴交。",
"肾虚耳鸣，听力下降，可用左归丸。针灸穴位：肾俞、听会、太溪。",
"风寒咳嗽，咳痰白稀，可用杏苏散。针灸穴位：肺俞、列缺、合谷。",
"风热咳嗽，咽喉肿痛，可用桑菊饮。针灸穴位：肺俞、列缺、风池。",
"脾气虚，食少乏力，可用补中益气汤。针灸穴位：足三里、气海、中脘。",
"肝阳偏亢，眩晕头痛，可用天麻钩藤饮。针灸穴位：风池、太冲、百会。",
"痰浊困脾，胸闷纳呆，可用平胃散。针灸穴位：中脘、足三里、丰隆。",
"湿热带下，阴痒色黄，可用二妙丸。针灸穴位：关元、三阴交、阴陵泉。"
]
INDEX_FILE = "kb_index.npy"

# ---------- 知识库检索 ----------
def get_embedding(text, model="text-embedding-3-small"):
    resp = openai.Embedding.create(model=model, input=text)
    return resp["data"][0]["embedding"]

def build_kb_index():
    if os.path.exists(INDEX_FILE):
        data = np.load(INDEX_FILE, allow_pickle=True).item()
        return data["texts"], data["vectors"]
    vectors = [get_embedding(t) for t in KB_TEXTS]
    np.save(INDEX_FILE, {"texts": KB_TEXTS, "vectors": vectors})
    return KB_TEXTS, vectors

def retrieve(query, texts, vectors, top_k=1):
    q_emb = get_embedding(query)
    sims = [np.dot(q_emb, v) / (np.linalg.norm(q_emb) * np.linalg.norm(v)) for v in vectors]
    top_idx = int(np.argmax(sims))
    return texts[top_idx]

def ask_gpt(query, context):
    prompt = f"你是中医助手。结合以下知识回答：\n知识：{context}\n用户：{query}\n助手："
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp["choices"][0]["message"]["content"]

# ---------- gTTS ----------
def tts_gtts(text):
    try:
        tts = gTTS(text=text, lang="zh")
        tmp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        st.warning(f"TTS 生成失败: {e}")
        return None

# ---------- 自动检测麦克风 ----------
def get_microphone():
    try:
        mic = sr.Microphone()
        print("✅ 使用 PyAudio 麦克风")
        return mic
    except (AttributeError, OSError):
        try:
            import sounddevice  # noqa
            sr.Microphone.device_index = None
            mic = sr.Microphone()
            print("✅ 使用 SoundDevice 麦克风")
            return mic
        except Exception as e:
            raise RuntimeError("没有可用音频输入，请安装 PyAudio 或 sounddevice") from e

def recognize_speech():
    r = sr.Recognizer()
    mic = get_microphone()
    with mic as source:
        st.info("🎤 请讲话中...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio, language="zh-CN")
        return text
    except sr.UnknownValueError:
        return "无法识别语音"
    except sr.RequestError as e:
        return f"语音识别出错: {e}"

# ---------- 聊天气泡 ----------
def chat_bubble(message, role="assistant"):
    if role == "user":
        st.markdown(
            f"""
            <div style='text-align: right; margin:10px;'>
                <span style='background:#DCF8C6; padding:10px; border-radius:10px; display:inline-block;'>
                    {message}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align: left; margin:10px;'>
                <span style='background:#F1F0F0; padding:10px; border-radius:10px; display:inline-block;'>
                    {message}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------- Streamlit 界面 ----------
def main():
    st.title("🌿 中医语音助手 TCM Voice Assistant")
    st.write("演示用途，不构成医疗建议。")
    st.markdown("<p style='color:gray;'>基于 RAG + GPT + gTTS</p>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []
    if "texts" not in st.session_state:
        st.session_state.texts, st.session_state.vectors = build_kb_index()

    # 文本模式输入
    query = st.text_input("请输入您的问题：", "")
    if st.button("💬 提交文本问题") and query:
        ctx = retrieve(query, st.session_state.texts, st.session_state.vectors)
        ans = ask_gpt(query, ctx)
        st.session_state.history.append(("user", query))
        st.session_state.history.append(("assistant", ans))

        # TTS
        audio_file = tts_gtts(ans)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")

    # 语音模式输入
    if st.button("🎤 语音提问"):
        query = recognize_speech()
        st.session_state.history.append(("user", query))
        ctx = retrieve(query, st.session_state.texts, st.session_state.vectors)
        ans = ask_gpt(query, ctx)
        st.session_state.history.append(("assistant", ans))

        audio_file = tts_gtts(ans)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")

    # 对话历史展示
    st.markdown("## 💬 对话历史")
    for role, msg in st.session_state.history:
        chat_bubble(msg, role=role)

if __name__ == "__main__":
    main()
