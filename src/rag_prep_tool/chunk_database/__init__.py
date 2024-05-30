import chromadb
from pathlib import Path 
from tqdm import tqdm

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from rag_prep_tool.config import EMBEDDING_MODEL

def add_embeddings_to_chunks(chunks):
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL,trust_remote_code=True)
    Settings.embed_model = embed_model

    for chunk in tqdm(chunks):
      chunk.embedding = embed_model.get_text_embedding(chunk.text)
    return chunks

def store_chunks(chunks, db_path="./chroma_db", collection_name="rag_demo", index_dir="./chroma_db/index"):
    """
    Store chunks of data in a persistent Chroma database.

    Args:
        chunks (list): The data chunks to be stored.
        db_path (str): The path to the Chroma database.
        collection_name (str): The name of the collection in the Chroma database.
        index_dir (str): The directory to persist the index.

    Returns:
        None
    """
    
    """ Initialize the ChromaDB persistent client"""
    db = chromadb.PersistentClient(path=db_path)
    
    """ Get or create the specified collection """
    chroma_collection = db.get_or_create_collection(collection_name)

    """ Add embeddings to the chunks"""
    chunks = add_embeddings_to_chunks(chunks)
    
    """ Set up the ChromaVectorStore and load in data """
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    chunk_ids = vector_store.add(chunks)
    
    """ Create a VectorStoreIndex from the vector store """
    vector_store_llama_index = VectorStoreIndex.from_vector_store(vector_store)
    
    """ Set the index as a retriever """
    vector_store_llama_index.as_retriever()
    
    """ Persist the storage context to the specified directory """
    vector_store_llama_index.storage_context.persist(persist_dir=index_dir)

    return chunk_ids


if __name__ == "__main__":

    from rag_prep_tool.chunking import chunk_files
    from rag_prep_tool.chunking.map_metadata import map_chunks_with_metadata

    file_paths = [Path("output/art_of_happiness.txt")]
    chunks = chunk_files(file_paths)
    mapped_chunks = map_chunks_with_metadata(chunks, Path("output/art_of_happiness.json"))

    ids = store_chunks(mapped_chunks)