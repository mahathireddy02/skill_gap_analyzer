import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.request_response import AnalyzeRequest, AnalyzeResponse, RolesResponse
from services.analyzer import analyze_skill_gap, get_all_roles

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Skill Gap Analyzer API",
    description="Analyze skill gaps between user skills and target job roles.",
    version="1.0.0",
)

# ── CORS (allows Streamlit frontend on any localhost port) ────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Skill Gap Analyzer API is running."}


@app.get("/roles", response_model=RolesResponse, tags=["Roles"])
def get_roles():
    """Returns all available job roles."""
    roles = get_all_roles()
    logger.info(f"GET /roles → {len(roles)} roles returned")
    return {"roles": roles}


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
def analyze(request: AnalyzeRequest):
    """
    Analyze skill gap for a given role and user skill list.

    - **role**: Target job role (e.g. "Flutter Developer")
    - **skills**: List of skills the user already has
    """
    logger.info(f"POST /analyze | role='{request.role}' | skills={request.skills}")
    return analyze_skill_gap(role=request.role, user_skills=request.skills)
