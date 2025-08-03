import asyncio
import edge_tts

async def generate_edge_wav(text, filename="user_input.wav"):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(filename)
    print(f"✅ 语音保存完成: {filename}")

asyncio.run(generate_edge_wav("You are a doctor, please explain what causes back pain."))
