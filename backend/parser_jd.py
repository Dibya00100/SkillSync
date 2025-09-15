import re
from nlp_processor import NLPProcessor

# Initialize NLP processor
nlp_processor = NLPProcessor()

def extract_role(text):
    """Extract job role/title from text"""
    if not text:
        return None
    
    # Try multiple patterns for role extraction
    patterns = [
        r"(?:job\s+title|position|role)[:\-]\s*(.*?)(?:\n|$)",
        r"(?:we\s+are\s+looking\s+for|seeking)\s+(?:a\s+)?(.*?)(?:\n|$)",
        r"(.*?)\s+(?:engineer|developer|analyst|manager|specialist|consultant)",
        r"(?:senior|junior|lead|principal)\s+(.*?)(?:\n|$)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            if len(role) > 3 and len(role) < 100:  # Reasonable role length
                return role
    
    # Fallback: first line if it looks like a title
    first_line = text.split('\n')[0].strip()
    if len(first_line.split()) <= 5 and any(word in first_line.lower() for word in ['engineer', 'developer', 'analyst', 'manager']):
        return first_line
    
    return None

def extract_sections(text, keywords):
    """Extract sections based on keywords"""
    if not text:
        return []
    
    sections = []
    lines = text.split("\n")
    capture = False
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line starts a new section
        if any(k.lower() in line.lower() for k in keywords):
            if current_section:
                sections.extend(current_section)
            current_section = []
            capture = True
            continue
        
        if capture:
            # Stop if we hit another major section header
            if any(header in line.lower() for header in ['requirements', 'qualifications', 'benefits', 'about', 'company']):
                break
            current_section.append(line)
    
    if current_section:
        sections.extend(current_section)
    
    return sections

def parse_jd(jd_text):
    """Parse job description with NLP enhancement"""
    if not jd_text:
        return {
            "role": None,
            "skills": {},
            "responsibilities": [],
            "qualifications": [],
            "entities": {},
            "keywords": [],
            "experience_info": {},
            "sentiment": {},
            "sections": {}
        }
    
    # Use NLP processor for advanced analysis
    nlp_data = nlp_processor.process_job_description_advanced(jd_text)
    
    # Extract basic information
    role = extract_role(jd_text)
    responsibilities = extract_sections(jd_text, ["Responsibilities", "Duties", "What you will do"])
    qualifications = extract_sections(jd_text, ["Requirements", "Qualifications", "Preferred", "Must have"])
    
    return {
        "role": role,
        "skills": nlp_data.get('skills', {}),
        "responsibilities": responsibilities,
        "qualifications": qualifications,
        "entities": nlp_data.get('entities', {}),
        "keywords": [kw[0] for kw in nlp_data.get('keywords', [])],
        "experience_info": nlp_data.get('experience_info', {}),
        "sentiment": nlp_data.get('sentiment', {}),
        "sections": nlp_data.get('sections', {}),
        "text_length": nlp_data.get('text_length', 0),
        "word_count": nlp_data.get('word_count', 0)
    }