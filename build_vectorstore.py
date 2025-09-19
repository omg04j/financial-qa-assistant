# build_vectorstore.py

import pickle
import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_documents(file_path: str):
    """Load financial documents (PDF or Excel)."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        loader = UnstructuredExcelLoader(file_path)
    else:
        raise ValueError("❌ Unsupported file format. Please upload PDF or Excel.")
    return loader.load()


def build_vectorstore(file_path: str, save_path: str = "vectorstore.pkl"):
    """Build FAISS vectorstore from uploaded financial document."""
    
    # Always rebuild when a new file is uploaded
    if os.path.exists(save_path):
        os.remove(save_path)

    print("📂 Loading document...")
    docs = load_documents(file_path)

    print("✂️ Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("🔎 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    print("💾 Saving vector store locally...")
    with open(save_path, "wb") as f:
        pickle.dump(vector_store, f)

    print(f"✅ Vector store built and saved at {save_path}!")
    return vector_store


if __name__ == "__main__":
    # Example usage
    sample_file = "sample_financials.pdf"  # Replace with your file
    build_vectorstore(sample_file)
