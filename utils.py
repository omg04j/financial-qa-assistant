# utils.py

import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama


def build_retriever(save_path: str = "vectorstore.pkl"):
    """Load retriever from saved FAISS vectorstore."""
    with open(save_path, "rb") as f:
        vectorstore = pickle.load(f)
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})


def build_chain():
    retriever = build_retriever()

    # Local LLM via Ollama (make sure Ollama is running and model is installed)
    llm = ChatOllama(
        model="mistral",
        temperature=0.2,
        max_tokens=512,
    )

    prompt = PromptTemplate(
        template="""
        You are a helpful **Financial Analyst Assistant**.
        Your job is to answer user questions about the uploaded financial document.

        Guidelines:
        - Use only the information from the document (context below).
        - Give concise, clear answers (2–5 sentences).
        - If numbers are asked, extract and present them directly.
        - If unsure, politely say the data is not in the document.

        Context:
        {context}

        Question: {question}
        """,
        input_variables=["context", "question"],
    )

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    parser = StrOutputParser()
    qa_chain = parallel_chain | prompt | llm | parser

    return qa_chain
