from pydantic import BaseModel, field_validator
from typing import List


class AnalyzeRequest(BaseModel):
    role: str
    skills: List[str]

    @field_validator("skills")
    @classmethod
    def deduplicate_skills(cls, v):
        seen = set()
        result = []
        for skill in v:
            normalized = skill.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(skill.strip())
        return result

    @field_validator("role")
    @classmethod
    def strip_role(cls, v):
        return v.strip()


class AnalyzeResponse(BaseModel):
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]


class RolesResponse(BaseModel):
    roles: List[str]
