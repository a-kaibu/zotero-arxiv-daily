import os
from openai import OpenAI
from loguru import logger
from time import sleep
from dotenv import load_dotenv

load_dotenv(override=True)

DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "hf.co/mmnga-o/NVIDIA-Nemotron-Nano-9B-v2-Japanese-gguf:Q4_K_M")
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"

GLOBAL_LLM = None

class LLM:
    def __init__(self, model: str = None, lang: str = "English"):
        self.llm = OpenAI(api_key="ollama", base_url=DEFAULT_OLLAMA_BASE_URL)
        self.model = model or DEFAULT_MODEL_NAME
        self.lang = lang

    def generate(self, messages: list[dict]) -> str:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.llm.chat.completions.create(messages=messages, temperature=0, model=self.model)
                break
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                sleep(3)
        return response.choices[0].message.content

def set_global_llm(model: str = None, lang: str = "English"):
    global GLOBAL_LLM
    GLOBAL_LLM = LLM(model=model, lang=lang)

def get_llm() -> LLM:
    if GLOBAL_LLM is None:
        logger.info("No global LLM found, creating a default one. Use `set_global_llm` to set a custom one.")
        set_global_llm()
    return GLOBAL_LLM
