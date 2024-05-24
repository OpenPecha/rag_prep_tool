from pathlib import Path 

from rag_prep_tool.preprocessing.transfer_annotation import transfer_page_ann


def test_transfer_page_annotation():
    DATA_DIR = Path(__file__).parent / "data"
    source_text = (DATA_DIR/"extracted_from_pdf.txt").read_text()
    target_text = (DATA_DIR/"clean_text.txt").read_text()

    page_annoted_text = transfer_page_ann(source_text, target_text)
    expected_page_annoted_text = Path(DATA_DIR / "expected_page_annoted_text.txt").read_text()

    assert page_annoted_text == expected_page_annoted_text


