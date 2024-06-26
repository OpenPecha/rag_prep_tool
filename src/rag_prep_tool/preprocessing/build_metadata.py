import json
from pathlib import Path
from typing import List, Dict 

from rag_prep_tool.preprocessing.clean_text import normalize_text, remove_chapter_name_from_text, get_chapter_from_page_number

def build_metadata_for_book(page_annotated_text:str, book_name:str, chapter_page_details: List[List]):

    page_annotated_text = page_annotated_text.split("\n\n")
    
    meta_data = []
    char_count = 0
    first_page_no = chapter_page_details[0][1]
    for page_no, text in enumerate(page_annotated_text, start=first_page_no):
        text = remove_chapter_name_from_text(text, chapter_page_details)
        text = normalize_text(text)
        meta_data.append({"book_title":book_name, 
                            "page_no":page_no, 
                            "chapter": get_chapter_from_page_number(page_no, chapter_page_details),
                            "start_char":char_count,
                            "end_char":len(text)+char_count,
                            "content":text})
        char_count += len(text)


    return meta_data

   
if __name__ == "__main__":
    from rag_prep_tool.vars import ETHICS_FOR_THE_MILENNIUM_PAGE_NUMBERS 


    page_annoted_file_path = Path("output/Ethics for the New Millennium_annotated.txt")
    book_name = "Ethics for the New Millennium"
    pagination_details = {"start_page_number":9, "page_diff":0, "end_page_number":91}

    output_file_path = Path("output/Ethics for the New Millennium_metadata.json")
    meta_data = build_metadata_for_book(page_annoted_file_path, book_name, ETHICS_FOR_THE_MILENNIUM_PAGE_NUMBERS, pagination_details,output_file_path)
    content = ""
    for data in meta_data:
        content += data["content"]
    Path("Ethics for the New Millennium_content.txt").write_text(content, encoding="utf-8")
        


