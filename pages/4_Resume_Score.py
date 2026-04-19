import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, update_user
from utils.scorer import score_resume, score_resume_file
from components.navbar import show_navbar

st.set_page_config(page_title="Resume Score · SkillGap", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")
require_login()

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.block-container{padding:0!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
.skill-chip{display:inline-block;background:#ede9fe;color:#5b21b6;border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.78rem;font-weight:600;margin:0.15rem;}
.cat-header{font-size:0.82rem;font-weight:700;color:#6b7280;text-transform:uppercase;
    letter-spacing:0.05em;margin:0.6rem 0 0.3rem;}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Score")

st.markdown("## 📄 Resume Scorer")
st.markdown("Upload your resume (PDF or DOCX) or paste text to get an ATS score, extracted skills, and improvement tips.")
st.markdown("")

upload_tab, paste_tab = st.tabs(["📁 Upload PDF / DOCX", "📋 Paste Text"])
parsed_data  = None
resume_text  = ""
upload_mode  = False

with upload_tab:
    uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx"])
    if uploaded:
        with st.spinner("Parsing resume..."):
            try:
                score, parsed_data, suggestions = score_resume_file(uploaded, uploaded.name)
                resume_text = parsed_data["raw_text"]
                upload_mode = True
                st.success(f"✅ Resume parsed successfully! ({uploaded.name})")
            except Exception as e:
                st.error(f"❌ Failed to parse: {e}")

with paste_tab:
    pasted = st.text_area("Paste your resume text here", height=280,
                          placeholder="Paste your full resume content...")
    if pasted.strip():
        resume_text = pasted

# ── Results ───────────────────────────────────────────────────────────────────
if resume_text.strip() and not upload_mode:
    with st.spinner("Analyzing..."):
        score, skills, suggestions = score_resume(resume_text)
        update_user(st.session_state.email, {"resume_score": score, "skills": skills})
    parsed_data = None  # text mode — no structured data

if upload_mode and parsed_data:
    skills = parsed_data["skills"]
    update_user(st.session_state.email, {"resume_score": score, "skills": skills})

if resume_text.strip():
    st.markdown("---")
    color = "#059669" if score >= 70 else "#d97706" if score >= 40 else "#dc2626"
    label = "Excellent 🌟" if score >= 70 else "Good 👍" if score >= 40 else "Needs Work ⚠️"

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div style="background:{color};border-radius:20px;padding:2rem;text-align:center;color:white;">
            <div style="font-size:3.5rem;font-weight:900;">{score}%</div>
            <div style="font-size:1.1rem;font-weight:700;margin-top:0.4rem;">{label}</div>
            <div style="font-size:0.85rem;margin-top:0.5rem;opacity:0.85;">ATS Score</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        st.progress(score / 100)

        st.markdown("### 💡 Suggestions")
        for tip in suggestions:
            st.info(f"💡 {tip}")

    with col2:
        if parsed_data:
            # ── Contact Info ──────────────────────────────────────────────
            contact = parsed_data.get("contact", {})
            if any(contact.values()):
                st.markdown("### 👤 Contact Detected")
                c_cols = st.columns(3)
                fields = [("📧", "email"), ("📞", "phone"), ("💼", "linkedin"), ("🐙", "github")]
                for i, (icon, key) in enumerate(fields):
                    val = contact.get(key, "")
                    if val:
                        with c_cols[i % 3]:
                            st.markdown(f"**{icon}** {val}")
                st.markdown("")

            # ── Categorized Skills ────────────────────────────────────────
            categorized = parsed_data.get("categorized_skills", {})
            if categorized:
                st.markdown("### 🧠 Skills Detected by Category")
                for category, skill_list in categorized.items():
                    if skill_list:
                        st.markdown(f'<div class="cat-header">{category}</div>', unsafe_allow_html=True)
                        chips = "".join(f'<span class="skill-chip">{s.title()}</span>' for s in skill_list)
                        st.markdown(chips, unsafe_allow_html=True)
                st.markdown("")
            elif skills:
                st.markdown("### 🧠 Skills Detected")
                chips = "".join(f'<span class="skill-chip">{s.title()}</span>' for s in skills)
                st.markdown(chips, unsafe_allow_html=True)
                st.markdown("")

            # ── Education ─────────────────────────────────────────────────
            education = parsed_data.get("education", [])
            if education:
                st.markdown("### 🎓 Education")
                for edu in education:
                    deg  = edu.get("degree", "")
                    inst = edu.get("institution", "")
                    yr   = edu.get("year", "")
                    st.markdown(f"**{deg}** — {inst} {f'({yr})' if yr else ''}")

            # ── Experience ────────────────────────────────────────────────
            experience = parsed_data.get("experience", [])
            if experience:
                st.markdown("### 💼 Experience")
                for exp in experience[:3]:
                    title    = exp.get("title", "")
                    company  = exp.get("company", "")
                    duration = exp.get("duration", "")
                    st.markdown(f"**{title}** @ {company} {f'| {duration}' if duration else ''}")

            # ── Projects ──────────────────────────────────────────────────
            projects = parsed_data.get("projects", [])
            if projects:
                st.markdown("### 🛠️ Projects")
                for proj in projects[:3]:
                    title = proj.get("title", "")
                    tech  = proj.get("tech", [])
                    st.markdown(f"**{title}** {f'— {', '.join(tech)}' if tech else ''}")

        else:
            # Text mode — just show flat skills
            if skills:
                st.markdown("### 🧠 Skills Detected")
                cols = st.columns(3)
                for i, skill in enumerate(skills):
                    with cols[i % 3]:
                        st.success(f"✅ {skill.title()}")
            else:
                st.warning("No recognizable skills found. Make sure your resume lists technical skills clearly.")

        st.markdown("")
        total_skills = len(skills) if skills else 0
        st.info(f"💡 **{total_skills} skills** detected. Go to Skill Gap to see what's missing for your target role.")
        if st.button("🧠 Analyze Skill Gap →", type="primary"):
            st.switch_page("pages/5_Skill_Gap.py")

st.markdown("</div>", unsafe_allow_html=True)
