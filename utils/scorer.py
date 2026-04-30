"""
scorer.py
"""
import re
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.resume_parser import parse_resume, split_into_sections

# ── Weights ───────────────────────────────────────────────────────────────────
WEIGHTS = {
    "sections":    25,   # standard resume sections present
    "contact":     10,   # email + phone
    "length":      15,   # appropriate word count
    "action_verbs":15,   # strong action verbs
    "quantified":  15,   # numbers / metrics
    "keywords":    10,   # role-relevant keywords found
    "formatting":  10,   # dates, job titles, education detected
}

SECTION_KEYWORDS = [
    "experience", "education", "skills", "projects",
    "certifications", "summary", "objective", "achievements",
    "profile", "work history", "employment", "training",
]

ACTION_VERBS = [
    "managed", "led", "developed", "built", "designed", "implemented",
    "created", "improved", "optimized", "delivered", "launched", "achieved",
    "increased", "reduced", "coordinated", "supervised", "trained", "mentored",
    "analyzed", "researched", "collaborated", "negotiated", "resolved",
    "maintained", "operated", "handled", "organized", "planned", "executed",
    "established", "streamlined", "generated", "oversaw", "directed",
    "facilitated", "administered", "monitored", "evaluated", "prepared",
    "assisted", "supported", "ensured", "provided", "served", "processed",
]

# Generic keywords that appear in good resumes across all domains
QUALITY_KEYWORDS = [
    "team", "project", "client", "customer", "service", "management",
    "communication", "leadership", "strategy", "performance", "results",
    "responsible", "experience", "professional", "certified", "trained",
    "award", "achievement", "promoted", "initiative", "solution",
]


def score_resume_text(text: str, target_role: str = "") -> tuple[int, list[str], list[str]]:
    text_lower = text.lower()
    suggestions = []
    breakdown   = {}

    # 1. Sections
    found_sections = [s for s in SECTION_KEYWORDS if s in text_lower]
    section_score  = min(len(found_sections) * 4, WEIGHTS["sections"])
    breakdown["sections"] = section_score
    if len(found_sections) < 3:
        missing = [s.title() for s in ["Experience", "Education", "Skills", "Summary"]
                   if s.lower() not in found_sections][:3]
        suggestions.append(f"Add missing sections: {', '.join(missing)}.")

    # 2. Contact
    has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.\w{2,}", text))
    has_phone = bool(re.search(r"\+?\d[\d\s\-().]{7,15}\d", text))
    contact_score = (5 if has_email else 0) + (5 if has_phone else 0)
    breakdown["contact"] = contact_score
    if not has_email:
        suggestions.append("Add a professional email address.")
    if not has_phone:
        suggestions.append("Include a contact phone number.")

    # 3. Length
    word_count = len(text.split())
    if 250 <= word_count <= 1000:
        length_score = WEIGHTS["length"]
    elif word_count > 1000:
        length_score = WEIGHTS["length"] - 4
        suggestions.append("Resume is too long. Aim for 250–1000 words.")
    elif word_count >= 100:
        length_score = int(word_count / 250 * WEIGHTS["length"])
        suggestions.append("Resume is too short. Add more detail about your experience.")
    else:
        length_score = 2
        suggestions.append("Resume has very little content. Add experience, skills, and education sections.")
    breakdown["length"] = length_score

    # 4. Action verbs
    verbs_found  = [v for v in ACTION_VERBS if v in text_lower]
    action_score = min(len(verbs_found) * 2, WEIGHTS["action_verbs"])
    breakdown["action_verbs"] = action_score
    if len(verbs_found) < 3:
        suggestions.append("Use strong action verbs like 'Managed', 'Led', 'Achieved', 'Coordinated'.")

    # 5. Quantified achievements
    numbers = re.findall(r"\b\d+[\%\+]?\b", text)
    # Filter out years (4-digit numbers like 2020)
    non_year_numbers = [n for n in numbers if not re.match(r"^(19|20)\d{2}$", n)]
    quant_score = min(len(non_year_numbers) * 2, WEIGHTS["quantified"])
    breakdown["quantified"] = quant_score
    if len(non_year_numbers) < 3:
        suggestions.append("Quantify achievements: e.g., 'Managed a team of 10', 'Increased sales by 25%'.")

    # 6. Role-relevant keywords
    keyword_score = 0
    if target_role:
        role_words = re.sub(r"[^a-z\s]", "", target_role.lower()).split()
        role_words = [w for w in role_words if len(w) > 3]
        matches    = sum(1 for w in role_words if w in text_lower)
        keyword_score = min(matches * 3, WEIGHTS["keywords"])
        # Also check generic quality keywords
        quality_matches = sum(1 for k in QUALITY_KEYWORDS if k in text_lower)
        keyword_score   = min(keyword_score + quality_matches, WEIGHTS["keywords"])
    else:
        quality_matches = sum(1 for k in QUALITY_KEYWORDS if k in text_lower)
        keyword_score   = min(quality_matches, WEIGHTS["keywords"])
    breakdown["keywords"] = keyword_score

    # 7. Formatting quality (dates, job titles, education detected)
    has_dates   = bool(re.search(
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s,]+\d{4}\b"
        r"|\b\d{4}\s*[-–]\s*(\d{4}|present|current)\b", text_lower))
    has_degree  = bool(re.search(
        r"\b(b\.?tech|m\.?tech|bachelor|master|phd|diploma|mba|b\.?sc|m\.?sc|bca|mca|b\.?e|m\.?e|b\.?a|m\.?a)\b",
        text_lower))
    has_jobtitle = bool(re.search(
        r"\b(engineer|developer|manager|analyst|designer|consultant|officer|"
        r"executive|director|coordinator|specialist|associate|intern|lead|head)\b",
        text_lower))
    fmt_score = (4 if has_dates else 0) + (3 if has_degree else 0) + (3 if has_jobtitle else 0)
    breakdown["formatting"] = fmt_score
    if not has_dates:
        suggestions.append("Add dates to your work experience (e.g., 'Jan 2022 – Present').")
    if not has_degree:
        suggestions.append("Include your educational qualification (degree name).")

    total = sum(breakdown.values())
    total = min(total, 100)

    if not suggestions:
        suggestions.append("✅ Your resume is well-structured and ATS-optimized!")

    return total, breakdown, suggestions


def score_resume_file(file_obj, filename: str, target_role: str = "") -> tuple[int, dict, list[str]]:
    """
    Score a resume from an uploaded file.
    Returns: (score, full_parsed_data, suggestions)
    """
    parsed = parse_resume(file_obj, filename)
    score, breakdown, suggestions = score_resume_text(parsed["raw_text"], target_role)
    parsed["score_breakdown"] = breakdown
    return score, parsed, suggestions


def score_resume(text: str, target_role: str = "") -> tuple[int, list, list[str]]:
    """Legacy API for text-based scoring."""
    score, _, suggestions = score_resume_text(text, target_role)
    from utils.resume_parser import extract_skills_from_text
    skills = extract_skills_from_text(text)
    return score, skills, suggestions
