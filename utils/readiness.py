from typing import Optional


def calculate_readiness(
    skills: Optional[list],
    missing_skills: Optional[list],
    gap_analyzed: bool = False,
    gap_result: Optional[dict] = None,
) -> int:
    """Return target-role readiness from the saved skill-gap result."""
    if not gap_analyzed:
        return 0

    gap_result = gap_result or {}
    if "score" in gap_result:
        return int(round(float(gap_result.get("score") or 0)))

    matched = gap_result.get("matched_skills") or skills or []
    missing_skills = gap_result.get("missing_skills") or missing_skills or []
    total = len(matched) + len(missing_skills)
    if total == 0:
        return 0
    return int(len(matched) / total * 100)


def has_gap_analysis(user: Optional[dict]) -> bool:
    user = user or {}
    return bool(user.get("gap_analyzed") or user.get("gap_result") or user.get("missing_skills"))
