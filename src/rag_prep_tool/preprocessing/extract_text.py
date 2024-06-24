import re 
import fitz  
from pathlib import Path
from typing import Dict 

from rag_prep_tool.preprocessing.clean_text import number_to_words

def extract_text_from_pdf_file(pdf_file_path: Path) -> Dict[int, str]:
    """Reads the content of a PDF file using PyMuPDF."""
    text = {}

    try:
        pdf_document = fitz.open(pdf_file_path)
        for no in range(len(pdf_document)):
            page = pdf_document.load_page(no)
            text[no+1] = page.get_text() if page.get_text() else ""
        return text
    except Exception as e:
        print(f"Failed to read PDF file {pdf_file_path}: {e}")
        return {}


def get_chapter_page_ranges(extracted_text:Dict[int, str]):
    chapter_page_details = []

    for page_no, content in extracted_text.items():
        stripped_content = content.strip().replace("\n","").replace(" ","")
        
        """ """

        """ Possible starts such as Chapter 1, Chapter One"""
        possible_starts = ["Chapter", "CHAPTER", "chapter"]
        if any(stripped_content.startswith(chapter_start) for chapter_start in possible_starts):
            flag = False 
            for number in range(20,0,-1):
                if stripped_content[len("chapter"):].startswith(str(number)):
                    flag = True 
                number_in_word = number_to_words(number)
                if stripped_content[len("chapter"):].startswith(number_in_word):
                    flag = True 
            
                if flag:
                    """ Get chapter name from content"""
                    """ ' \nChapter One\nCHAPTER NAME\nPAGE CONTENT ... '"""
                    cleaned_content = re.sub(r'\s*\n\s*', '\n', content.strip())
                    chapter_name = cleaned_content.splitlines()[1]
                    chapter_page_details.append([f"{chapter_name}", page_no])
                    break 
    
    return chapter_page_details




if __name__ == "__main__":
    pdf_path = Path("output/EN19 Ethics for the New Millennium - Dalai Lama.pdf")
    extracted_text = extract_text_from_pdf_file(pdf_path)
    chapter_details = get_chapter_page_ranges(extracted_text)
    print(chapter_details)

    