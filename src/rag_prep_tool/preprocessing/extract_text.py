
import fitz  
from pathlib import Path
from typing import Dict 


def extract_text_from_pdf_file(pdf_file_path: Path) -> Dict[int, str]:
    """Reads the content of a PDF file using PyMuPDF."""
    text = {}

    try:
        pdf_document = fitz.open(pdf_file_path)
        for no in range(len(pdf_document)):
            page = pdf_document.load_page(no)
            text[no] = page.get_text() if page.get_text() else ""
        return text
    except Exception as e:
        print(f"Failed to read PDF file {pdf_file_path}: {e}")
        return {}

    

    