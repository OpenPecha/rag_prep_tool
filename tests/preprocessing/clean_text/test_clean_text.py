from rag_prep_tool.vars import ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS

from rag_prep_tool.preprocessing.clean_text import ( 
    get_chapter_from_page_number,
    remove_chapter_name_from_text,
    normalize_text,
    replace_double_quotes
)


def test_get_chapter_from_page_number():
    
    chapter = get_chapter_from_page_number(24,ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert chapter == "TRANSFORMING DISSATISFACTION AT WORK"

    chapter = get_chapter_from_page_number(111,ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert chapter == "JOB, CAREER, AND CALLING"

    chapter = get_chapter_from_page_number(190,ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert chapter == "HAPPINESS AT WORK"


def test_remove_chapter_name_from_text():
    text = "Chapter1TRANSFORMING DISSATISFACTION AT WORK Hello"
    output  = remove_chapter_name_from_text(text, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert output == "Hello"

    text = "Chapter One TRANSFORMING DISSATISFACTION AT WORK Hello"
    output  = remove_chapter_name_from_text(text, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert output == "Hello"

    text = "Chapter5 \nJOB, CAREER,  AND\n CALLING It has been a very long day since"
    output  = remove_chapter_name_from_text(text, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert output == "It has been a very long day since"

    text = "ChapterFive \nJOB, CAREER,  AND\n CALLING It has been a very long day since"
    output  = remove_chapter_name_from_text(text, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert output == "It has been a very long day since"

    text = "Chapter 9 \nHAPPINESS AT WORK Once upon a time"
    output  = remove_chapter_name_from_text(text, ART_OF_HAPPINESS_CHAPTERS_PAGE_NUMBERS)
    assert output == "Once upon a time"

def test_normalize_text():
    text = "Hello\n.Today was a very nice day"
    output = normalize_text(text) 
    assert output == "Hello.Today was a very nice day"

    text = "Hello\n.Today was a  \n very   nice   day"
    output = normalize_text(text) 
    assert output == "Hello.Today was a very nice day"


def test_replace_double_quotes():
    text = "Hello \"World\""
    output = replace_double_quotes(text)
    assert output == "Hello <World>"

    text = "Hello \"World\" \"How are you doing\""
    output = replace_double_quotes(text)
    assert output == "Hello <World> <How are you doing>"
