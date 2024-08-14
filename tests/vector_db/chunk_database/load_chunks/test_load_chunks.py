import shutil 
from pathlib import Path 

from rag_prep_tool.vector_db.chunk_database import load_chunks_from_database
from llama_index.core.indices.vector_store.base import VectorStoreIndex

def test_load_chunks():
    DATA_DIR = Path(__file__).parent / "data"
    database_path = DATA_DIR / "chroma_db"
    collection_name = "rag_demo"
    persist_path = database_path / "index"
    
    chunks_vectors = load_chunks_from_database(str(database_path), collection_name, str(persist_path))
    assert isinstance(chunks_vectors, VectorStoreIndex)



