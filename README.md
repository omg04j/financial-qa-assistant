# 📊 Financial Document Q\&A Assistant

An interactive **rag based web application** that processes **financial documents (PDF & Excel)** and enables users to ask **natural language questions** about revenues, expenses, profits, and other financial metrics.

Built using **Streamlit, LangChain, FAISS, Hugging Face Embeddings, and Ollama** for local LLM inference.

---

## 🚀 Features

* 📂 Upload **PDF or Excel** financial documents
* 🔍 Extract text & numerical data from financial statements
* 📑 Supports Income Statements, Balance Sheets, and Cash Flow Statements
* 💬 Ask **natural language questions** about financial data
* 🤖 Powered by **local Small Language Models (SLMs)** via **Ollama**
* 🖥️ Runs **locally** (no cloud deployment required)

---

## 📋 Requirements

* Python
* [Ollama](https://ollama.ai/) installed locally with **Mistral** model (or another compatible model)
* Dependencies listed in `requirements.txt`

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/financial-qa-assistant.git
cd financial-qa-assistant
```

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3️⃣ Install & Run Ollama

* Download Ollama: [https://ollama.ai/download](https://ollama.ai/download)
* Pull the **Mistral** model (or another model you prefer, I used Mistral in my case):

```bash
ollama pull mistral
```

> If you use a different local model name, update `utils.py` where `ChatOllama(model=...)` is set.

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

The app will normally be served at `http://localhost:8501`.

---

## 📂 Project Structure

```
financial-qa-assistant/
│── app.py                # Streamlit UI for file upload & chat
│── build_vectorstore.py  # Builds FAISS vectorstore from uploaded docs
│── utils.py              # QA chain, retriever, and LLM integration
│── requirements.txt      # Python dependencies
│── README.md             # This file
```

---

## 💻 Usage

1. Open the app in your browser (`http://localhost:8501`)
2. Upload a **PDF or Excel financial document**
3. Click **Process Document**
4. Ask questions in the chat box

