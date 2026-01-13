# RAG AI Project

A clean architecture implementation of a Retrieval-Augmented Generation (RAG) system using FastAPI, OpenAI, and PGVector.

## Project Structure

```
rag_ai_project/
├── app/
│   ├── domain/             # Core business entities and repository interfaces
│   ├── use_cases/          # Business logic (Application layer)
│   ├── interfaces/         # API and External Clients (LLM)
│   ├── infrastructure/     # Database and External service implementations
│   └── main.py             # Entry point
├── scripts/                # Utility scripts
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup

1. **Environment Variables**:
   Create a `.env` file in the root with your OpenAI key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Initialize Database**:
   If not using Docker or for first time setup:
   ```bash
   python app/infrastructure/database/postgres.py
   ```

## Usage

### Ingest a document
```bash
python scripts/ingest_docs.py "Your knowledge base content goes here."
```

### Ask a question
Use the API at `POST /api/v1/ask`:
```json
{
  "text": "What is the content you just ingested?"
}
```
