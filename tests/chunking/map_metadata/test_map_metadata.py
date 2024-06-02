from pathlib import Path 

from nltk.tokenize import word_tokenize
from llama_index.core.schema import TextNode

from rag_prep_tool.chunking import chunk_files
from rag_prep_tool.chunking.map_metadata import map_chunks_with_metadata

def test_sentence_splitter():
    DATA_DIR = Path(__file__).parent / "data"
    text_file_path = DATA_DIR / "ethics_for_new_millennium_chapter_1_first_page.txt"
    metadata_file_path = DATA_DIR / "art_of_happiness.json"
    chunk_size = 500
    chunk_overlap = 50
    chunks = chunk_files([text_file_path], chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    """ before mapping metadata"""
    for chunk in chunks:
        assert isinstance(chunk, TextNode)
        chunk_metadata = chunk.metadata
        assert "book_title" not in chunk_metadata
        assert "page_no" not in chunk_metadata
        assert "chapter" not in chunk_metadata

    """ after mapping metadata"""
    mapped_chunks = map_chunks_with_metadata(chunks, metadata_file_path)
    for chunk in mapped_chunks:
        assert isinstance(chunk, TextNode)
        chunk_metadata = chunk.metadata
        assert "book_title" in chunk_metadata
        assert "page_no" in chunk_metadata
        assert "chapter" in chunk_metadata

test_sentence_splitter()