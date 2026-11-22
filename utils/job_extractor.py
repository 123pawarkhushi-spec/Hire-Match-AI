
from utils.skills_extractor import extract_skills


def extract_job_skills(job_description):

    required_skills = extract_skills(job_description)

    return required_skills
