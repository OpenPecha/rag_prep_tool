import re 
from typing import List 

from rag_prep_tool.vars import ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS
from antx.core import transfer


def normalize_text(text:str)->str:
    """ replaces double quotes with < and >"""
    text = replace_double_quotes(text)
    text = text.replace("\n","")
    """ Replace multiple spaces with a single space """
    text = re.sub(r"[ ]+", " ", text)
    return text.strip()


def replace_double_quotes(text:str)->str:
    """ replaces double quotes with < and >"""
    result = []
    quote_count = 0
    for char in text:
        if char == '"':
            quote_count += 1
            if quote_count % 2 == 1:
                result.append('<')
            else:
                result.append('>')
        else:
            result.append(char)
    return ''.join(result)

def remove_chapter_name_from_text(text:str, chapter_page_numbers:List[List])->str:
    """ removes chapter name from the text """
    text_stripped = text.strip().replace("\n", "").replace(" ","")

    chapter_no = 1
    for chapter, _ in chapter_page_numbers:
        chapter_start = f"Chapter{chapter_no}{chapter.replace(' ', '')}"
        if text_stripped.startswith(chapter_start):
            text_stripped = text_stripped.replace(chapter_start, "")
            annotations = [["new_line", "(\n)"], ["space", "(\s)"]]
            output_text = transfer(text, annotations, text_stripped, output="txt")
            return output_text.strip()
        chapter_no += 1
    return text


def get_chapter_from_page_number(page_no:int, chapter_page_numbers:List[List])->str:
    prev_chapter = ""
    for chapter, chapter_page_start in chapter_page_numbers:
        if page_no >= chapter_page_start:
            prev_chapter = chapter
            continue
        return prev_chapter
    return prev_chapter
