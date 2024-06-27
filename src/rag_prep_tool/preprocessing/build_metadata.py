import json
from pathlib import Path
from typing import List

from rag_prep_tool.preprocessing.clean_text import normalize_text, remove_chapter_name_from_text, get_chapter_from_page_number
from rag_prep_tool.config import BOOK_SECTION_TITLES

def build_metadata_for_book(page_annotated_text:str, book_name:str, chapter_page_details: List[List]):

    page_annotated_text = page_annotated_text.split("\n\n")
    
    meta_data = []
    char_count = 0
    
    """ if a page contains a bottom page no(normally not same as actual page no), we take that"""
    """ else take actual page no (paper wise from first page of book)"""
    bottom_page_no, page_no = chapter_page_details[0][1], chapter_page_details[0][2]
    first_page_no = bottom_page_no if bottom_page_no else page_no
    for page_no, text in enumerate(page_annotated_text, start=first_page_no):
        text = remove_chapter_name_from_text(text, chapter_page_details)
        text = normalize_text(text)
        chapter_name = get_chapter_from_page_number(page_no, chapter_page_details)
        """ if the section is index, epilogue, dont need to include in metadata """
        if chapter_name in BOOK_SECTION_TITLES:
            break 
        meta_data.append({"book_title":book_name, 
                            "page_no":page_no, 
                            "chapter": chapter_name,
                            "start_char":char_count,
                            "end_char":len(text)+char_count,
                            "content":text})
        char_count += len(text)


    return meta_data

   


