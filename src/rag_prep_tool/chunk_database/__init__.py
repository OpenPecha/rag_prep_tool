import chromadb
from pathlib import Path 
from tqdm import tqdm

from llama_index.core import VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore




from rag_prep_tool.config import EMBEDDING_MODEL

def add_embeddings_to_chunks(chunks):
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL,trust_remote_code=True)
    Settings.embed_model = embed_model

    for chunk in tqdm(chunks, desc="Adding embeddings to chunks"):
      chunk.embedding = embed_model.get_text_embedding(chunk.text)
    return chunks

def store_chunks(chunks, db_path="./chroma_db", collection_name="rag_demo", persist_dir="./chroma_db/index"):
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
    
    """ Persist the storage context to the specified directory """
    vector_store_llama_index.storage_context.persist(persist_dir=persist_dir)

    return chunk_ids

def load_chunks_from_database(db_path="./chroma_db", collection_name="rag_demo",persist_dir="./chroma_db/index"):
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL,trust_remote_code=True)
    Settings.embed_model = embed_model
    
    """ Initialize the Chroma persistent client """
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    """ Get or create the specified collection"""
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    
    """ Initialize the vector store with the specified collection """
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    """ Initialize the storage context with the vector store and persist directory """
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=persist_dir)
    
    """ Load the index from storage """
    vector_store_llama_index = load_index_from_storage(storage_context)
    
    return vector_store_llama_index



