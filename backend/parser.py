import os
import re
import docx
import pdfplumber


# TODO Create a function for extracting text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text


# TODO Create a function for extracting text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


# TODO Create a function for simplifying the text and removing extra spaces
def clean_text(text):
    # Remove extra spaces, tabs, etc.
    return re.sub(r'\s+', ' ', text).strip()


# TODO Create a function for extracting data from the parsed text
def structure_data(text):
    data = {
        "name": None,
        "email": None,
        "phone": None,
        "address": None,
        "skills": [],
        "experience": [],
        "projects": [],
    }

    # email
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
    if email_match:
        data["email"] = email_match.group(0)

    # Phone
    phone_matching = re.search(r"\b\d{10}\b", text)
    if phone_matching:
        data["phone"] = phone_matching.group(0)

    # Skills (basic keyword match for now)
    skills_list = ["Python", "C++", "Java", "SQL", "Machine Learning", "Data Science", "React", "Node.js"]
    data["skills"] = [skill for skill in skills_list if skill.lower() in text.lower()]

    return data

def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
         return {"error": "Unsupported file type"}


    text = clean_text(text)
    data = structure_data(text)

    # Delete temp file
    if file_path.startswith("temp_") and os.path.exists(file_path):
        os.remove(file_path)

    return data

