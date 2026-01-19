# 📄 PDF Claim Verification System (RAG + Web Search)

This project is an **end-to-end LangChain application** that extracts factual claims from a PDF and verifies them using **live web search**.

It demonstrates:
- Retrieval-Augmented Generation (RAG)
- Real-time fact verification
- Tool usage with Tavily Search
- A simple Streamlit UI

---

## 🚀 Live Demo

🔗 **Deployed App:**  
👉 [link of the app: https://dhruvsharma2311-ai-assingment-app-4pdcsf.streamlit.app/]

--- 

## 🧠 What This Project Does

1. **Upload a PDF**
   - Drag-and-drop any PDF document containing factual information.

2. **Extract Claims**
   - Identifies factual, verifiable claims (numbers, dates, statistics, measurable facts).

3. **Retrieve Context (RAG)**
   - Uses a vector database (Chroma) to retrieve relevant document chunks.

4. **Verify Using Live Web Search**
   - Uses Tavily Search to verify each claim against real-time web data.

5. **Generate a Report**
   - Each claim is flagged as:
     - ✅ **Verified**
     - ⚠️ **Inaccurate**
     - ❌ **False**

---

## 🧠 Architecture Overview

1. **PDF Loading** – Load PDF using `PyPDFLoader`
2. **Text Splitting** – Split document using `RecursiveCharacterTextSplitter`
3. **Vector Store** – Store embeddings in Chroma DB
4. **Claim Extraction** – Use Groq LLM to extract factual claims
5. **Web Verification** – Use Tavily Search to verify each claim
6. **UI** – Display results using Streamlit

---

## 🧰 Tech Stack

- **Python**
- **LangChain**
- **RAG (Retrieval-Augmented Generation)**
- **Chroma Vector Database**
- **HuggingFace Embeddings**
- **Groq LLM (Free API)**
- **Tavily Search API**
- **Streamlit (UI)**

---

## 📂 Project Structure

ai_assignment/
├── app.py # Streamlit UI
├── rag.py # RAG + verification pipeline
├── requirements.txt
├── README.md
├── .gitignore
└── .env # API keys (not committed)

---

## 💻 Usage

1. Clone the repository:

```bash
git clone <repo_url>
cd ai_assignment
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Add yourvAPI keys in .env:
```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```
4. Run the Streamlit app:
```bash
streamlit run app.py
```