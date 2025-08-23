"""
Matching engine for SkillSync (skills-based, Day 3)
- Case-insensitive matching
- Preserves JD casing in outputs
- Returns a backward-compatible alias 'match_skill' for 'matched_skills'
"""

def calculate_match(resume_data: dict, jd_data: dict) -> dict:

    resume_list = resume_data.get("skills", []) or []
    jd_list = jd_data.get("skills_required", []) or []

    # Build lowercase maps to original casing
    resume_map = {str(s).strip().lower(): str(s).strip() for s in resume_list if isinstance(s, (str,))}
    jd_map = {str(s).strip().lower(): str(s).strip() for s in jd_list if isinstance(s, (str,))}

    resume_lower = set(resume_map.keys())
    jd_lower = set(jd_map.keys())

    matched_lower = resume_lower & jd_lower
    missing_lower = jd_lower - resume_lower

    # Prefer JD casing for output (consistent with job requirement wording)
    matched_skills = [jd_map[k] for k in sorted(matched_lower)]
    missing_skills = [jd_map[k] for k in sorted(missing_lower)]

    match_score = int(round((len(matched_lower) / len(jd_lower)) * 100)) if jd_lower else 0

    return {
        "match_score": match_score,
        "match_skill": matched_skills,
        "missing_skills": missing_skills,
    }
