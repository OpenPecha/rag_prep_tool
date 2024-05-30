import json 
from pathlib import Path 
from typing import List, Dict 

from llama_index.core.schema import TextNode

def is_overlapping(x1,x2,y1,y2):
  x = range(x1, y1)
  y = range(x2, y2)
  xs = set(x)

  if len(xs.intersection(y)) == 0:
    return False
  return True

def get_metadata_for_each_chunk(chunks: List[TextNode], metadata: Path)->Dict:
    mapping = {}
    for block in metadata:
        for chunk in chunks:
            if is_overlapping(block["start_char"], chunk.start_char_idx, block["end_char"], chunk.end_char_idx):
                if not chunk.id_ in mapping:
                    mapping[chunk.id_] = {"book_title": [], "page_no": [], "chapter": []}

                if not block["book_title"] in mapping[chunk.id_]["book_title"]:
                    mapping[chunk.id_]["book_title"].append(block["book_title"])

                if not block["chapter"] in mapping[chunk.id_]["chapter"]:
                    mapping[chunk.id_]["chapter"].append(block["chapter"])

                mapping[chunk.id_]["page_no"].append(block["page_no"])

    return mapping

def map_chunks_with_metadata(chunks: List[TextNode], metadata_file_path: Path)->List[TextNode]:
    """Map the metadata to the chunks"""

    with open(metadata_file_path) as f:
        metadata = json.load(f)
    
    mapping = get_metadata_for_each_chunk(chunks, metadata)
    for chunk in chunks:
        current_metadata = mapping[chunk.id_]

        for key_ in current_metadata:
            metadata_str = current_metadata[key_]
            if type(metadata_str) == list:
                metadata_str = ','.join(map(str, metadata_str))
            chunk.metadata[key_] = metadata_str

    return chunks 

