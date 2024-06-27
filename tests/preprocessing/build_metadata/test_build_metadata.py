import json 
from pathlib import Path 

from rag_prep_tool.preprocessing.build_metadata import build_metadata_for_book

FREEDOM_IN_EXILE_PAGE_NUMBERS = [['HOLDER OF THE  WHITE LOTUS', 1, 18], 
                            ['THE LION THRONE', 16, 33], 
                            ['INVASION: THE STORM BREAKS', 49, 66], 
                            ['REFUGE IN THE SOUTH', 58, 75], 
                            ['IN COMMUNIST CHINA', 82, 99], 
                            ['ESCAPE INTO EXILE', 123, 140], 
                            ['A DESPERATE YEAR', 144, 161], 
                            ['A WOLF IN MONK’S ROBES', 176, 193], 
                            ['FROM EAST TO WEST', 194, 211], 
                            ['OF ‘MAGIC AND MYSTERY’', 209, 226], 
                            ['THE NEWS FROM TIBET', 221, 238], 
                            ['INITIATIVES FOR PEACE', 238, 255], 
                            ['UNIVERSAL  RESPONSIBILITY AND  THE GOOD HEART', 254, 271], 
                            ['INDEX', 273, 290]]

def test_build_metadata_for_book():
    DATA_DIR = Path(__file__).parent / "data"
    page_annotated_text = Path(DATA_DIR / "page_annoted_text.txt").read_text(encoding="utf-8")
    
    book_title = "FREEDOM IN EXILE"
    
    
    meta_data = build_metadata_for_book(page_annotated_text, book_title, FREEDOM_IN_EXILE_PAGE_NUMBERS)
    
    with open(DATA_DIR / "expected_metadata.json", "r", encoding="utf-8") as f:
        expected_metadata = json.load(f)
    assert meta_data == expected_metadata
    
