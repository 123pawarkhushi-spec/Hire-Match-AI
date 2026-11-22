
import re

EDUCATION_PATTERNS = [
    r"\bb\.?\s*tech\b",
    r"\bb\.?\s*e\.?\b",
    r"\bbca\b",
    r"\bmca\b",
    r"\bb\.?\s*sc\b",
    r"\bm\.?\s*sc\b",
    r"\bmba\b",
    r"\bbachelor\b",
    r"\bmaster\b",
    r"\bph\.?\s*d\b",
    r"\bdiploma\b",
    r"\b12th\b",
    r"\b10th\b",
    r"\bclass\s*12\b",
    r"\bclass\s*10\b"
]

def extract_education(text):
    education = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        for pattern in EDUCATION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                education.append(line)
                break

    return list(dict.fromkeys(education))
