from pypdf import PdfReader
from pathlib import Path
from typing import Dict 

def extract_text_from_pdf_file(pdf_file_path: Path) -> Dict[int, str]:
    """Reads the content of a PDF file using pypdf."""
    text = {}

    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for no, page in enumerate(pdf_reader.pages):
                text[no] = page.extract_text() if page.extract_text() else ""
        return text
    except Exception as e:
        print(f"pdf file {pdf_file_path} is corrupted")
        return {}
    

    