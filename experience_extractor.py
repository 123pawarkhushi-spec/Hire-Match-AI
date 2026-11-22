
import re

EXPERIENCE_KEYWORDS = [
    "intern",
    "internship",
    "worked at",
    "employed at",
    "professional experience",
    "work experience"
]

def extract_experience(text):
    experience = []

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        for keyword in EXPERIENCE_KEYWORDS:
            if re.search(re.escape(keyword), line, re.IGNORECASE):
                experience.append(line)
                break

    return list(dict.fromkeys(experience))
