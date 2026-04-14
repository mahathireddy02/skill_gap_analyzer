import re

SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "html", "css",
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "data analysis", "data science", "data engineering", "devops", "agile", "scrum",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "rest api", "graphql", "microservices", "ci/cd", "terraform",
]

SECTION_KEYWORDS = ["experience", "education", "projects", "skills", "certifications", "summary", "objective"]

def extract_skills(text):
    text_lower = text.lower()
    return [s for s in SKILL_KEYWORDS if s in text_lower]

def score_resume(text):
    text_lower = text.lower()
    found_skills = extract_skills(text)
    skill_score = min(len(found_skills) * 4, 40)

    sections = sum(1 for s in SECTION_KEYWORDS if s in text_lower)
    section_score = min(sections * 5, 30)

    word_count = len(text.split())
    length_score = 15 if 200 <= word_count <= 800 else (10 if word_count > 800 else 5)

    email_score = 5 if re.search(r"[\w.+-]+@[\w-]+\.\w+", text) else 0
    phone_score = 5 if re.search(r"\+?\d[\d\s\-]{8,}", text) else 0
    action_verbs = ["developed", "built", "designed", "implemented", "led", "managed", "created", "improved"]
    action_score = 5 if any(v in text_lower for v in action_verbs) else 0

    total = skill_score + section_score + length_score + email_score + phone_score + action_score

    suggestions = []
    if skill_score < 20:
        suggestions.append("Add more technical skills relevant to your target role.")
    if section_score < 20:
        suggestions.append("Include standard sections: Experience, Education, Skills, Projects.")
    if length_score < 10:
        suggestions.append("Resume is too short. Add more detail about your experience and projects.")
    if not email_score:
        suggestions.append("Add a professional email address.")
    if not phone_score:
        suggestions.append("Include a contact phone number.")
    if not action_score:
        suggestions.append("Use action verbs like 'Developed', 'Built', 'Led' to describe achievements.")

    return min(total, 100), found_skills, suggestions
