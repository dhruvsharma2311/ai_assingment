# 📄 PDF Claim Verification System (RAG + Web Search)

This project is an **end-to-end LangChain application** that extracts factual claims from a PDF and verifies them using **live web search**.

It demonstrates:
- Retrieval-Augmented Generation (RAG)
- Real-time fact verification
- Tool usage with Tavily Search
- A simple Streamlit UI

---

## 🚀 Features

- Upload any PDF document
- Automatically extract **verifiable claims** (numbers, dates, statistics, facts)
- Verify each claim using live web search
- Classify claims as:
  - ✅ **Verified**
  - ⚠️ **Inaccurate**
  - ❌ **False**
- Clean and simple Streamlit interface

---

## 🧠 Architecture Overview

1. **PDF Loading** – Load PDF using `PyPDFLoader`
2. **Text Splitting** – Split document using `RecursiveCharacterTextSplitter`
3. **Vector Store** – Store embeddings in Chroma DB
4. **Claim Extraction** – Use Groq LLM to extract factual claims
5. **Web Verification** – Use Tavily Search to verify each claim
6. **UI** – Display results using Streamlit

---

## 📁 Project Structure
-app.py # Streamlit UI
-rag.py # RAG + claim verification logic
-chroma_db/ # Vector database (auto-created)
-.env # API keys
-README.md

## How to run 
- streamlit run app.py