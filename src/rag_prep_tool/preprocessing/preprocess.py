import json 

from pathlib import Path 
from typing import List, Dict 
from rag_prep_tool.preprocessing.extract_text import (extract_text_from_pdf_file, filter_extracted_text, get_chapter_page_ranges) 
from rag_prep_tool.preprocessing.transfer_annotation import transfer_page_ann
from rag_prep_tool.preprocessing.build_metadata import build_metadata_for_book

def preprocess(pdf_file_path:Path, transcribed_text_path:Path, book_name:str):
    """ extract text from pdf file"""
    extracted_data = extract_text_from_pdf_file(pdf_file_path)
    """ get chapter details """
    chapter_details = get_chapter_page_ranges(extracted_data)


    """ transfer page annotation from extracted text to page annotated text"""
    transcribed_text = transcribed_text_path.read_text(encoding="utf-8")    
    first_page = chapter_details[0][2]
    last_page = chapter_details[-1][2]
    filtered_text = "\n\n".join([content for page_no, content in extracted_data.items() if first_page <= page_no <= last_page])
    page_annoted_text = transfer_page_ann(filtered_text, transcribed_text)


if __name__ == "__main__":
    pdf_path = Path("output/art_of_happiness_at_work.pdf")
    transcribed_path = Path("output/art_of_happiness_at_work.txt")
    preprocess(pdf_path, transcribed_path, "freedom in exile")
