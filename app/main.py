from fastapi import FastAPI
from .interfaces.api.routes import router
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="RAG AI Project API")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to RAG AI API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
