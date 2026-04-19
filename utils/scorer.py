"""
scorer.py
ATS-style resume scoring using the new resume_parser.
Scores across 6 dimensions: skills, sections, length,
contact info, action verbs, and quantified achievements.
"""

import re
from utils.resume_parser import parse_resume, extract_skills_from_text, split_into_sections

# ── ATS Scoring Weights ───────────────────────────────────────────────────────
WEIGHTS = {
    "skills":        35,   # technical skills detected
    "sections":      25,   # standard resume sections present
    "contact":       10,   # email, phone present
    "length":        10,   # appropriate word count
    "action_verbs":  10,   # strong action verbs used
    "quantified":    10,   # numbers/metrics in experience
}

SECTION_KEYWORDS = [
    "experience", "education", "projects", "skills",
    "certifications", "summary", "objective", "achievements",
]

ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "led", "managed",
    "created", "improved", "optimized", "deployed", "architected",
    "automated", "reduced", "increased", "delivered", "launched",
    "collaborated", "mentored", "researched", "analyzed", "engineered",
    "integrated", "migrated", "scaled", "refactored", "maintained",
]


def score_resume_text(text: str) -> tuple[int, list[str], list[str]]:
    """
    Score a resume from raw text.
    Returns: (score 0-100, detected_skills, suggestions)
    """
    text_lower = text.lower()
    suggestions = []

    # 1. Skills score
    skills = extract_skills_from_text(text)
    skill_count = len(skills)
    skill_score = min(skill_count * 3, WEIGHTS["skills"])
    if skill_score < WEIGHTS["skills"] * 0.5:
        suggestions.append("Add more technical skills relevant to your target role (languages, tools, frameworks).")

    # 2. Sections score
    sections_found = sum(1 for s in SECTION_KEYWORDS if s in text_lower)
    section_score  = min(sections_found * 4, WEIGHTS["sections"])
    if sections_found < 4:
        missing_secs = [s.title() for s in SECTION_KEYWORDS if s not in text_lower][:3]
        suggestions.append(f"Add missing sections: {', '.join(missing_secs)}.")

    # 3. Contact score
    has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.\w{2,}", text))
    has_phone = bool(re.search(r"\+?\d[\d\s\-().]{8,15}\d", text))
    contact_score = (5 if has_email else 0) + (5 if has_phone else 0)
    if not has_email:
        suggestions.append("Add a professional email address.")
    if not has_phone:
        suggestions.append("Include a contact phone number.")

    # 4. Length score
    word_count = len(text.split())
    if 300 <= word_count <= 900:
        length_score = WEIGHTS["length"]
    elif word_count > 900:
        length_score = WEIGHTS["length"] - 3
        suggestions.append("Resume is too long. Keep it to 1 page (300–900 words) for ATS.")
    else:
        length_score = max(0, int(word_count / 300 * WEIGHTS["length"]))
        suggestions.append("Resume is too short. Add more detail about your experience and projects.")

    # 5. Action verbs score
    verbs_found = sum(1 for v in ACTION_VERBS if v in text_lower)
    action_score = min(verbs_found * 2, WEIGHTS["action_verbs"])
    if verbs_found < 3:
        suggestions.append("Use strong action verbs: 'Developed', 'Implemented', 'Optimized', 'Led'.")

    # 6. Quantified achievements score
    numbers_found = len(re.findall(r"\b\d+[\%\+x]?\b", text))
    quant_score = min(numbers_found * 2, WEIGHTS["quantified"])
    if numbers_found < 3:
        suggestions.append("Quantify achievements: e.g., 'Improved performance by 40%', 'Led a team of 5'.")

    total = skill_score + section_score + contact_score + length_score + action_score + quant_score
    total = min(total, 100)

    if not suggestions:
        suggestions.append("✅ Your resume is well-structured and ATS-optimized!")

    return total, skills, suggestions


def score_resume(text: str) -> tuple[int, list[str], list[str]]:
    """Public API — scores resume from raw text string."""
    return score_resume_text(text)


def score_resume_file(file_obj, filename: str) -> tuple[int, dict, list[str]]:
    """
    Score a resume from an uploaded file (PDF or DOCX).
    Returns: (score, full_parsed_data, suggestions)
    """
    parsed = parse_resume(file_obj, filename)
    score, _, suggestions = score_resume_text(parsed["raw_text"])
    return score, parsed, suggestions
