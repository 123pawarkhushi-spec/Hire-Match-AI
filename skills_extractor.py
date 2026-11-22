
import re


# --------------------------------------------------
# SKILLS DATABASE WITH ALIASES
# --------------------------------------------------

SKILLS_DATABASE = {

    # Programming Languages
    "C": ["C"],
    "C++": ["C++"],
    "C#": ["C#"],
    "Java": ["Java"],
    "JavaScript": ["JavaScript", "JS"],
    "Python": ["Python", "Py"],
    "R": ["R"],
    "PHP": ["PHP"],
    "Ruby": ["Ruby"],
    "Go": ["Golang", "Go"],
    "Rust": ["Rust"],
    "Kotlin": ["Kotlin"],
    "Swift": ["Swift"],

    # Database
    "SQL": ["SQL"],
    "MySQL": ["MySQL"],
    "PostgreSQL": ["PostgreSQL", "Postgres"],
    "MongoDB": ["MongoDB"],
    "SQLite": ["SQLite"],
    "Oracle": ["Oracle Database"],
    "Redis": ["Redis"],

    # Python Libraries
    "NumPy": ["NumPy"],
    "Pandas": ["Pandas"],
    "Matplotlib": ["Matplotlib"],
    "Seaborn": ["Seaborn"],
    "Scikit-learn": ["Scikit-learn", "Scikit learn", "sklearn"],
    "SciPy": ["SciPy"],
    "NLTK": ["NLTK"],
    "spaCy": ["spaCy", "Spacy"],
    "OpenCV": ["OpenCV"],
    "Plotly": ["Plotly"],

    # Machine Learning and AI
    "Machine Learning": ["Machine Learning", "ML"],
    "Deep Learning": ["Deep Learning", "DL"],
    "Artificial Intelligence": ["Artificial Intelligence", "AI"],
    "NLP": ["NLP", "Natural Language Processing"],
    "Computer Vision": ["Computer Vision"],
    "Generative AI": ["Generative AI", "GenAI"],
    "LLM": ["LLM", "Large Language Model", "Large Language Models"],
    "Neural Networks": ["Neural Network", "Neural Networks"],
    "TensorFlow": ["TensorFlow"],
    "PyTorch": ["PyTorch"],
    "Keras": ["Keras"],
    "XGBoost": ["XGBoost"],
    "LightGBM": ["LightGBM"],
    "CatBoost": ["CatBoost"],
    "Hugging Face": ["Hugging Face", "Huggingface"],
    "Transformers": ["Transformers"],

    # Data Analysis and Visualization
    "Data Analysis": ["Data Analysis", "Data Analytics"],
    "Data Science": ["Data Science"],
    "Data Visualization": ["Data Visualization"],
    "Power BI": ["Power BI", "PowerBI"],
    "Tableau": ["Tableau"],
    "Excel": ["Excel", "Microsoft Excel"],
    "Statistics": ["Statistics", "Statistical Analysis"],
    "Probability": ["Probability"],
    "ETL": ["ETL"],
    "Data Cleaning": ["Data Cleaning", "Data Cleansing"],

    # Web Development
    "HTML": ["HTML"],
    "CSS": ["CSS"],
    "React": ["React", "React.js", "ReactJS"],
    "Node.js": ["Node.js", "NodeJS"],
    "Angular": ["Angular"],
    "Vue.js": ["Vue.js", "VueJS"],
    "Bootstrap": ["Bootstrap"],
    "Flask": ["Flask"],
    "Django": ["Django"],
    "FastAPI": ["FastAPI"],

    # Tools
    "Git": ["Git"],
    "GitHub": ["GitHub"],
    "Docker": ["Docker"],
    "Kubernetes": ["Kubernetes"],
    "Linux": ["Linux"],
    "AWS": ["AWS", "Amazon Web Services"],
    "Azure": ["Microsoft Azure", "Azure"],
    "Google Cloud": ["Google Cloud", "GCP"],
    "Jupyter": ["Jupyter", "Jupyter Notebook"],
    "Streamlit": ["Streamlit"],
    "VS Code": ["VS Code", "Visual Studio Code"],

    # Concepts
    "Data Structures": ["Data Structures", "DS"],
    "Algorithms": ["Algorithms"],
    "Object Oriented Programming": [
        "Object Oriented Programming",
        "OOP",
        "OOPs"
    ],
    "DBMS": ["DBMS", "Database Management System"],
    "Operating Systems": ["Operating Systems", "OS"],
    "Computer Networks": ["Computer Networks"],
    "Software Engineering": ["Software Engineering"],
    "REST API": ["REST API", "REST APIs", "RESTful API"],
    "API": ["API", "APIs"],
}


# --------------------------------------------------
# SKILL EXTRACTION
# --------------------------------------------------

def extract_skills(text):

    found_skills = []

    if not text:
        return found_skills

    for canonical_skill, aliases in SKILLS_DATABASE.items():

        for alias in aliases:

            # Special handling for single-character C
            if alias == "C":
                pattern = r"(?<![A-Za-z0-9])C(?![A-Za-z0-9])"

            # Special handling for C++
            elif alias == "C++":
                pattern = r"(?<![A-Za-z0-9])C\+\+(?![A-Za-z0-9])"

            # Special handling for C#
            elif alias == "C#":
                pattern = r"(?<![A-Za-z0-9])C#(?![A-Za-z0-9])"

            else:
                pattern = (
                    r"(?<![A-Za-z0-9])"
                    + re.escape(alias)
                    + r"(?![A-Za-z0-9])"
                )

            if re.search(pattern, text, re.IGNORECASE):

                found_skills.append(canonical_skill)
                break

    return found_skills
