"""
skill_analyzer.py
Intelligent skill gap analysis engine.
Uses weighted role requirements, fuzzy similarity matching,
and skill importance tiers to produce accurate gap reports.
"""

from difflib import SequenceMatcher

# ── Role Skill Dataset ────────────────────────────────────────────────────────
# Each role has: core (must-have), important (high value), nice_to_have
ROLE_DATASET = {
    "Data Scientist": {
        "core":         ["python", "machine learning", "pandas", "numpy", "scikit-learn", "sql"],
        "important":    ["deep learning", "tensorflow", "pytorch", "data analysis", "matplotlib", "statistics"],
        "nice_to_have": ["spark", "aws", "docker", "mlops", "tableau", "r"],
        "description":  "Builds ML models and extracts insights from data.",
    },
    "Frontend Developer": {
        "core":         ["html", "css", "javascript", "react", "git"],
        "important":    ["typescript", "tailwind", "redux", "rest api", "figma"],
        "nice_to_have": ["next", "vue", "angular", "graphql", "webpack", "jest"],
        "description":  "Builds user interfaces and web experiences.",
    },
    "Backend Developer": {
        "core":         ["python", "sql", "rest api", "git", "docker"],
        "important":    ["postgresql", "redis", "microservices", "ci/cd", "linux"],
        "nice_to_have": ["java", "golang", "kafka", "kubernetes", "grpc", "elasticsearch"],
        "description":  "Builds server-side logic, APIs, and databases.",
    },
    "Full Stack Developer": {
        "core":         ["html", "css", "javascript", "react", "node", "sql", "git"],
        "important":    ["typescript", "rest api", "docker", "postgresql", "python"],
        "nice_to_have": ["next", "graphql", "redis", "aws", "ci/cd", "mongodb"],
        "description":  "Builds both frontend and backend of web applications.",
    },
    "DevOps Engineer": {
        "core":         ["docker", "kubernetes", "linux", "git", "ci/cd", "aws"],
        "important":    ["terraform", "ansible", "python", "bash", "prometheus", "grafana"],
        "nice_to_have": ["helm", "istio", "azure", "gcp", "jenkins", "elk stack"],
        "description":  "Manages infrastructure, deployments, and automation.",
    },
    "ML Engineer": {
        "core":         ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "git"],
        "important":    ["mlops", "docker", "aws", "sql", "scikit-learn", "mlflow"],
        "nice_to_have": ["kubernetes", "spark", "kafka", "kubeflow", "fastapi", "airflow"],
        "description":  "Deploys and scales ML models in production.",
    },
    "Data Engineer": {
        "core":         ["python", "sql", "spark", "airflow", "git"],
        "important":    ["kafka", "aws", "docker", "postgresql", "dbt", "data pipelines"],
        "nice_to_have": ["scala", "kubernetes", "snowflake", "databricks", "bigquery", "flink"],
        "description":  "Builds data pipelines and infrastructure.",
    },
    "Android Developer": {
        "core":         ["kotlin", "android", "git", "rest api", "java"],
        "important":    ["jetpack compose", "firebase", "mvvm", "sql", "testing"],
        "nice_to_have": ["flutter", "dart", "ci/cd", "kotlin coroutines", "dagger", "hilt"],
        "description":  "Builds native Android mobile applications.",
    },
    "iOS Developer": {
        "core":         ["swift", "ios", "xcode", "git", "rest api"],
        "important":    ["swiftui", "firebase", "core data", "testing", "mvvm"],
        "nice_to_have": ["objective-c", "react native", "flutter", "ci/cd", "instruments"],
        "description":  "Builds native iOS mobile applications.",
    },
    "Flutter Developer": {
        "core":         ["flutter", "dart", "git", "rest api"],
        "important":    ["firebase", "state management", "android", "ios", "testing"],
        "nice_to_have": ["ci/cd", "figma", "graphql", "sqlite", "bloc", "riverpod"],
        "description":  "Builds cross-platform mobile apps with Flutter.",
    },
    "Cloud Engineer": {
        "core":         ["aws", "docker", "kubernetes", "terraform", "linux"],
        "important":    ["azure", "gcp", "python", "ci/cd", "networking", "bash"],
        "nice_to_have": ["ansible", "helm", "prometheus", "grafana", "security", "cost optimization"],
        "description":  "Designs and manages cloud infrastructure.",
    },
    "Data Analyst": {
        "core":         ["sql", "excel", "python", "data analysis"],
        "important":    ["power bi", "tableau", "pandas", "statistics", "matplotlib"],
        "nice_to_have": ["r", "looker", "bigquery", "machine learning", "numpy", "seaborn"],
        "description":  "Analyzes data and creates reports and dashboards.",
    },
    "Cybersecurity Engineer": {
        "core":         ["networking", "linux", "python", "security"],
        "important":    ["penetration testing", "cryptography", "firewalls", "bash", "git"],
        "nice_to_have": ["aws", "docker", "kubernetes", "siem", "incident response", "cloud security"],
        "description":  "Protects systems and networks from threats.",
    },
    "QA Engineer": {
        "core":         ["selenium", "python", "git", "sql", "testing"],
        "important":    ["pytest", "ci/cd", "rest api", "jira", "postman"],
        "nice_to_have": ["cypress", "jest", "performance testing", "docker", "java", "appium"],
        "description":  "Ensures software quality through automated and manual testing.",
    },
    "Web Developer": {
        "core":         ["html", "css", "javascript", "git"],
        "important":    ["react", "node", "sql", "rest api", "typescript"],
        "nice_to_have": ["docker", "aws", "graphql", "mongodb", "next", "tailwind"],
        "description":  "Builds and maintains websites and web applications.",
    },
}

