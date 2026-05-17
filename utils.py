from docx import Document


def extract_text(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception:
        return ""


# Comprehensive skill list
SKILLS_LIST = [
    # Programming
    "python", "java", "c++", "javascript",

    # Web Development
    "html", "css", "react", "angular", "node.js", "bootstrap",

    # Backend Frameworks
    "spring", "spring boot", "django", "flask", "express",

    # Machine Learning / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch",

    # Data Analysis
    "data analysis", "data visualization", "matplotlib", "seaborn",
    "excel", "power bi", "tableau",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle",

    # DevOps
    "docker", "aws", "kubernetes", "ci/cd", "jenkins", "linux",

    # General Tools
    "git", "api", "rest", "microservices"
]


def extract_skills(text):
    text = text.lower()
    detected_skills = []

    for skill in SKILLS_LIST:
        if skill in text:
            detected_skills.append(skill)

    return list(set(detected_skills))


def assign_role(skills):
    skills = set(skills)

    role_scores = {
        "Machine Learning Engineer": 0,
        "NLP Engineer": 0,
        "Data Scientist": 0,
        "Data Analyst": 0,
        "Frontend Developer": 0,
        "Backend Developer": 0,
        "DevOps Engineer": 0,
        "Database Engineer": 0,
        "Software Engineer": 0
    }

    # Machine Learning Engineer
    ml_engineer_skills = {
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "keras"
    }
    role_scores["Machine Learning Engineer"] += len(ml_engineer_skills & skills) * 3

    # NLP Engineer
    nlp_skills = {
        "nlp", "machine learning", "deep learning"
    }
    role_scores["NLP Engineer"] += len(nlp_skills & skills) * 4

    # Data Scientist
    data_science_skills = {
        "machine learning", "pandas", "numpy", "data analysis", "data visualization"
    }
    role_scores["Data Scientist"] += len(data_science_skills & skills) * 3

    # Data Analyst
    data_analyst_skills = {
        "excel", "sql", "power bi", "tableau", "data visualization"
    }
    role_scores["Data Analyst"] += len(data_analyst_skills & skills) * 3

    # Frontend Developer
    frontend_skills = {
        "react", "angular", "javascript", "html", "css", "bootstrap"
    }
    role_scores["Frontend Developer"] += len(frontend_skills & skills) * 2

    # Backend Developer
    backend_skills = {
        "node.js", "django", "flask", "spring", "java"
    }
    role_scores["Backend Developer"] += len(backend_skills & skills) * 2

    # DevOps Engineer
    devops_skills = {
        "aws", "docker", "kubernetes", "ci/cd", "jenkins", "linux"
    }
    role_scores["DevOps Engineer"] += len(devops_skills & skills) * 2

    # Database Engineer
    database_skills = {
        "sql", "mysql", "postgresql", "mongodb", "oracle"
    }
    role_scores["Database Engineer"] += len(database_skills & skills) * 2

    # Software Engineer (fallback)
    general_skills = {"python", "java", "c++"}
    role_scores["Software Engineer"] += len(general_skills & skills)

    # Select role with highest score
    best_role = max(role_scores, key=role_scores.get)

    return best_role