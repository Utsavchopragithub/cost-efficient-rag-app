import hashlib
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import get_vectorstore

def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def ingest_document(file_path, category="default", chunk_size=512, chunk_overlap=64):
    # Select appropriate loader based on extension
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
        
    documents = loader.load()
    
    # Attach custom metadata filter tag
    doc_hash = get_file_hash(file_path)
    for doc in documents:
        doc.metadata["file_hash"] = doc_hash
        doc.metadata["category"] = category

    # Chunk the documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    
    # Store vectors
    db = get_vectorstore(chunks=chunks)
    print(f"Ingested {len(chunks)} chunks from {file_path}")
    return db

if __name__ == "__main__":
    # Example usage
    ingest_document("sample.pdf", category="docs")