# Tier weights for scoring
TIER_WEIGHTS = {"core": 1.0, "important": 0.6, "nice_to_have": 0.3}


# ── Similarity Engine ─────────────────────────────────────────────────────────

def skill_similarity(a: str, b: str) -> float:
    """Compute similarity between two skill strings."""
    a, b = a.lower().strip(), b.lower().strip()
    if a == b:
        return 1.0
    # Substring containment
    if a in b or b in a:
        return 0.9
    return SequenceMatcher(None, a, b).ratio()


def best_match_score(user_skill: str, required_skills: list[str]) -> tuple[float, str]:
    """Find the best matching required skill for a user skill."""
    best_score, best_skill = 0.0, ""
    for req in required_skills:
        score = skill_similarity(user_skill, req)
        if score > best_score:
            best_score, best_skill = score, req
    return best_score, best_skill


# ── Core Analysis ─────────────────────────────────────────────────────────────

def analyze_skill_gap(user_skills: list[str], role: str, threshold: float = 0.75) -> dict:
    """
    Full skill gap analysis with weighted scoring.

    Returns:
    {
        role, score, grade,
        matched_skills, missing_skills, partial_matches,
        strengths, weaknesses,
        core_coverage, important_coverage,
        recommendations, role_description
    }
    """
    if role not in ROLE_DATASET:
        available = list(ROLE_DATASET.keys())
        raise ValueError(f"Role '{role}' not found. Available: {available}")

    role_data   = ROLE_DATASET[role]
    user_lower  = [s.lower().strip() for s in user_skills]

    matched_skills   = []
    missing_skills   = []
    partial_matches  = []  # skills where similarity is 0.5–0.74

    # Track per-tier coverage
    tier_scores = {}

    for tier, weight in TIER_WEIGHTS.items():
        tier_required = role_data.get(tier, [])
        tier_matched, tier_missing = [], []

        for req_skill in tier_required:
            best_score, best_user_skill = 0.0, ""
            for u_skill in user_lower:
                score = skill_similarity(u_skill, req_skill)
                if score > best_score:
                    best_score, best_user_skill = score, u_skill

            if best_score >= threshold:
                matched_skills.append(req_skill)
                tier_matched.append(req_skill)
            elif best_score >= 0.5:
                partial_matches.append({
                    "required": req_skill,
                    "user_has": best_user_skill,
                    "similarity": round(best_score, 2),
                    "tier": tier,
                })
                tier_missing.append(req_skill)
            else:
                missing_skills.append(req_skill)
                tier_missing.append(req_skill)

        tier_scores[tier] = {
            "matched": len(tier_matched),
            "total":   len(tier_required),
            "coverage": round(len(tier_matched) / len(tier_required) * 100, 1) if tier_required else 100.0,
        }

    # Weighted score calculation
    total_weight, earned_weight = 0.0, 0.0
    for tier, weight in TIER_WEIGHTS.items():
        tier_required = role_data.get(tier, [])
        tier_matched_count = tier_scores[tier]["matched"]
        total_weight  += len(tier_required) * weight
        earned_weight += tier_matched_count * weight

    score = round((earned_weight / total_weight * 100), 1) if total_weight > 0 else 0.0

    # Grade
    grade = (
        "A+" if score >= 90 else
        "A"  if score >= 80 else
        "B"  if score >= 65 else
        "C"  if score >= 50 else
        "D"  if score >= 35 else "F"
    )

    # Strengths: user skills that match known skills across ALL roles
    all_role_skills = {
        s for rd in ROLE_DATASET.values()
        for tier_skills in rd.values()
        if isinstance(tier_skills, list)
        for s in tier_skills
    }
    strengths = [s for s in user_lower if any(
        skill_similarity(s, known) >= threshold for known in all_role_skills
    )]

    # Prioritized recommendations: core missing first, then important
    recommendations = (
        [s for s in missing_skills if s in role_data.get("core", [])] +
        [s for s in missing_skills if s in role_data.get("important", [])] +
        [s for s in missing_skills if s in role_data.get("nice_to_have", [])]
    )

    return {
        "role":               role,
        "score":              score,
        "grade":              grade,
        "matched_skills":     matched_skills,
        "missing_skills":     missing_skills,
        "partial_matches":    partial_matches,
        "strengths":          strengths,
        "core_coverage":      tier_scores["core"]["coverage"],
        "important_coverage": tier_scores["important"]["coverage"],
        "tier_breakdown":     tier_scores,
        "recommendations":    recommendations,
        "role_description":   role_data.get("description", ""),
    }


def get_roles() -> list[str]:
    return sorted(ROLE_DATASET.keys())


def get_role_requirements(role: str) -> dict:
    """Return full skill requirements for a role."""
    if role not in ROLE_DATASET:
        raise ValueError(f"Role '{role}' not found.")
    return ROLE_DATASET[role]


def suggest_roles(user_skills: list[str], top_n: int = 3) -> list[dict]:
    """
    Given user skills, suggest the top N best-fit roles.
    Useful for users who don't know what role to target.
    """
    scores = []
    for role in ROLE_DATASET:
        result = analyze_skill_gap(user_skills, role)
        scores.append({"role": role, "score": result["score"], "grade": result["grade"]})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_n]
