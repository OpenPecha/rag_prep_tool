import re 
from typing import List 

from rag_prep_tool.vars import ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS
from fast_antx.core import transfer

def remove_space(text:str)->str:
    text = text.strip().replace("\n","").replace(" ","")
    return text 

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

def number_to_words(num):
    if not (1 <= num <= 20):
        return "Number out of range"
    
    words = [
        "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen",
        "Twenty"
    ]
    return words[num - 1]

def remove_substring_from_text(text:str, substring:str)->str:
    """ removes the substring from the text """
    """ exclude the new lines and spaces"""
    """ substring should start from the beginning of the text"""
    sub_string_len = len(substring)
    count = 0
    for idx,char in enumerate(text):
        if char in ["\n", " "]:
            continue
        count += 1
        if count == sub_string_len:
            return text[idx+1:]
    return text


def remove_chapter_name_from_text(text:str, chapter_page_numbers:List[List])->str:
    """ removes chapter name from the text """
    text_stripped = text.strip().replace("\n", " ").replace(" ","")

    chapter_no = 1
    for chapter, _,_ in chapter_page_numbers:
        """ Chapter could start with 'Chapter1' or 'ChapterOne'"""
        chapter_start_variations = [f"Chapter{chapter_no}{chapter.replace(' ', '')}", f"Chapter{number_to_words(chapter_no)}{chapter.replace(' ', '')}"]
        for chapter_start in chapter_start_variations:
            if text_stripped.startswith(chapter_start):
                return remove_substring_from_text(text, chapter_start).strip()
        chapter_no += 1
    return text


def get_chapter_from_page_number(page_no:int, chapter_page_numbers:List[List])->str:
    prev_chapter = ""
    
    """ if bottom page number is not present in the book,"""
    """ we compare it with the actual page no to get the chapter name """
    bottom_page_no = chapter_page_numbers[0][1]
    has_bottom_page_no = True if bottom_page_no else False 
    for chapter, bottom_page_no, actual_page_no in chapter_page_numbers:
        if has_bottom_page_no:
            if page_no >= bottom_page_no:
                prev_chapter = chapter
                continue
        else:
            if page_no >= actual_page_no:
                prev_chapter = chapter
                continue 
        return prev_chapter
    return prev_chapter
