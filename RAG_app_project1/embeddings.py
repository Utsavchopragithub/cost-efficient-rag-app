from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def get_vectorstore(chunks=None, persist_directory="db"):
    # Download and load free local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if chunks:
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
    else:
        db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
    return db