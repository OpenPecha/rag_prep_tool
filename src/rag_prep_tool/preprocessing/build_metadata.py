import json
from pathlib import Path
from typing import List, Dict 

from rag_prep_tool.preprocessing.clean_text import normalize_text, get_chapter_from_page_number
from rag_prep_tool.vars import ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS

def build_metadata_for_book(page_annotated_file:Path, chapter_page_numbers: List[List], pagination_details:Dict[str,int], output_file_path:Path ):

    start_page_number = pagination_details["start_page_number"]
    page_diff = pagination_details["page_diff"]
    end_page_number = pagination_details["end_page_number"]

    """ 
    Args:
    page_annotated_file: Path to the page annotated file txt file
    chapters_page_numbers: List of Lists containing the chapter name and the page number where the chapter starts
    start_page_number: The page number from where the chapter 1 starts
    page_diff: The difference between the page number in the chapter 1 and the actual page number 
                of the book (in some cases page number below the page is not equal to the actual page number of the book)
    end_page_number: The page number where the last chapter ends
    
    output_file_path: Path to the output json file where the metadata will be saved
    """
    page_annoted_text = page_annotated_file.read_text()
    page_annoted_text = page_annoted_text.split("\n\n")
    """ Extracting the content of book starting from chapter 1"""
    meta_data = []
    char_count = 0

    for i, text in enumerate(page_annoted_text):
        """ removes eplilogue and appendix"""
        if i+start_page_number > end_page_number:
            break
        text = normalize_text(text, chapter_page_numbers)
        meta_data.append({"book_title":"The Art of Happiness at Work", 
                            "page_no":i+start_page_number, 
                            "chapter": get_chapter_from_page_number(i+start_page_number+page_diff),
                            "start_char":char_count,
                            "end_char":len(text)+char_count,
                            "content":text})
        char_count += len(text)

    """ Save the meta_data to a json file """
    output_file_path = Path("art_of_happiness.json")
    with open(output_file_path, "w") as f:
        f.write(json.dumps(meta_data, indent=4))

   