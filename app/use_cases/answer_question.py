from ..infrastructure.database.vector_store import VectorStore
from ..infrastructure.embeddings.gemini_embeddings import GeminiEmbeddings
from ..interfaces.llm.gemini_client import GeminiClient
from ..domain.entities.answer import Answer

class AnswerQuestion:
    def __init__(self, vector_store: VectorStore, embeddings: GeminiEmbeddings, llm_client: GeminiClient):
        self.vector_store = vector_store
        self.embeddings = embeddings
        self.llm_client = llm_client

    def execute(self, question_text: str) -> Answer:
        # 1. Get embedding for the question (using specific query embedding method)
        query_embedding = self.embeddings.get_query_embedding(question_text)
        
        # 2. Search for similar documents
        documents = self.vector_store.search_similar(query_embedding, limit=5)
        
        # 3. Build context
        context_parts = []
        for doc in documents:
            context_parts.append(f"Source: {doc.title}\nContent: {doc.content}")
        
        context = "\n\n".join(context_parts)
        
        # 4. Generate answer using LLM
        answer_text = self.llm_client.generate_answer(question_text, context)
        
        return Answer(text=answer_text, sources=documents)
