from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ...use_cases.answer_question import AnswerQuestion
from ...use_cases.ingest_document import IngestDocument
from ...infrastructure.database.vector_store import VectorStore
from ...infrastructure.embeddings.gemini_embeddings import GeminiEmbeddings
from ...interfaces.llm.gemini_client import GeminiClient

router = APIRouter()

# Dependency injection
# In a production app, use FastAPI's Depends
vector_store = VectorStore()
try:
    embeddings = GeminiEmbeddings()
    llm_client = GeminiClient()
    ingest_use_case = IngestDocument(vector_store, embeddings)
    answer_use_case = AnswerQuestion(vector_store, embeddings, llm_client)
except Exception as e:
    print(f"Error initializing services: {e}")
    # We allow the app to start even if keys are missing, but endpoints will fail
    ingest_use_case = None
    answer_use_case = None

class QuestionRequest(BaseModel):
    text: str

class DocumentRequest(BaseModel):
    title: str
    content: str
    metadata: Optional[dict] = {}

class SourceResponse(BaseModel):
    title: str
    content: str
    metadata: dict

class AnswerResponse(BaseModel):
    answer: str
    sources: List[SourceResponse]

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    if not answer_use_case:
         raise HTTPException(status_code=500, detail="Services not initialized. Check API Key.")
    
    try:
        result = answer_use_case.execute(request.text)
        sources = [SourceResponse(title=doc.title, content=doc.content, metadata=doc.metadata) for doc in result.sources]
        return AnswerResponse(answer=result.text, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest")
async def ingest_document(request: DocumentRequest):
    if not ingest_use_case:
        raise HTTPException(status_code=500, detail="Services not initialized. Check API Key.")
        
    try:
        doc_ids = ingest_use_case.execute(request.content, request.title, request.metadata)
        return {"status": "success", "document_ids": doc_ids, "count": len(doc_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
