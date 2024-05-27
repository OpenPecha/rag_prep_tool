import json 
from pathlib import Path 

from rag_prep_tool.preprocessing.build_metadata import build_metadata_for_book
from rag_prep_tool.vars import ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS

def test_build_metadata_for_book():
    DATA_DIR = Path(__file__).parent / "data"
    page_annotated_file = DATA_DIR / "page_annoted_text.txt"
    
    book_title = "The Art of Happiness at Work"
    pagination_details = {
        "start_page_number":11,
        "page_diff":13,
        "end_page_number":205
    }
    output_file_path = DATA_DIR / "output_metadata.json"
    build_metadata_for_book(page_annotated_file, book_title, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS, pagination_details, output_file_path)

    assert output_file_path.exists()
    output_data = json.loads(output_file_path.read_text())
    expected_output_data = json.loads((DATA_DIR / "expected_output_metadata.json").read_text())
    assert output_data == expected_output_data
    
    """ clean up"""
    output_file_path.unlink()

test_build_metadata_for_book()