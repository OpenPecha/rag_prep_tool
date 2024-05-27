import json 

from pathlib import Path 

from rag_prep_tool.preprocessing.extract_text import extract_text_from_pdf_file
from rag_prep_tool.preprocessing.transfer_annotation import transfer_page_ann
from rag_prep_tool.preprocessing.build_metadata import build_metadata_for_book

def preprocess(pdf_file_path:Path, clean_text_path:Path, book_name:str, chapter_page_numbers:List[List], pagination_details:Dict[str,int]):
    """ extract text from pdf file and save it in json and txt format"""
    extracted_data = extract_text_from_pdf_file(pdf_file_path)

    file_name = pdf_file_path.stem
    with open(f"{file_name}.json", "w") as f:
        json.dump(extracted_data, f, indent=4)

    extracted_text_path = Path(f"{file_name}.txt")
    with open(extracted_text_path, "w") as f:
        for page_no, page_text in extracted_data.items():
            if page_no <=7 or page_no >= 91:
                continue
            f.write(f"{page_text}\n\n")
    
    """ transfer page annotations from extracted text to clean text and save it in txt format"""
    source_text = extracted_text_path.read_text(encoding="utf-8")
    target_text = clean_text_path.read_text(encoding="utf-8")
    page_annoted_text = transfer_page_ann(source_text, target_text)

    page_annotated_file = Path(f"{file_name}_annotated.txt")
    page_annotated_file.write_text(page_annoted_text, encoding="utf-8")

    """ build metadata for the book and save it in json format"""
    output_metadata_path = Path(f"{file_name}_metadata.json")
    book_meta_data = build_metadata_for_book(page_annotated_file, book_name,chapter_page_numbers, pagination_details, output_metadata_path)
    return book_meta_data

