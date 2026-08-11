import streamlit as st
import os
import sys

# Append current directory to system path for smooth imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query import query_rag
from ingest import ingest_document

st.set_page_config(page_title="Cost-Efficient RAG System", layout="wide")
st.title("🤖 Cost-Efficient RAG Application")

# Sidebar for document ingestion
with st.sidebar:
    st.header("📄 Document Ingestion")
    uploaded_file = st.file_uploader("Upload a document (.pdf or .txt)", type=["pdf", "txt"])
    category = st.text_input("Category Tag", value="general")
    
    if st.button("Ingest Document") and uploaded_file:
        save_path = os.path.join(".", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Ingesting and embedding..."):
            ingest_document(save_path, category=category)
        st.success("Document Ingested Successfully!")

# Main chat interface
st.header("💬 Ask Questions")
question = st.text_input("Enter your query about the knowledge base:")

if st.button("Get Answer") and question:
    with st.spinner("Searching and generating response..."):
        res = query_rag(question)
        
    st.subheader("Answer:")
    st.write(res["answer"])
    
    st.subheader("Sources:")
    st.write(res.get("sources", []))
    
    st.caption(f"Latency: {res.get('latency_sec', 0)} seconds")