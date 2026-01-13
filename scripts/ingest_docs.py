import sys
import os
import glob

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.use_cases.ingest_document import IngestDocument
from app.infrastructure.database.vector_store import VectorStore
from app.infrastructure.embeddings.gemini_embeddings import GeminiEmbeddings

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest_docs.py <path_to_txt_files_or_content>")
        sys.exit(1)
        
    input_arg = sys.argv[1]
    
    # Initialize services
    try:
        vector_store = VectorStore()
        embeddings = GeminiEmbeddings()
        ingestor = IngestDocument(vector_store, embeddings)
    except Exception as e:
        print(f"Error initializing: {e}")
        return

    # Check if input is a directory or file
    files_to_ingest = []
    
    if os.path.isdir(input_arg):
        files_to_ingest = glob.glob(os.path.join(input_arg, "*.txt"))
    elif os.path.isfile(input_arg):
        files_to_ingest = [input_arg]
    else:
        # Treat as raw string content
        print("Ingesting raw string content...")
        doc_ids = ingestor.execute(input_arg, "Manual Input", {"source": "cli"})
        print(f"Ingested {len(doc_ids)} chunks.")
        return

    print(f"Found {len(files_to_ingest)} files to ingest.")
    
    for file_path in files_to_ingest:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            title = os.path.basename(file_path)
            print(f"Ingesting {title}...")
            try:
                doc_ids = ingestor.execute(content, title, {"source": file_path})
                print(f"  -> Created {len(doc_ids)} chunks.")
            except Exception as e:
                print(f"  -> Error: {e}")

if __name__ == "__main__":
    main()
