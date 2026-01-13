import psycopg2
from pgvector.psycopg2 import register_vector
from typing import List
import os
import json
from ...domain.entities.document import Document

class VectorStore:
    def __init__(self):
        # We need to be careful with connection management in a real app (connection pool preferred)
        # For this example, we reconnect on init or handle it simply.
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "rag_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        self.conn.autocommit = True
        register_vector(self.conn)

    def save_document(self, title: str, content: str, embedding: List[float], metadata: dict) -> str:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (title, content, embedding, metadata)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (title, content, embedding, json.dumps(metadata))
            )
            return str(cur.fetchone()[0])

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Document]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, content, metadata, created_at
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, limit)
            )
            results = cur.fetchall()
            documents = []
            for r in results:
                meta = json.loads(r[3]) if r[3] else {}
                documents.append(Document(
                    id=str(r[0]),
                    title=r[1],
                    content=r[2],
                    metadata=meta,
                    created_at=r[4]
                ))
            return documents
