import shutil 
from pathlib import Path 

from rag_prep_tool.vector_db.chunk_database import store_chunks
from rag_prep_tool.vector_db.chunking import chunk_files
from rag_prep_tool.vector_db.chunking.map_metadata import map_chunks_with_metadata




def test_store_chunks():
    DATA_DIR = Path(__file__).parent / "data"
    text_file_path = DATA_DIR / "art_of_happiness.txt"
    metadata_file_path = DATA_DIR / "art_of_happiness.json"

    file_paths = [text_file_path]
    all_chunks = chunk_files(file_paths)
    mapped_chunks = map_chunks_with_metadata(all_chunks, [metadata_file_path])

    database_path = DATA_DIR / "chroma_db"
    persist_path = database_path / "index"

    chunk_ids = store_chunks(mapped_chunks, db_path=str(database_path), collection_name="rag_demo", persist_dir=str(persist_path))

    """ Check that the number of chunk ids is equal to the number of mapped chunks """
    assert len(chunk_ids) == len(mapped_chunks)

    """ Check that the chunk ids are equal to the mapped chunks"""
    for chunk_id, chunk in zip(chunk_ids, mapped_chunks):
        assert chunk_id == chunk.id_
    
    """ Check that the database and persist directories exist """
    assert Path(database_path).exists()
    assert Path(persist_path).exists()
    """ Check that the SQLite database is created """
    assert Path(Path(database_path) / "chroma.sqlite3").exists()

    """ Clean up the database and persist directories """
    shutil.rmtree(database_path)


