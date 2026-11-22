
# --------------------------------------------------
# SKILL MATCHING ENGINE
# --------------------------------------------------

def compare_skills(candidate_skills, job_skills):

    # Remove duplicates while preserving order
    candidate_skills = list(dict.fromkeys(candidate_skills))
    job_skills = list(dict.fromkeys(job_skills))

    matched_skills = []
    missing_skills = []

    # Compare candidate skills with required job skills
    for skill in job_skills:

        if skill in candidate_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate skill match percentage
    total_required = len(job_skills)

    if total_required > 0:

        matching_score = (
            len(matched_skills) / total_required
        ) * 100

    else:
        matching_score = 0

    matching_score = round(matching_score, 2)

    # Match status
    if total_required == 0:
        match_status = "No requirements detected"

    elif matching_score >= 80:
        match_status = "High Skill Match"

    elif matching_score >= 50:
        match_status = "Moderate Skill Match"

    else:
        match_status = "Low Skill Match"

    # Detailed report
    skill_report = []

    for skill in job_skills:

        if skill in candidate_skills:

            skill_report.append({
                "skill": skill,
                "status": "Matched"
            })

        else:

            skill_report.append({
                "skill": skill,
                "status": "Missing"
            })

    # Return results
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matching_score": matching_score,
        "match_status": match_status,
        "skill_report": skill_report
    }
