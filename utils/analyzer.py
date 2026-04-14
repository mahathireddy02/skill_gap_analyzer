ROLE_SKILLS = {
    "Data Scientist": ["python", "machine learning", "deep learning", "pandas", "numpy",
                       "scikit-learn", "sql", "tensorflow", "data analysis", "matplotlib"],
    "Web Developer": ["html", "css", "javascript", "react", "node", "rest api",
                      "git", "sql", "typescript", "docker"],
    "Backend Developer": ["python", "java", "sql", "rest api", "docker", "git",
                          "postgresql", "redis", "microservices", "ci/cd"],
    "Frontend Developer": ["html", "css", "javascript", "react", "typescript",
                           "git", "vue", "angular", "graphql", "figma"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "ci/cd", "linux", "git",
                        "terraform", "python", "ansible", "monitoring"],
    "Data Engineer": ["python", "sql", "spark", "airflow", "aws", "data pipelines",
                      "postgresql", "kafka", "docker", "git"],
    "ML Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch",
                    "docker", "aws", "mlops", "git", "sql"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node", "python",
                             "sql", "docker", "git", "rest api"],
    "Android Developer": ["java", "kotlin", "android sdk", "git", "rest api",
                          "firebase", "sql", "mvvm", "jetpack compose", "testing"],
    "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform",
                       "linux", "python", "ci/cd", "networking"],
}

def get_roles():
    return list(ROLE_SKILLS.keys())

def analyze_gap(user_skills, role):
    required = ROLE_SKILLS.get(role, [])
    user_lower = [s.lower() for s in user_skills]
    matched = [s for s in required if s.lower() in user_lower]
    missing = [s for s in required if s.lower() not in user_lower]
    return matched, missing, required
