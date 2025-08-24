def calculate_match(resume_data: dict, jd_data: dict) -> dict:
    resume_list = resume_data.get("skills", []) or []
    # ✅ accept either "skills_required" or "skills"
    jd_list = jd_data.get("skills_required", jd_data.get("skills", [])) or []

    # Build lowercase maps to original casing
    resume_map = {str(s).strip().lower(): str(s).strip() for s in resume_list if isinstance(s, str)}
    jd_map = {str(s).strip().lower(): str(s).strip() for s in jd_list if isinstance(s, str)}

    resume_lower = set(resume_map.keys())
    jd_lower = set(jd_map.keys())

    matched_lower = resume_lower & jd_lower
    missing_lower = jd_lower - resume_lower

    matched_skills = [jd_map[k] for k in sorted(matched_lower)]
    missing_skills = [jd_map[k] for k in sorted(missing_lower)]

    match_score = int(round((len(matched_lower) / len(jd_lower)) * 100)) if jd_lower else 0

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }