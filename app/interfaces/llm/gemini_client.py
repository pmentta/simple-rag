import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self, model: str = "gemini-2.0-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_answer(self, prompt: str, context: str) -> str:
        # Construct the full prompt as requested
        final_prompt = f"""Você é um assistente que responde exclusivamente com base no contexto abaixo.

Contexto:
{context}

Pergunta:
{prompt}

Se a resposta não estiver no contexto, diga claramente que não encontrou a informação."""
        
        import time
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(final_prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):
                    if attempt < max_retries - 1:
                        sleep_time = 2 ** attempt * 2  # 2s, 4s, 8s
                        print(f"Quota exceeded, retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                raise e
