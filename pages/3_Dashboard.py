import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from components.navbar import show_navbar

st.set_page_config(page_title="Dashboard · SkillGap", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")
require_login()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="stSidebar"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"],.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.block-container{padding:1.5rem 2rem 2rem!important;max-width:100%!important;}
.stat-card{background:rgba(255,255,255,0.06);border-radius:16px;padding:1.3rem 1rem;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 2px 12px rgba(0,0,0,0.2);text-align:center;transition:transform 0.2s,box-shadow 0.2s;}
.stat-card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(124,58,237,0.2);}
.sc-icon{font-size:1.8rem;margin-bottom:0.35rem;}
.sc-val{font-size:1.85rem;font-weight:800;line-height:1;}
.sc-lbl{font-size:0.8rem;color:rgba(255,255,255,0.5);margin-top:0.2rem;}
.feat-card{background:rgba(255,255,255,0.05);border-radius:16px;padding:1.4rem;
    border:1px solid rgba(255,255,255,0.08);height:100%;
    transition:box-shadow 0.22s,border-color 0.22s;}
.feat-card:hover{box-shadow:0 8px 24px rgba(124,58,237,0.2);border-color:rgba(167,139,250,0.4);}
.fci{font-size:2rem;margin-bottom:0.5rem;}
.fct{font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.3rem;}
.fcd{font-size:0.81rem;color:rgba(255,255,255,0.55);line-height:1.5;}
.fcb{display:inline-block;background:rgba(124,58,237,0.2);color:#a78bfa;font-size:0.7rem;
    font-weight:600;padding:0.15rem 0.5rem;border-radius:999px;margin-top:0.5rem;
    border:1px solid rgba(167,139,250,0.3);}
.chip-g{display:inline-block;padding:0.25rem 0.7rem;border-radius:999px;font-size:0.79rem;
    font-weight:600;margin:0.15rem;background:rgba(16,185,129,0.15);color:#34d399;
    border:1px solid rgba(16,185,129,0.3);}
.chip-r{display:inline-block;padding:0.25rem 0.7rem;border-radius:999px;font-size:0.79rem;
    font-weight:600;margin:0.15rem;background:rgba(239,68,68,0.15);color:#f87171;
    border:1px solid rgba(239,68,68,0.3);}
.prog-bg{background:rgba(255,255,255,0.1);border-radius:999px;height:8px;overflow:hidden;margin:0.4rem 0;}
.prog-fill{height:100%;border-radius:999px;}
div[data-testid="stButton"] button{font-weight:600!important;border-radius:10px!important;
    font-size:0.88rem!important;transition:all 0.2s!important;}
div[data-testid="stButton"] button[kind="primary"]{
    background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
</style>
""", unsafe_allow_html=True)

show_navbar("Dashboard")

user         = st.session_state.user
email        = st.session_state.email
db_user      = get_user(email)
name         = db_user.get("name", "").strip() or user.get("name", "Student")
resume_score = db_user.get("resume_score", 0)
skills       = db_user.get("skills", [])
missing      = db_user.get("missing_skills", [])
target_role  = db_user.get("target_role", "Not set")
total        = len(skills) + len(missing)
readiness    = int(len(skills) / total * 100) if total else 0

# ── Welcome banner ────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5 55%,#0ea5e9);
            border-radius:20px;padding:1.8rem 2.2rem;color:#fff;
            position:relative;overflow:hidden;margin-bottom:3rem;">
  <div style="position:absolute;top:-40%;right:-5%;width:260px;height:260px;
              background:rgba(255,255,255,0.05);border-radius:50%;"></div>
  <div style="position:relative;z-index:1;">
    <div style="font-size:0.85rem;opacity:0.7;margin-bottom:0.2rem;">👋 Welcome back,</div>
    <h1 style="margin:0 0 0.4rem;font-size:1.85rem;font-weight:800;">{name}</h1>
    <div style="font-size:0.9rem;opacity:0.8;">
      🎯 Target Role: <strong>{target_role}</strong> &nbsp;·&nbsp; 📈 Readiness: <strong>{readiness}%</strong>
    </div>
    <div style="margin-top:0.9rem;background:rgba(255,255,255,0.15);border-radius:999px;height:6px;width:260px;overflow:hidden;">
      <div style="width:{readiness}%;height:100%;background:rgba(255,255,255,0.9);border-radius:999px;"></div>
    </div>
  </div>
  <div style="position:absolute;top:1rem;right:1.8rem;font-size:3.2rem;opacity:0.2;">🎓</div>
</div>
""", unsafe_allow_html=True)

