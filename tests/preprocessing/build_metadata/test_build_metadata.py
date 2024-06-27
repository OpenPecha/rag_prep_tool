import json 
from pathlib import Path 

from rag_prep_tool.preprocessing.build_metadata import build_metadata_for_book
from config import FREEDOM_IN_EXILE_PAGE_NUMBERS

def test_build_metadata_for_book():
    DATA_DIR = Path(__file__).parent / "data"
    page_annotated_text = Path(DATA_DIR / "page_annoted_text.txt").read_text(encoding="utf-8")
    
    book_title = "FREEDOM IN EXILE"
    
    
    meta_data = build_metadata_for_book(page_annotated_text, book_title, FREEDOM_IN_EXILE_PAGE_NUMBERS)
    
    with open(DATA_DIR / "expected_metadata.json", "r", encoding="utf-8") as f:
        expected_metadata = json.load(f)
    assert meta_data == expected_metadata
    
