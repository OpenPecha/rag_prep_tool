import nltk 
from pathlib import Path 
from nltk.tokenize import word_tokenize
from llama_index.core.schema import TextNode

from rag_prep_tool.chunking import chunk_files

nltk.download('punkt')


def test_sentence_splitter():
    DATA_DIR = Path(__file__).parent / "data"
    text_file_path = DATA_DIR / "ethics_for_new_millennium_chapter_1_first_page.txt"
    
    chunk_size = 500
    chunk_overlap = 50
    all_chunks = chunk_files([text_file_path], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    """ Test the sentence splitter with first chunks"""
    chunks = all_chunks[0]
    for chunk in chunks:
        assert isinstance(chunk, TextNode)
        tokens = word_tokenize(chunk.text)
        assert len(tokens) <= chunk_size 
    

test_sentence_splitter()