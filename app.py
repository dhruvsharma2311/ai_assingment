import streamlit as st
from rag import run_pipeline

st.set_page_config(page_title="PDF Claim Verifier", layout="centered")

st.title("📄 PDF Claim Verification App")
st.write("Upload a PDF to extract factual claims and verify them using live web search.")

uploaded_file = st.file_uploader(
    "Drag and drop a PDF file",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Processing PDF..."):
        results = run_pipeline(uploaded_file)

    st.success("Analysis Complete")

    for i, item in enumerate(results, 1):
        st.markdown(f"### Claim {i}")
        st.write(f"**Claim:** {item['claim']}")
        st.write(f"**Status:** `{item['status']}`")
        st.write(f"**Evidence:** {item['evidence']}")
        st.divider()
