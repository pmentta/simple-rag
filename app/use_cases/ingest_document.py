from ..infrastructure.database.vector_store import VectorStore
from ..infrastructure.embeddings.gemini_embeddings import GeminiEmbeddings
from typing import List

class IngestDocument:
    def __init__(self, vector_store: VectorStore, embeddings: GeminiEmbeddings):
        self.vector_store = vector_store
        self.embeddings = embeddings

    def execute(self, content: str, title: str, metadata: dict) -> List[str]:
        # Simple chunking strategy (approx 300-500 tokens ~ 1500-2000 chars)
        # We'll use a simple overlap strategy
        chunk_size = 2000
        overlap = 200
        
        chunks = []
        if len(content) <= chunk_size:
            chunks.append(content)
        else:
            start = 0
            while start < len(content):
                end = start + chunk_size
                chunk = content[start:end]
                chunks.append(chunk)
                start += (chunk_size - overlap)
        
        doc_ids = []
        for i, chunk in enumerate(chunks):
            # Enrich metadata with chunk info
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
            
            # Generate embedding
            embedding = self.embeddings.get_embedding(chunk)
            
            # Save to vector store
            doc_id = self.vector_store.save_document(title, chunk, embedding, chunk_metadata)
            doc_ids.append(doc_id)
            
        return doc_ids
