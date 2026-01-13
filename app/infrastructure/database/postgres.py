import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    # Use localhost if running script locally, or DB_HOST if inside container
    db_host = os.getenv("DB_HOST", "localhost")
    conn = psycopg2.connect(
        host=db_host,
        database=os.getenv("DB_NAME", "rag_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        
        # Drop table if exists to ensure schema update (Development only behavior)
        cur.execute("DROP TABLE IF EXISTS documents")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                title TEXT,
                content TEXT,
                embedding vector(768),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Create IVFFlat index for faster search (optional but good practice)
        # Using cosine distance (vector_cosine_ops)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx 
            ON documents USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)
        
    conn.commit()
    conn.close()
    print("Database initialized successfully with 768-dim vector support.")

if __name__ == "__main__":
    init_db()
