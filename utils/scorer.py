"""
scorer.py
"""
import re
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.resume_parser import parse_resume, split_into_sections
from utils.skill_analyzer import ROLE_DATASET, skill_similarity

# ── Weights ───────────────────────────────────────────────────────────────────
WEIGHTS = {
    "sections":    20,   # standard resume sections present
    "contact":     10,   # email + phone
    "length":      10,   # appropriate word count
    "action_verbs":10,   # strong action verbs
    "quantified":  10,   # numbers / metrics
    "keywords":    30,   # role-relevant skill keywords (main signal)
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

# Tier weights mirror skill_analyzer.py
_TIER_W = {"core": 1.0, "important": 0.6, "nice_to_have": 0.3}
_SIM_THRESHOLD = 0.75


def _role_keyword_score(text_lower: str, target_role: str) -> tuple[int, list[str], list[str]]:
    """
    Score the keywords component using the ROLE_DATASET.
    Returns (score_0_to_30, matched_skills, missing_core_skills).
    Falls back to generic quality keywords if role not in dataset.
    """
    # ── Fuzzy-match role name to dataset ─────────────────────────────────────
    role_key = None
    if target_role:
        role_lower = target_role.lower().strip()
        # Exact match first
        for k in ROLE_DATASET:
            if k.lower() == role_lower:
                role_key = k
                break
        # Partial / fuzzy match
        if not role_key:
            best_sim, best_k = 0.0, None
            for k in ROLE_DATASET:
                sim = skill_similarity(role_lower, k.lower())
                if sim > best_sim:
                    best_sim, best_k = sim, k
            if best_sim >= 0.55:
                role_key = best_k

    if not role_key:
        # Generic fallback — count quality words
        QUALITY_KEYWORDS = [
            "team", "project", "client", "customer", "service", "management",
            "communication", "leadership", "strategy", "performance", "results",
            "responsible", "professional", "certified", "solution",
        ]
        hits = sum(1 for k in QUALITY_KEYWORDS if k in text_lower)
        return min(hits * 2, WEIGHTS["keywords"]), [], []

    role_data = ROLE_DATASET[role_key]
    total_w, earned_w = 0.0, 0.0
    matched, missing_core = [], []

    for tier, tw in _TIER_W.items():
        for skill in role_data.get(tier, []):
            total_w += tw
            # Check if skill (or close variant) appears in resume text
            found = False
            # Direct substring check first (fast)
            if skill in text_lower:
                found = True
            else:
                # Fuzzy: split resume into tokens and compare
                for token in re.findall(r"[\w/+#.-]+", text_lower):
                    if skill_similarity(token, skill) >= _SIM_THRESHOLD:
                        found = True
                        break
                # Also try multi-word skill as a phrase
                if not found and " " in skill:
                    words = skill.split()
                    if all(w in text_lower for w in words):
                        found = True

            if found:
                earned_w += tw
                matched.append(skill)
            elif tier == "core":
                missing_core.append(skill)

    raw_ratio = earned_w / total_w if total_w > 0 else 0.0
    score = round(raw_ratio * WEIGHTS["keywords"])
    return min(score, WEIGHTS["keywords"]), matched, missing_core


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
        length_score = WEIGHTS["length"] - 3
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
    non_year_numbers = [n for n in numbers if not re.match(r"^(19|20)\d{2}$", n)]
    quant_score = min(len(non_year_numbers) * 2, WEIGHTS["quantified"])
    breakdown["quantified"] = quant_score
    if len(non_year_numbers) < 3:
        suggestions.append("Quantify achievements: e.g., 'Managed a team of 10', 'Increased sales by 25%'.")

    # 6. Role-relevant keywords (uses ROLE_DATASET)
    keyword_score, matched_skills, missing_core = _role_keyword_score(text_lower, target_role)
    breakdown["keywords"] = keyword_score

    if target_role and missing_core:
        top_missing = ", ".join(s.title() for s in missing_core[:4])
        suggestions.append(f"Add core {target_role} skills missing from your resume: {top_missing}.")
    elif target_role and keyword_score < WEIGHTS["keywords"] * 0.5:
        suggestions.append(f"Include more {target_role}-specific skills and technologies in your resume.")

    # 7. Formatting quality
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

    total = min(sum(breakdown.values()), 100)

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
