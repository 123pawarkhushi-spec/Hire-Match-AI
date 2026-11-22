from utils.skills_extractor import extract_skills
from utils.education_extractor import extract_education
from utils.experience_extractor import extract_experience


def extract_candidate_profile(resume_text):
    profile = {
        "skills": extract_skills(resume_text),
        "education": extract_education(resume_text),
        "experience": extract_experience(resume_text)
    }

    return profile