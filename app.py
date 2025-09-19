# app.py

import streamlit as st
import os
import tempfile

from build_vectorstore import build_vectorstore
from utils import build_chain


st.set_page_config(page_title="Financial Q&A Assistant", page_icon="💹")

st.title("📊 Financial Document Q&A Assistant")
st.write("Upload a **PDF or Excel file** and ask questions about your financial data.")


# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload Financial Document", type=["pdf", "xlsx", "xls"])

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    st.success(f"✅ File uploaded: {uploaded_file.name}")

    if st.button("📌 Process Document"):
        with st.spinner("Processing document..."):
            build_vectorstore(file_path)
        st.success("✅ Document processed and ready for Q&A!")


# ---------------------------
# Chat Section
# ---------------------------
st.subheader("💬 Ask Questions")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    if os.path.exists("vectorstore.pkl"):
        qa_chain = build_chain()
        with st.spinner("Thinking..."):
            answer = qa_chain.invoke(prompt)
    else:
        answer = "⚠️ Please upload and process a document first."

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").markdown(answer)
