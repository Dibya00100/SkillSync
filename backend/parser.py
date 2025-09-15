import os
import re
import docx
import pdfplumber
from nlp_processor import NLPProcessor

# Initialize NLP processor
nlp_processor = NLPProcessor()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF files"""
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX files"""
    text = ''
    try:
        doc = docx.Document(docx_path)
        text = '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
    return text

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra spaces, tabs, etc.
    return re.sub(r'\s+', ' ', text).strip()

def structure_data(text):
    """Extract structured data from resume text using NLP"""
    if not text:
        return {
            "name": None,
            "email": None,
            "phone": None,
            "address": None,
            "skills": [],
            "experience": [],
            "projects": [],
            "entities": {},
            "keywords": [],
            "experience_info": {},
            "sentiment": {}
        }

    # Use NLP processor for advanced extraction
    nlp_data = nlp_processor.process_resume_advanced(text)
    
    # Basic regex extraction for contact info
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
    phone_match = re.search(r"\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b", text)
    
    # Extract name (first line that looks like a name)
    lines = text.split('\n')
    name = None
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if len(line.split()) >= 2 and len(line.split()) <= 4:
            # Check if it doesn't contain common resume keywords
            if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae', 'email', 'phone']):
                name = line
                break

    # Structure the data
    data = {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "address": None,  # Could be enhanced with NLP
        "skills": nlp_data.get('skills', {}),
        "experience": [],  # Could be enhanced with NLP
        "projects": [],    # Could be enhanced with NLP
        "entities": nlp_data.get('entities', {}),
        "keywords": [kw[0] for kw in nlp_data.get('keywords', [])],
        "experience_info": nlp_data.get('experience_info', {}),
        "sentiment": nlp_data.get('sentiment', {}),
        "text_length": nlp_data.get('text_length', 0),
        "word_count": nlp_data.get('word_count', 0)
    }

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

