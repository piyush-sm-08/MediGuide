import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM

load_dotenv()
url = os.getenv("OLLAMA_BASE_URL")
model_name = os.getenv("OLLAMA_MODEL")

llm = OllamaLLM(
    base_url=url,
    model=model_name
)
print(llm.invoke("Say hello"))
print(llm.invoke("tell me a story in 2000 words"))
