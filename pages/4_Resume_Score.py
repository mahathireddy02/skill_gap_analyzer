import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, update_user
from utils.scorer import score_resume_file
from utils.skill_analyzer import get_roles
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
div[data-testid="stButton"] button[kind="primary"]{
    background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
.skill-chip{display:inline-block;background:rgba(124,58,237,0.1);color:#7c3aed;
    border-radius:999px;padding:0.18rem 0.6rem;font-size:0.78rem;font-weight:600;margin:0.12rem;}
.tip-row{padding:0.45rem 0.8rem;border-left:3px solid #7c3aed;
    border-radius:0 8px 8px 0;background:rgba(124,58,237,0.05);
    margin-bottom:0.4rem;font-size:0.85rem;}
.bd-row{display:flex;justify-content:space-between;
    font-size:0.83rem;padding:0.25rem 0;}
.bd-score{font-weight:700;color:#7c3aed;}
.info-pill{background:rgba(124,58,237,0.06);border-radius:10px;
    padding:0.6rem 0.9rem;margin-bottom:0.5rem;font-size:0.84rem;}
.cta-box{border:2px dashed rgba(124,58,237,0.3);border-radius:14px;
    padding:1.2rem 1.5rem;text-align:center;margin-top:1.5rem;
    background:rgba(124,58,237,0.03);}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Score")

st.markdown("## 📄 Resume Scorer")
st.caption("Upload your resume to get an ATS score, extracted skills, and improvement tips.")
st.markdown("")

# ── Inputs ────────────────────────────────────────────────────────────────────
roles = get_roles()
i1, i2, i3 = st.columns([2, 2, 2])
with i1:
    role_option = st.selectbox("🎯 Target Role", ["-- Select --"] + roles)
with i2:
    manual_role = st.text_input("✏️ Or type your own role", placeholder="e.g. Hotel Manager...")
with i3:
    uploaded = st.file_uploader("📁 Upload Resume (PDF / DOCX)", type=["pdf", "docx"])

target_role = manual_role.strip() if manual_role.strip() else (
    role_option if role_option != "-- Select --" else ""
)

# ── Analyze on upload ─────────────────────────────────────────────────────────
if uploaded and target_role:
    # Only re-analyze if file or role changed
    file_key = f"{uploaded.name}_{uploaded.size}_{target_role}"
    if st.session_state.get("resume_file_key") != file_key:
        with st.spinner("Analyzing your resume..."):
            try:
                score, parsed_data, suggestions = score_resume_file(
                    uploaded, uploaded.name, target_role
                )
                skills = parsed_data.get("skills", [])
                update_user(st.session_state.email, {
                    "resume_score": score,
                    "skills":       skills,
                    "target_role":  target_role,
                })
                st.session_state["resume_result"] = {
                    "score":       score,
                    "parsed_data": parsed_data,
                    "suggestions": suggestions,
                    "skills":      skills,
                    "target_role": target_role,
                }
                st.session_state["resume_file_key"] = file_key
            except Exception as e:
                st.error(f"❌ Failed to parse resume: {e}")
                st.session_state.pop("resume_result", None)

elif uploaded and not target_role:
    st.warning("⚠️ Please select or enter a target role first.")

elif not uploaded:
    st.info("👆 Select a target role and upload your resume to get started.")
    st.session_state.pop("resume_result", None)
    st.session_state.pop("resume_file_key", None)

# ── Results ───────────────────────────────────────────────────────────────────
if "resume_result" in st.session_state:
    res         = st.session_state["resume_result"]
    score       = res["score"]
    parsed_data = res["parsed_data"]
    suggestions = res["suggestions"]
    skills      = res["skills"]
    target_role = res["target_role"]

    contact    = parsed_data.get("contact", {})
    education  = parsed_data.get("education", [])
    experience = parsed_data.get("experience", [])
    projects   = parsed_data.get("projects", [])
    breakdown  = parsed_data.get("score_breakdown", {})
    categorized = parsed_data.get("categorized_skills", {})

    color = "#059669" if score >= 70 else "#d97706" if score >= 40 else "#dc2626"
    label = "Excellent 🌟" if score >= 70 else "Good 👍" if score >= 40 else "Needs Work ⚠️"

    st.markdown("---")

    # ── Row 1: Score | Breakdown | Suggestions ────────────────────────────────
    c1, c2, c3 = st.columns([1, 1.2, 1.4])

    with c1:
        st.markdown(f"""
        <div style="background:{color};border-radius:16px;padding:1.8rem 1rem;
                    text-align:center;color:#fff;">
            <div style="font-size:3.8rem;font-weight:900;line-height:1;">{score}%</div>
            <div style="font-size:1rem;font-weight:700;margin-top:0.3rem;">{label}</div>
            <div style="font-size:0.78rem;opacity:0.8;margin-top:0.2rem;">
                ATS Score · {target_role}
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        st.progress(score / 100)
        st.markdown("")
        a, b = st.columns(2)
        a.metric("Skills",     len(skills))
        b.metric("Experience", len(experience))
        c_, d = st.columns(2)
        c_.metric("Education", len(education))
        d.metric("Projects",   len(projects))

    with c2:
        st.markdown("**📊 Score Breakdown**")
        items = [
            ("sections",     "Sections",          25),
            ("contact",      "Contact Info",       10),
            ("length",       "Content Length",     15),
            ("action_verbs", "Action Verbs",       15),
            ("quantified",   "Quantified Results", 15),
            ("keywords",     "Role Keywords",      10),
            ("formatting",   "Formatting",         10),
        ]
        for key, lbl, mx in items:
            val = breakdown.get(key, 0)
            pct = int(val / mx * 100) if mx else 0
            st.markdown(
                f'<div class="bd-row"><span>{lbl}</span>'
                f'<span class="bd-score">{val}/{mx}</span></div>',
                unsafe_allow_html=True)
            st.progress(pct / 100)

    with c3:
        st.markdown("**💡 How to Improve**")
        for tip in suggestions:
            clean = tip.lstrip("✅💡 ")
            icon  = "✅" if tip.startswith("✅") else "💡"
            st.markdown(f'<div class="tip-row">{icon} {clean}</div>',
                        unsafe_allow_html=True)
        st.markdown("")
        if st.button("🧠 Analyze Skill Gap →", type="primary", use_container_width=True):
            st.switch_page("pages/5_Skill_Gap.py")

    st.markdown("---")
    st.markdown("### 🔍 Extracted Resume Data")

    # Contact
    contact_vals = {k: v for k, v in contact.items() if v and k != "name"}
    if contact_vals:
        icons_map = {"email": "📧", "phone": "📞", "linkedin": "💼", "github": "🐙"}
        cc = st.columns(len(contact_vals))
        for i, (k, v) in enumerate(contact_vals.items()):
            with cc[i]:
                st.markdown(f"**{icons_map.get(k,'')} {k.title()}**  \n`{v}`")
        st.markdown("")

    # Skills by category
    if categorized:
        st.markdown("**🧠 Skills by Category**")
        for cat, skill_list in categorized.items():
            if skill_list:
                st.markdown(f"*{cat}*")
                chips = "".join(
                    f'<span class="skill-chip">{s.title()}</span>' for s in skill_list
                )
                st.markdown(chips, unsafe_allow_html=True)
        st.markdown("")

    # Education | Experience | Projects
    d1, d2, d3 = st.columns(3)

    with d1:
        if education:
            st.markdown("**🎓 Education**")
            for edu in education:
                yr = edu.get("year", "")
                st.markdown(f"""
                <div class="info-pill">
                    <strong>{edu.get('degree','')}</strong><br>
                    <span style="color:#6b7280;font-size:0.8rem;">
                        {edu.get('institution','')}{"  ·  " + yr if yr else ""}
                    </span>
                </div>""", unsafe_allow_html=True)

    with d2:
        if experience:
            st.markdown("**💼 Experience**")
            for exp in experience[:3]:
                resps = exp.get("responsibilities", [])
                dur   = exp.get("duration", "")
                resp_line = f'<br><span style="font-size:0.76rem;color:#9ca3af;">• {resps[0][:70]}</span>' if resps else ""
                st.markdown(f"""
                <div class="info-pill">
                    <strong>{exp.get('title','')}</strong><br>
                    <span style="color:#6b7280;font-size:0.8rem;">
                        {exp.get('company','')}{"  ·  " + dur if dur else ""}
                    </span>{resp_line}
                </div>""", unsafe_allow_html=True)

    with d3:
        if projects:
            st.markdown("**🛠️ Projects**")
            for proj in projects[:3]:
                tech = proj.get("tech", [])
                tech_line = f'<span style="color:#7c3aed;font-size:0.78rem;">{", ".join(tech[:4])}</span>' if tech else ""
                st.markdown(f"""
                <div class="info-pill">
                    <strong>{proj.get('title','')}</strong><br>
                    {tech_line}
                </div>""", unsafe_allow_html=True)

# ── Builder CTA ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-box">
    <div style="font-size:1.05rem;font-weight:800;margin-bottom:0.25rem;">
        📝 Don't have a resume?
    </div>
    <div style="font-size:0.85rem;color:#6b7280;margin-bottom:0.7rem;">
        Build a professional ATS-friendly resume with 4 templates in minutes.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("✨ Create Resume with Builder →", use_container_width=True):
    st.switch_page("pages/10_Resume_Builder.py")
