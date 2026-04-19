import json
import logging
from pathlib import Path
from fastapi import HTTPException

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent.parent / "data" / "skills_data.json"


def load_skills_data() -> dict:
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"skills_data.json not found at {DATA_PATH}")
        raise HTTPException(status_code=500, detail="Skills dataset not found.")
    except json.JSONDecodeError:
        logger.error("skills_data.json is malformed.")
        raise HTTPException(status_code=500, detail="Skills dataset is corrupted.")


def get_all_roles() -> list[str]:
    data = load_skills_data()
    return sorted(data.keys())


def analyze_skill_gap(role: str, user_skills: list[str]) -> dict:
    data = load_skills_data()

    # Case-insensitive role lookup
    role_map = {r.lower(): r for r in data}
    matched_role = role_map.get(role.lower())

    if not matched_role:
        logger.warning(f"Role not found: '{role}'")
        raise HTTPException(
            status_code=404,
            detail=f"Role '{role}' not found. Use GET /roles to see available roles."
        )

    required_skills: list[str] = data[matched_role]
    required_lower = {s.lower(): s for s in required_skills}
    user_lower = {s.lower() for s in user_skills}

    matched = [required_lower[s] for s in required_lower if s in user_lower]
    missing = [required_lower[s] for s in required_lower if s not in user_lower]

    total = len(required_skills)
    score = round((len(matched) / total) * 100, 1) if total > 0 else 0.0

    logger.info(f"Analyzed role='{matched_role}' | score={score}% | matched={len(matched)} | missing={len(missing)}")

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": missing,  # can be extended with course links later
    }
