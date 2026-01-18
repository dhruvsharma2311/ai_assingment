import os
import tempfile
import json
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
import streamlit as st

# -------------------------
# ENV SETUP
# -------------------------
load_dotenv()

# Try to get keys from Streamlit secrets first
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY"))

if not GROQ_API_KEY or not TAVILY_API_KEY:
    st.error("GROQ_API_KEY or TAVILY_API_KEY is missing! Please set them in Streamlit Secrets or .env")
    st.stop()  # Stop execution so the app doesn't crash

# -------------------------
# LLM
# -------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# -------------------------
# 1) Load PDF
# -------------------------
def load_dataset(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()
    return docs

# -------------------------
# 2) Split Documents
# -------------------------
def splitting_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150
    )
    return splitter.split_documents(docs)

# -------------------------
# 3) Create Vector DB
# -------------------------
def create_vectordb(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    return vectordb

def get_retriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": 3})

# -------------------------
# 4) Claim Extraction
# -------------------------
CLAIM_PROMPT = PromptTemplate(
    template="""
Context:
{context}

Extract ONLY factual, verifiable claims.
Claims must include numbers, dates, statistics, or measurable facts.

Return STRICT JSON list of strings.
""",
    input_variables=["context"]
)

def extract_claims(retriever):
    docs = retriever.invoke("Extract key factual claims")
    context = "\n".join(doc.page_content for doc in docs)

    response = llm.invoke(CLAIM_PROMPT.format(context=context)).content

    try:
        return json.loads(response)
    except:
        return []

# -------------------------
# 5) Verify Claims with Tavily
# -------------------------
tavily = TavilySearchResults(max_results=3)

def verify_claims(claims):
    results = []

    for claim in claims:
        search = tavily.invoke({"query": claim})

        verify_prompt = f"""
    Claim:
    {claim}

    Web Evidence:
    {search}

    Classify the claim as:
    - Verified
    - Inaccurate
    - False

    Return STRICT JSON:
    {{
    "status": "...",
    "evidence": "short explanation"
    }}
    """

        response = llm.invoke(verify_prompt).content

        try:
            parsed = json.loads(response)
        except:
            parsed = {
                "status": "False",
                "evidence": "No reliable evidence found."
            }

        results.append({
            "claim": claim,
            "status": parsed["status"],
            "evidence": parsed["evidence"]
        })

    return results

# -------------------------
# 6) End-to-End Pipeline
# -------------------------
def run_pipeline(pdf_file):
    docs = load_dataset(pdf_file)
    chunks = splitting_docs(docs)
    vectordb = create_vectordb(chunks)
    retriever = get_retriever(vectordb)

    claims = extract_claims(retriever)
    if not claims:
        return []

    return verify_claims(claims)
