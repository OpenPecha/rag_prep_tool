from fast_antx.core import transfer


def transfer_page_ann(source_text:str, target_text:str)->str:
    """ replacing page breaks (\n\n) with ⏎ in source_text and removing page breaks in target_text"""
    source_text = source_text.replace("\n\n", "⏎")
    target_text = target_text.replace("\n\n", "")

    annotations = [["page_breaks", "(⏎)"]]
    page_annoted_text = transfer(source_text, annotations, target_text, output="txt")
    page_annoted_text = page_annoted_text.replace("⏎", "\n\n")
    return page_annoted_text




