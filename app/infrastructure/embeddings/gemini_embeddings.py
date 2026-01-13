import google.generativeai as genai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class GeminiEmbeddings:
    def __init__(self, model: str = "models/text-embedding-004"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = model

    def get_embedding(self, text: str) -> List[float]:
        # Gemini embedding-004 returns 768 dimensions by default
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def get_query_embedding(self, text: str) -> List[float]:
        # Specific task type for queries ensures better retrieval
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
