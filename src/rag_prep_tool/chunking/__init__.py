from pathlib import Path 
from typing import List 

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode

def chunk_files(file_paths: List[Path], chunk_size: int = 500, chunk_overlap: int = 50)->List[TextNode]:
    
    """ convert the files into structured nodes for the RAG model"""
    file_paths = [str(file_path) for file_path in file_paths]
    documents = SimpleDirectoryReader(input_files= file_paths).load_data()
    base_splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = base_splitter.get_nodes_from_documents(documents)

    return chunks 

if __name__ == "__main__":
    file_paths = [Path("output/Ethics for the New Millennium_content.txt")]
    chunks = chunk_files(file_paths)
    print(chunks[0].text)
