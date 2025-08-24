import re

SKILLS = [
    "Python", "C++", "Java", "SQL", "Machine Learning", "Data Science",
    "React", "Node.js", "AWS", "GCP", "Azure", "Docker", "Kubernetes"
]

def extract_skill(text):
    found_skills = []
    for skill in SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

def extract_role(text):
    role_match = re.search(r"(Role|Title)[:\-]\s*(.*)", text, re.IGNORECASE)
    if role_match:
        return role_match.group(2).strip()
    else:
        return text.split(0).strip()

def extract_sections(text,keywords):
    sections = []
    lines = text.split("\n")
    capture = False
    for line in lines:
        if any(k.lower() in line.lower() for k in keywords):
            capture = True
        if capture:
            if line.strip() == "":
                break
            # stop only if it's another header line (not bullet points with :)
            if any(h.lower() in line.lower() for h in keywords):
                continue
            if ":" in line and not line.strip().startswith("-"):
                break
            sections.append(line)
    return sections

def parse_jd(jd_text):
    return{
        "role": extract_role(jd_text),
        "skills": extract_skill(jd_text),
        "responsibilities": extract_sections(jd_text, ["Responsibilities", "Duties"]),
        "qualifications": extract_sections(jd_text, ["Requirements", "Qualifications", "Preferred"])
    }