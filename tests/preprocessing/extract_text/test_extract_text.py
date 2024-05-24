import json 
from pathlib import Path 

from rag_prep_tool.preprocessing.extract_text import extract_text_from_pdf_file


def test_extract_text_from_pdf_file():
    DATA_DIR = Path(__file__).parent / "data"
    pdf_file_path = DATA_DIR / "The Art of Happiness at Work first page.pdf"

    extracted_data = extract_text_from_pdf_file(pdf_file_path)
    with open(DATA_DIR / "expected_extracted_file.json", "r") as f:
        expected_extracted_data = json.load(f)

    """ Convert expected_extracted_data keys to integer for comparison """
    expected_extracted_data = {int(key): value for key, value in expected_extracted_data.items()}

    assert extracted_data == expected_extracted_data

