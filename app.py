import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
import docx

st.set_page_config(layout="wide")

@st.cache_data
def text_summary(text, maxlength=None):
    summary = Summary()
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def extract_text_from_word_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if input_text is not None:
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document here", type=['pdf', 'txt', 'doc', 'docx'])
    if input_file is not None:
        if st.button("Summarize Document"):
            with open("doc_file", "wb") as f:
                f.write(input_file.getbuffer())
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("File uploaded successfully")
                file_extension = input_file.name.split(".")[-1].lower()

                if file_extension == "pdf":
                    extracted_text = extract_text_from_pdf("doc_file")
                elif file_extension == "txt":
                    extracted_text = extract_text_from_text_file("doc_file")
                elif file_extension in ["doc", "docx"]:
                    extracted_text = extract_text_from_word_file("doc_file")

                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text)
            with col2:
                st.markdown("**Summary Result**")
                doc_summary = text_summary(extracted_text)
                st.success(doc_summary)
