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
.block-container{padding:0!important;max-width:100%!important;}
.stat-card{background:#fff;border-radius:16px;padding:1.3rem 1rem;border:1px solid #f0f0f0;
    box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;transition:transform 0.2s,box-shadow 0.2s;}
.stat-card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,0.1);}
.sc-icon{font-size:1.8rem;margin-bottom:0.35rem;}
.sc-val{font-size:1.85rem;font-weight:800;line-height:1;}
.sc-lbl{font-size:0.8rem;color:#999;margin-top:0.2rem;}
.feat-card{background:#fff;border-radius:16px;padding:1.5rem;border:1px solid #f0f0f0;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);transition:all 0.22s ease;}
.feat-card:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(124,58,237,0.1);border-color:#c4b5fd;}
.fci{font-size:2.2rem;margin-bottom:0.6rem;}
.fct{font-size:0.97rem;font-weight:700;color:#1a1a2e;margin-bottom:0.3rem;}
.fcd{font-size:0.82rem;color:#777;line-height:1.5;}
.fcb{display:inline-block;background:#f3f0ff;color:#7c3aed;font-size:0.7rem;font-weight:600;
    padding:0.15rem 0.5rem;border-radius:999px;margin-top:0.6rem;}
.sec-title{font-size:1.1rem;font-weight:700;color:#1a1a2e;margin-bottom:0.8rem;}
.chip{display:inline-block;padding:0.25rem 0.7rem;border-radius:999px;font-size:0.79rem;font-weight:600;margin:0.15rem;}
.chip-g{background:#d1fae5;color:#065f46;}
.chip-r{background:#fee2e2;color:#991b1b;}
.prog-bg{background:#f0f0f0;border-radius:999px;height:8px;overflow:hidden;margin:0.4rem 0;}
.prog-fill{height:100%;border-radius:999px;}
div[data-testid="stButton"] button{font-weight:600!important;border-radius:10px!important;font-size:0.88rem!important;transition:all 0.2s!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
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

st.markdown(f"""
<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5 55%,#0ea5e9);
            border-radius:20px;padding:1.8rem 2.2rem;color:#fff;
            margin-bottom:1.5rem;position:relative;overflow:hidden;">
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

s1, s2, s3, s4 = st.columns(4)
for col, icon, val, lbl, color in [
    (s1, "📄", f"{resume_score}%", "Resume Score",   "#7c3aed"),
    (s2, "✅", str(len(skills)),   "Skills Found",   "#059669"),
    (s3, "❌", str(len(missing)),  "Skills Missing", "#dc2626"),
    (s4, "📈", f"{readiness}%",   "Readiness",      "#0ea5e9"),
]:
    with col:
        st.markdown(f'<div class="stat-card"><div class="sc-icon">{icon}</div>'
                    f'<div class="sc-val" style="color:{color};">{val}</div>'
                    f'<div class="sc-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sec-title">🚀 What would you like to do?</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4)
for col, icon, title, desc, cta, path, badge in [
    (fc1,"📄","Resume Scorer",     "Upload your resume and get an ATS-style score with improvement tips.", "Score Resume →",  "pages/4_Resume_Score.py","Most Popular"),
    (fc2,"🧠","Skill Gap Analyzer","Compare your skills against top job roles and find what's missing.",   "Analyze Gap →",   "pages/5_Skill_Gap.py",  "Core Feature"),
    (fc3,"🛤️","Learning Roadmap",  "Get a Beginner → Advanced step-by-step plan for every missing skill.","View Roadmap →",  "pages/6_Roadmap.py",    "Personalized"),
    (fc4,"📊","Progress Analytics","Visualize your skill growth and readiness with interactive charts.",   "View Analytics →","pages/7_Analytics.py",  "Track Growth"),
]:
    with col:
        st.markdown(f'<div class="feat-card"><div class="fci">{icon}</div>'
                    f'<div class="fct">{title}</div><div class="fcd">{desc}</div>'
                    f'<div class="fcb">{badge}</div></div>', unsafe_allow_html=True)
        if st.button(cta, key=f"fc_{title}", use_container_width=True, type="primary"):
            st.switch_page(path)

st.markdown("<br>", unsafe_allow_html=True)
ca, cb = st.columns(2)
with ca:
    st.markdown('<div class="sec-title">✅ Your Skills</div>', unsafe_allow_html=True)
    if skills:
        st.markdown("".join(f'<span class="chip chip-g">✅ {s}</span>' for s in skills), unsafe_allow_html=True)
    else:
        st.info("📄 Upload your resume to detect your skills automatically.")
        if st.button("Upload Resume →", key="d_upload"):
            st.switch_page("pages/4_Resume_Score.py")

with cb:
    st.markdown('<div class="sec-title">⚠️ Skills to Learn</div>', unsafe_allow_html=True)
    if missing:
        st.markdown("".join(f'<span class="chip chip-r">❌ {s}</span>' for s in missing), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛤️ Get My Roadmap", key="d_roadmap", type="primary"):
            st.switch_page("pages/6_Roadmap.py")
    else:
        st.info("🧠 Run Skill Gap Analyzer to discover what skills you need.")
        if st.button("Analyze Skill Gap →", key="d_gap"):
            st.switch_page("pages/5_Skill_Gap.py")

if resume_score > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    c = "#059669" if resume_score >= 70 else "#d97706" if resume_score >= 40 else "#dc2626"
    lbl = "Excellent 🌟" if resume_score >= 70 else "Good 👍" if resume_score >= 40 else "Needs Work ⚠️"
    st.markdown(f"""
    <div style="background:#fff;border-radius:16px;padding:1.3rem 1.5rem;border:1px solid #f0f0f0;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
        <span style="font-weight:700;color:#1a1a2e;">ATS Resume Score</span>
        <span style="font-size:1.1rem;font-weight:800;color:{c};">{resume_score}% — {lbl}</span>
      </div>
      <div class="prog-bg"><div class="prog-fill" style="width:{resume_score}%;background:{c};"></div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
