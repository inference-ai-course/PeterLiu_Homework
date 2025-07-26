from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import gradio as gr

# 1. Prompt template to instruct the model to translate
prompt = PromptTemplate.from_template(
    "Translate the following sentence into {target_language}:\n\n{input_text}"
)

# 2. Initialize local Ollama model (e.g., llama2)
model = ChatOllama(model="llama2")

# 3. Build the LangChain pipeline
chain = (
    {"input_text": RunnablePassthrough(), "target_language": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 4. Define Gradio interface logic
def translate_text(input_text: str, target_language: str) -> str:
    return chain.invoke({
        "input_text": input_text,
        "target_language": target_language
    })

# 5. Create the Gradio UI
demo = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Textbox(label="Input Text"),
        gr.Dropdown(choices=["English", "Chinese", "French", "Spanish"], label="Target Language", value="Chinese")
    ],
    outputs=gr.Textbox(label="Translated Text"),
    title="Local AI Translator",
    description="Translate any sentence using a local LLM (Ollama + LangChain + Gradio)"
)

# 6. Launch the web app
if __name__ == "__main__":
    demo.launch()
