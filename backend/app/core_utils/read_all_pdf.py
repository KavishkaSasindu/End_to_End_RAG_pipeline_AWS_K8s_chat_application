import os 
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def process_all_pdf(path_directory: str):
    """Automatically process all pdf files to Document data structure
    in langchain

    Args:
        path_directory (str): require path for the actual fils have
    """
    
    all_documents = []
    pdf_dir = Path(path_directory)
    
    # find all pdf files
    pdf_files = list(pdf_dir.glob("**/*.pdf"))
    print(pdf_files)
    
    print(f"Found {len(pdf_files)} of pdf files to process")
    
    for pdf_file in pdf_files:
        print(f"\nProcessing {pdf_file.name}")
        try:
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            
            # add source information to documents that create through the pypdfloader
            for document in documents:
                document.metadata["source_file"] = pdf_file.name
                document.metadata["file_type"] = "pdf"
                
            all_documents.extend(documents)
            print(f"Load {len(documents)} documents")
        except Exception as e:
            print(f"There is an issue with the process {pdf_file.name}")   
            raise
        
    return all_documents