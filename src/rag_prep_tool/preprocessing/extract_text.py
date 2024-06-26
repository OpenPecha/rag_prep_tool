import re 
import fitz  
from pathlib import Path
from typing import Dict , Tuple
from fast_antx.core import transfer

from rag_prep_tool.preprocessing.clean_text import number_to_words
from rag_prep_tool.config import BOOK_SECTION_TITLES

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

def filter_extracted_text(extracted_text:str, transcribed_text:str)->str:
    transcribed_text = "⏎"+ transcribed_text+ "⏎"
    annotations = [["page_breaks", "(⏎)"]]

    annotated_text = transfer(transcribed_text, annotations, extracted_text, output="txt")
    filtered_text = "".join(annotated_text.split("⏎")[1])
    return filtered_text
    

def get_chapter_name(page_content:str)->str:
    """ Get chapter name from page content"""
    """ ' \nChapter One\nCHAPTER NAME\nPAGE CONTENT ... '"""
    cleaned_content = re.sub(r'\s*\n\s*', '\n', page_content.strip())
    chapter_name = cleaned_content.splitlines()[1]
    return chapter_name

def get_page_number(page_content:str)->int:
    cleaned_content = re.sub(r'\s*\n\s*', '\n', page_content.strip())

    """ Get page number of page number"""
    """ Important Note: page number written on bottom of page, not the actual page number"""

    try: 
        page_no = cleaned_content.split("\n")[-1]
        page_no = page_no.replace(" ","")
        page_no = int(page_no)
    except:
        page_no = None 
    return page_no

def get_chapter_page_ranges(extracted_text:Dict[int, str]):
    chapter_page_details = []

    for page_no, content in extracted_text.items():
        stripped_content = content.strip().replace("\n","").replace(" ","")
        
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
                    chapter_name = get_chapter_name(content)
                    bottom_page_no = get_page_number(content)
                    chapter_page_details.append([chapter_name, bottom_page_no, page_no])
                    break 
        """ Start of Index, Epilogue, ..."""
        for book_section_title in BOOK_SECTION_TITLES:
            if stripped_content.startswith(book_section_title):
                """ check if the book section is already covered"""
                if book_section_title == chapter_page_details[-1][0]:
                    break 
                bottom_page_no = get_page_number(content)
                chapter_page_details.append([book_section_title,bottom_page_no, page_no])
                break 
    return chapter_page_details



if __name__ == "__main__":
    pdf_path = Path("output/freedom_in_exile.pdf")
    extracted_content = extract_text_from_pdf_file(pdf_path)
    extracted_text = [content for _, content in extracted_content.items()]
    extracted_text = ''.join(extracted_text)

    transcribed_text = Path("output/freedom_in_exile.txt").read_text(encoding="utf-8")
    filter_text = filter_extracted_text(extracted_text, transcribed_text)
    print(filter_text)
