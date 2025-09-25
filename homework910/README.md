# TCM Voice Assistant Demo (RAG + GPT + gTTS)

A **Streamlit** demo for a Traditional Chinese Medicine (TCM) voice assistant.  
It combines:

- **RAG (Retrieval-Augmented Generation)**: Retrieve answers from a local TCM knowledge base  
- **GPT-4o-mini**: Generate natural language responses  
- **gTTS**: High-quality Chinese text-to-speech playback  
- **Speech Recognition**: Users can ask questions via voice  
- **Chat History**: Conversation bubbles like ChatGPT  

---

## Features

1. **Text Input Mode** – type your question, get GPT answer + TTS playback  
2. **Voice Input Mode** – speak your question, get GPT answer + TTS playback  
3. **Conversation History** – chat bubbles: user messages on the right (green), assistant messages on the left (gray)  
4. Works with PyAudio or SoundDevice for microphone input  
5. Cross-platform audio playback with gTTS + playsound  

---

## Tech Stack

- [Streamlit](https://streamlit.io/)  
- [OpenAI GPT API](https://platform.openai.com/)  
- [gTTS](https://pypi.org/project/gTTS/) – Chinese text-to-speech  
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – voice input  
- [playsound](https://pypi.org/project/playsound/) – audio playback  
- [numpy](https://numpy.org/) – vector similarity  
- [python-dotenv](https://pypi.org/project/python-dotenv/) – load API key from `.env`  

---

## Setup

1. Clone or download the project.  
2. Install Python >= 3.10.  
3. Install dependencies:

```bash
pip install streamlit openai python-dotenv numpy SpeechRecognition gTTS playsound sounddevice

voice_tcm_agent/
│
├── voice_tcm_agent.py    # main Streamlit app
├── kb_index.npy          # optional cached knowledge embeddings
├── requirements.txt      # dependencies
├── README.md             # this file
└── .env                  # your OpenAI API key