# ── Stat cards ────────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4, gap="large")
for col, icon, val, lbl, color in [
    (s1, "📄", f"{resume_score}%", "Resume Score",   "#7c3aed"),
    (s2, "✅", str(len(skills)),   "Skills Found",   "#059669"),
    (s3, "❌", str(len(missing)),  "Skills Missing", "#dc2626"),
    (s4, "📈", f"{readiness}%",   "Readiness",      "#0ea5e9"),
]:
    with col:
        st.markdown(
            f'<div class="stat-card" style="margin-bottom:3rem;"><div class="sc-icon">{icon}</div>'
            f'<div class="sc-val" style="color:{color};">{val}</div>'
            f'<div class="sc-lbl">{lbl}</div></div>',
            unsafe_allow_html=True
        )

# ── What would you like to do ─────────────────────────────────────────────────
st.markdown("### 🚀 What would you like to do?")

features = [
    ("📄", "Resume Scorer",      "Upload your resume and get an ATS-style score with improvement tips.", "Score Resume →",   "pages/4_Resume_Score.py", "Most Popular"),
    ("🧠", "Skill Gap Analyzer", "Compare your skills against top job roles and find what's missing.",   "Analyze Gap →",    "pages/5_Skill_Gap.py",   "Core Feature"),
    ("🛤️", "Learning Roadmap",   "Get a Beginner → Advanced step-by-step plan for every missing skill.","View Roadmap →",   "pages/6_Roadmap.py",     "Personalized"),
    ("📊", "Progress Analytics", "Visualize your skill growth and readiness with interactive charts.",   "View Analytics →", "pages/7_Analytics.py",   "Track Growth"),
]

cards_html = "".join(
    f'<div class="feat-card"><div class="fci">{ic}</div>'
    f'<div class="fct">{ti}</div><div class="fcd">{de}</div>'
    f'<div class="fcb">{ba}</div></div>'
    for ic, ti, de, _, __, ba in features
)

st.markdown(f"""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:20px;padding:1.2rem;margin-bottom:3rem;
            display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
  {cards_html}
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="large")
for col, (_, __, ___, cta, path, ____) in zip([c1, c2, c3, c4], features):
    with col:
        if st.button(cta, key=f"fc_{cta}", use_container_width=True, type="primary"):
            st.switch_page(path)

# ── Your Skills + Missing ─────────────────────────────────────────────────────
st.markdown("### 📊 Your Progress")
st.markdown("<br><br>", unsafe_allow_html=True)

skills_html  = "".join(f'<span class="chip-g">✅ {s}</span>' for s in skills) if skills \
               else '<span style="color:rgba(255,255,255,0.4);font-size:0.85rem;">No skills detected. Upload your resume.</span>'
missing_html = "".join(f'<span class="chip-r">❌ {s}</span>' for s in missing) if missing \
               else '<span style="color:rgba(255,255,255,0.4);font-size:0.85rem;">Run Skill Gap Analyzer to see missing skills.</span>'

st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;">
  <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);
              border-radius:16px;padding:1.2rem 1.4rem;">
    <div style="font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.7rem;">✅ Your Skills</div>
    <div style="display:flex;flex-wrap:wrap;gap:0.3rem;">{skills_html}</div>
  </div>
  <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);
              border-radius:16px;padding:1.2rem 1.4rem;">
    <div style="font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.7rem;">⚠️ Skills to Learn</div>
    <div style="display:flex;flex-wrap:wrap;gap:0.3rem;">{missing_html}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Roadmap button centered ───────────────────────────────────────────────────
if missing:
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("🛤️ Get My Roadmap", key="d_roadmap", type="primary", use_container_width=True):
            st.switch_page("pages/6_Roadmap.py")
elif not skills:
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("Upload Resume →", key="d_upload", use_container_width=True):
            st.switch_page("pages/4_Resume_Score.py")

# ── ATS Score ─────────────────────────────────────────────────────────────────
if resume_score > 0:
    c   = "#059669" if resume_score >= 70 else "#d97706" if resume_score >= 40 else "#dc2626"
    lbl = "Excellent 🌟" if resume_score >= 70 else "Good 👍" if resume_score >= 40 else "Needs Work ⚠️"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.06);border-radius:16px;padding:1.3rem 1.5rem;
                border:1px solid rgba(255,255,255,0.1);box-shadow:0 2px 10px rgba(0,0,0,0.2);">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
        <span style="font-weight:700;color:#fff;">ATS Resume Score</span>
        <span style="font-size:1.1rem;font-weight:800;color:{c};">{resume_score}% — {lbl}</span>
      </div>
      <div class="prog-bg"><div class="prog-fill" style="width:{resume_score}%;background:{c};"></div></div>
    </div>
    """, unsafe_allow_html=True)
