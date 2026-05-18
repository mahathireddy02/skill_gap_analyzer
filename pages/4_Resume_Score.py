import streamlit as st
import sys, os
import html
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
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
.history-card{border:1px solid rgba(124,58,237,0.2);border-radius:14px;
    padding:0.9rem 1rem;background:rgba(124,58,237,0.04);margin:0.75rem 0;}
.history-row{display:grid;grid-template-columns:1.2fr 1.2fr 0.8fr 0.8fr 0.8fr;
    gap:0.7rem;align-items:center;padding:0.5rem 0;border-bottom:1px solid rgba(148,163,184,0.22);
    font-size:0.84rem;}
.history-row:last-child{border-bottom:none;}
.history-head{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;
    color:#6b7280;font-weight:800;}
.history-score{font-weight:900;color:#7c3aed;}
.history-delta{font-weight:900;}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Score")

st.markdown("## 📄 Resume Scorer")
st.caption("Upload your resume to get an ATS score, extracted skills, and improvement tips.")
st.markdown("")

# ── Target role: fixed from signup, change only via Profile ────────────────
db_user     = get_user(st.session_state.email)
target_role = db_user.get("target_role", "").strip()

if not target_role:
    st.warning("⚠️ No target role set. Please update it in your Profile.")
    if st.button("👤 Go to Profile", type="primary"):
        st.switch_page("pages/8_Profile.py")
    st.stop()

st.markdown(
    f'<div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);'
    f'border-radius:10px;padding:0.5rem 1rem;font-size:0.9rem;margin-bottom:1rem;">'
    f'🎯 Scoring against: <strong>{target_role}</strong> '
    f'<span style="font-size:0.75rem;opacity:0.5;">(✏️ change in Profile)</span></div>',
    unsafe_allow_html=True,
)

# ── File uploader ─────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "📁 Upload Resume",
    help="Accepts PDF, DOCX, TXT, images, and other resume file formats.",
)
st.caption("Accepted formats: PDF, DOCX, TXT, MD, CSV, TSV, RTF, HTML, ODT, JPG, PNG, WEBP, BMP, TIFF.")


def render_score_history(score_history):
    if not score_history:
        return
    st.markdown("### 📈 Resume Score History")
    recent_history = list(reversed(score_history[-5:]))
    rows = [
        '<div class="history-row history-head">'
        '<div>Date</div><div>Resume</div><div>Score</div><div>Change</div><div>Skills</div></div>'
    ]
    for item in recent_history:
        delta = item.get("delta", 0)
        delta_text = f"+{delta}%" if delta > 0 else f"{delta}%" if delta < 0 else "-"
        delta_color = "#059669" if delta > 0 else "#dc2626" if delta < 0 else "#6b7280"
        filename = item.get("filename", "Resume")
        if len(filename) > 28:
            filename = filename[:25] + "..."
        filename = html.escape(filename)
        rows.append(
            f'<div class="history-row">'
            f'<div>{item.get("date", "")}</div>'
            f'<div>{filename}</div>'
            f'<div class="history-score">{item.get("score", 0)}%</div>'
            f'<div class="history-delta" style="color:{delta_color};">{delta_text}</div>'
            f'<div>{item.get("skills_count", 0)}</div>'
            f'</div>'
        )
    st.markdown(
        '<div class="history-card">' + "".join(rows) + '</div>',
        unsafe_allow_html=True,
    )


# ── Analyze on upload ─────────────────────────────────────────────────────────
if uploaded and target_role:
    file_key = f"{uploaded.name}_{uploaded.size}_{target_role}"
    if st.session_state.get("resume_file_key") != file_key:
        with st.spinner("Analyzing your resume..."):
            try:
                score, parsed_data, suggestions = score_resume_file(
                    uploaded, uploaded.name, target_role
                )
                skills = parsed_data.get("skills", [])
                latest_user = get_user(st.session_state.email) or {}
                score_history = latest_user.get("resume_score_history", [])
                previous_score = score_history[-1]["score"] if score_history else latest_user.get("resume_score", 0)
                history_entry = {
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "filename": uploaded.name,
                    "file_type": uploaded.name.rsplit(".", 1)[-1].upper() if "." in uploaded.name else "FILE",
                    "target_role": target_role,
                    "score": score,
                    "delta": score - previous_score if previous_score else 0,
                    "skills_count": len(skills),
                }
                score_history = (score_history + [history_entry])[-10:]
                update_user(st.session_state.email, {
                    "resume_score":         score,
                    "resume_score_history": score_history,
                    "skills":               skills,
                    "target_role":          target_role,
                })
                st.session_state.user.update({
                    "resume_score": score,
                    "resume_score_history": score_history,
                    "skills": skills,
                    "target_role": target_role,
                })
                st.session_state["resume_result"] = {
                    "score":       score,
                    "parsed_data": parsed_data,
                    "suggestions": suggestions,
                    "skills":      skills,
                    "target_role": target_role,
                    "score_history": score_history,
                }
                st.session_state["resume_file_key"] = file_key
            except Exception as e:
                st.error(f"❌ Failed to parse resume: {e}")
                st.session_state.pop("resume_result", None)

elif uploaded and not target_role:
    st.warning("⚠️ Please enter a target role first.")

elif not uploaded:
    st.info("👆 Upload your resume to get started.")
    st.session_state.pop("resume_result", None)
    st.session_state.pop("resume_file_key", None)
    saved_history = db_user.get("resume_score_history", [])
    if saved_history:
        st.markdown("---")
        render_score_history(saved_history)

# ── Results ───────────────────────────────────────────────────────────────────
if "resume_result" in st.session_state:
    res         = st.session_state["resume_result"]
    score       = res["score"]
    parsed_data = res["parsed_data"]
    suggestions = res["suggestions"]
    skills      = res["skills"]
    target_role = res["target_role"]
    score_history = res.get("score_history") or (get_user(st.session_state.email) or {}).get("resume_score_history", [])

    contact     = parsed_data.get("contact", {})
    education   = parsed_data.get("education", [])
    experience  = parsed_data.get("experience", [])
    projects    = parsed_data.get("projects", [])
    breakdown   = parsed_data.get("score_breakdown", {})
    categorized = parsed_data.get("categorized_skills", {})

    color = "#059669" if score >= 70 else "#d97706" if score >= 40 else "#dc2626"
    label = "Excellent 🌟" if score >= 70 else "Good 👍" if score >= 40 else "Needs Work ⚠️"

    st.markdown("---")

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

        if score_history:
            latest = score_history[-1]
            delta = latest.get("delta", 0)
            delta_color = "#059669" if delta > 0 else "#dc2626" if delta < 0 else "#6b7280"
            delta_label = f"+{delta}%" if delta > 0 else f"{delta}%" if delta < 0 else "No change"
            st.markdown(
                f'<div class="history-card">'
                f'<div style="font-size:0.78rem;color:#6b7280;font-weight:800;">Compared with previous upload</div>'
                f'<div style="font-size:1.15rem;font-weight:900;color:{delta_color};">{delta_label}</div>'
                f'<div style="font-size:0.78rem;color:#6b7280;">{latest.get("date", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown("**📊 Score Breakdown**")
        items = [
            ("sections",     "Sections",          20),
            ("contact",      "Contact Info",       10),
            ("length",       "Content Length",     10),
            ("action_verbs", "Action Verbs",       10),
            ("quantified",   "Quantified Results", 10),
            ("keywords",     "Role Keywords",      30),
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

    if score_history:
        st.markdown("---")
        render_score_history(score_history)

    st.markdown("---")
    st.markdown("### 🔍 Extracted Resume Data")

    contact_vals = {k: v for k, v in contact.items() if v and k != "name"}
    if contact_vals:
        icons_map = {"email": "📧", "phone": "📞", "linkedin": "💼", "github": "🐙"}
        cc = st.columns(len(contact_vals))
        for i, (k, v) in enumerate(contact_vals.items()):
            with cc[i]:
                st.markdown(f"**{icons_map.get(k,'')} {k.title()}**  \n`{v}`")
        st.markdown("")

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
                        {edu.get('institution','')}{" · " + yr if yr else ""}
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
                        {exp.get('company','')}{" · " + dur if dur else ""}
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
