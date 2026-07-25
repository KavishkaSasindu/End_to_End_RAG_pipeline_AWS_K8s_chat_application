from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core_utils.read_all_pdf import process_all_pdf

def create_chunks(chunk_size=1000,chunk_overlap=200):
    """Here this one create chunks for the each documents which have been created by the 
    langchain pypdf loader

    Args:
        chunk_size (int, optional): define for chunk size how many charaters in one chunk. Defaults to 1000.
        chunk_overlap (int, optional): overalap with each chunk. Defaults to 200.

    Returns:
        _type_: return split_docs these are chunks list
    """
    all_documents = process_all_pdf("./data")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators=["\n\n","\n"," ",""]
    )
    
    chunks = text_splitter.split_documents(all_documents)
    print(f"Split {len(all_documents)} documents into {len(chunks)} chunks.")
    
    #show example chunk
    if chunks:
        print("\nExample Chunk: ")
        print(f"Page Contents: {chunks[0].page_content[:500]}")
        print(f"Page Contents: {chunks[0].metadata}")
        
    return chunks