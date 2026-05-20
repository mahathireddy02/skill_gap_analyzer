import base64
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.navbar import show_navbar
from utils.auth import get_user, require_login
from utils.resume_builder import build_resume_pdf, validate_resume_data


st.set_page_config(page_title="Resume Details", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
require_login()

db_user = get_user(st.session_state.email)
theme = db_user.get("theme", "dark")

bg_color = "#ffffff" if theme == "light" else "#0a0e17"
text_color = "#000000" if theme == "light" else "#ffffff"
border_color = "#e5e7eb" if theme == "light" else "rgba(255,255,255,0.1)"
secondary_text = "#4b5563" if theme == "light" else "rgba(255,255,255,0.5)"
info_bg = "#f9fafb" if theme == "light" else "rgba(124,58,237,0.08)"
info_border = "#e5e7eb" if theme == "light" else "rgba(124,58,237,0.25)"

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body,.stApp{margin:0!important;padding:0!important;background:""" + bg_color + """!important;color:""" + text_color + """!important;}
.block-container{padding:1.5rem 2.5rem 2rem!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
div[data-testid="stButton"] button[kind="secondary"]{
    background-color: """ + bg_color + """!important;
    color: """ + text_color + """!important;
    border: 1px solid """ + border_color + """!important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background-color: """ + bg_color + """!important;
    color: """ + text_color + """!important;
    border: 1px solid """ + border_color + """!important;
}
div[data-testid="stTextInput"] input:hover,
div[data-testid="stTextArea"] textarea:hover,
div[data-testid="stNumberInput"] input:hover,
div[data-testid="stSelectbox"] > div > div:hover {
    background-color: """ + (info_bg if theme == "light" else "rgba(255,255,255,0.05)") + """!important;
}
div[data-testid="stExpander"] {
    background-color: """ + bg_color + """!important;
    border: 1px solid """ + border_color + """!important;
    border-radius: 12px !important;
}
div[data-testid="stAlert"] {
    background-color: """ + bg_color + """!important;
    border: 1px solid """ + border_color + """!important;
    color: """ + text_color + """!important;
}
h1, h2, h3, h4, p, label, .stMarkdown {color: """ + text_color + """!important;}
small, .stCaptionContainer p {color: """ + secondary_text + """!important;}
hr {border-color: """ + border_color + """!important; opacity: 0.6;}
.resume-shell{max-width:980px;margin:0 auto;padding:0 1rem 1.5rem;}
.template-pill{background:""" + info_bg + """;border:1px solid """ + info_border + """;border-radius:10px;padding:0.55rem 0.9rem;font-size:0.88rem;margin:0.65rem 0 0.35rem;color:""" + text_color + """;}
.wizard-wrap{display:flex;align-items:center;gap:0.65rem;margin:0.9rem 0 0.45rem;}
.wizard-step{flex:1;height:6px;border-radius:999px;background:rgba(148,163,184,0.22);}
.wizard-done{background:linear-gradient(90deg,#7c3aed,#4f46e5);}
.wizard-active{background:linear-gradient(90deg,#a78bfa,#818cf8);}
.wizard-label{font-size:0.8rem;color:""" + secondary_text + """;font-weight:800;white-space:nowrap;}
.wizard-names{display:grid;grid-template-columns:repeat(5,1fr);gap:0.55rem;margin-bottom:1.1rem;color:""" + secondary_text + """;font-size:0.74rem;font-weight:800;text-align:center;}
.wizard-current{color:#7c3aed;}
.step-card{border:1px solid """ + border_color + """;border-radius:14px;background:""" + (info_bg if theme == "light" else "rgba(255,255,255,0.035)") + """;padding:1.2rem;margin-bottom:1rem;}
.step-title{font-size:1.05rem;font-weight:900;margin-bottom:0.15rem;color:""" + text_color + """;}
.step-note{font-size:0.84rem;color:""" + secondary_text + """;margin-bottom:0.9rem;}
.summary-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1rem;}
.summary-pill{border:1px solid """ + border_color + """;border-radius:10px;padding:0.65rem;background:""" + info_bg + """;}
.summary-label{font-size:0.7rem;font-weight:900;color:""" + secondary_text + """;text-transform:uppercase;}
.summary-value{font-size:0.92rem;font-weight:800;margin-top:0.2rem;color:""" + text_color + """;}
div[data-testid="column"] {display:flex;flex-direction:column;justify-content:flex-end;}
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {align-items:flex-end!important;}
@media (max-width: 760px){
    .wizard-names{display:none;}
    .summary-strip{grid-template-columns:1fr 1fr;}
}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

TEMPLATE_META = {
    "Classic": {"icon": "📄"},
    "Modern": {"icon": "✨"},
    "Minimal": {"icon": "🎯"},
    "Creative": {"icon": "🎨"},
}

selected_template = st.session_state.get("selected_template")
if not selected_template:
    st.warning("Please choose a resume template first.")
    if st.button("Choose Template", type="primary"):
        st.switch_page("pages/10_Resume_Builder.py")
    st.stop()

st.session_state.setdefault("rb_step", 1)
st.session_state.setdefault("rb_num_skills", 3)
st.session_state.setdefault("rb_num_edu", 1)
st.session_state.setdefault("rb_num_exp", 0)
st.session_state.setdefault("rb_num_proj", 2)
st.session_state.setdefault("rb_name", db_user.get("name", ""))
st.session_state.setdefault("rb_email", st.session_state.email)

def collect_skills():
    skills_data = {}
    for i in range(int(st.session_state.rb_num_skills)):
        cat = st.session_state.get(f"rb_scat_{i}", "").strip()
        val = st.session_state.get(f"rb_sval_{i}", "").strip()
        level = st.session_state.get(f"rb_slvl_{i}", "Intermediate")
        if cat and val:
            skills_data[cat] = {
                "skills": [s.strip() for s in val.split(",") if s.strip()],
                "level": level,
            }
    return skills_data


def collect_education():
    education = []
    for i in range(int(st.session_state.rb_num_edu)):
        degree = st.session_state.get(f"rb_deg_{i}", "").strip()
        if degree:
            education.append({
                "degree": degree,
                "institution": st.session_state.get(f"rb_inst_{i}", "").strip(),
                "year": st.session_state.get(f"rb_yr_{i}", "").strip(),
                "gpa": st.session_state.get(f"rb_gpa_{i}", "").strip(),
            })
    return education


def collect_experience():
    experience = []
    for i in range(int(st.session_state.rb_num_exp)):
        title = st.session_state.get(f"rb_jtitle_{i}", "").strip()
        if title:
            resp = st.session_state.get(f"rb_jresp_{i}", "")
            experience.append({
                "title": title,
                "company": st.session_state.get(f"rb_jcomp_{i}", "").strip(),
                "duration": st.session_state.get(f"rb_jdur_{i}", "").strip(),
                "responsibilities": [r.lstrip("•-– ").strip() for r in resp.splitlines() if r.strip()],
            })
    return experience


def collect_projects():
    projects = []
    for i in range(int(st.session_state.rb_num_proj)):
        title = st.session_state.get(f"rb_ptitle_{i}", "").strip()
        if title:
            tech = st.session_state.get(f"rb_ptech_{i}", "")
            projects.append({
                "title": title,
                "description": st.session_state.get(f"rb_pdesc_{i}", "").strip(),
                "tech": [t.strip() for t in tech.split(",") if t.strip()],
                "link": st.session_state.get(f"rb_plink_{i}", "").strip(),
            })
    return projects


def build_current_resume_data():
    certs_raw = st.session_state.get("rb_certs_raw", "")
    return {
        "name": st.session_state.get("rb_name", "").strip(),
        "email": st.session_state.get("rb_email", "").strip(),
        "phone": st.session_state.get("rb_phone", "").strip(),
        "linkedin": st.session_state.get("rb_linkedin", "").strip(),
        "github": st.session_state.get("rb_github", "").strip(),
        "location": st.session_state.get("rb_location", "").strip(),
        "summary": st.session_state.get("rb_summary", "").strip(),
        "skills": collect_skills(),
        "experience": collect_experience(),
        "education": collect_education(),
        "projects": collect_projects(),
        "certifications": [line.strip() for line in certs_raw.splitlines() if line.strip()],
    }


def set_step(step):
    st.session_state.rb_step = step
    st.rerun()


def render_progress(step):
    total_steps = 5
    labels = ["Contact", "Skills", "Education", "Experience", "Finish"]
    bars = []
    for i in range(1, total_steps + 1):
        state = "wizard-done" if step > i else ("wizard-active" if step == i else "")
        bars.append(f'<div class="wizard-step {state}"></div>')
    names = "".join(
        f'<div class="{"wizard-current" if idx == step else ""}">{label}</div>'
        for idx, label in enumerate(labels, start=1)
    )
    st.markdown(f"""
    <div class="wizard-wrap">
        {''.join(bars)}
        <span class="wizard-label">Step {step} of {total_steps}</span>
    </div>
    <div class="wizard-names">{names}</div>
    """, unsafe_allow_html=True)


def render_summary(resume_data):
    st.markdown(f"""
    <div class="summary-strip">
        <div class="summary-pill"><div class="summary-label">Template</div><div class="summary-value">{selected_template}</div></div>
        <div class="summary-pill"><div class="summary-label">Skills</div><div class="summary-value">{len(resume_data["skills"])}</div></div>
        <div class="summary-pill"><div class="summary-label">Education</div><div class="summary-value">{len(resume_data["education"])}</div></div>
        <div class="summary-pill"><div class="summary-label">Projects</div><div class="summary-value">{len(resume_data["projects"])}</div></div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="resume-shell">', unsafe_allow_html=True)

meta = TEMPLATE_META.get(selected_template, {"icon": "📝"})
top_left, top_right = st.columns([3, 1])
with top_left:
    st.markdown("## Resume Details")
    st.caption("Build your resume one clean step at a time.")
with top_right:
    if st.button("Change Template", use_container_width=True):
        st.switch_page("pages/10_Resume_Builder.py")

st.markdown(
    f'<div class="template-pill">{meta["icon"]} Using <strong style="color:#7c3aed;">{selected_template}</strong> template</div>',
    unsafe_allow_html=True,
)

step = int(st.session_state.rb_step)
if step < 1 or step > 5:
    st.session_state.rb_step = 1
    step = 1
render_progress(step)

if step == 1:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Contact basics</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Start with only the details that belong at the top of the resume.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Full Name *", key="rb_name")
        st.text_input("Email *", key="rb_email")
        st.text_input("Phone", key="rb_phone", placeholder="+91 9876543210")
    with c2:
        st.text_input("Location", key="rb_location", placeholder="City, Country")
        st.text_input("LinkedIn", key="rb_linkedin", placeholder="linkedin.com/in/yourname")
        st.text_input("GitHub", key="rb_github", placeholder="github.com/yourname")
    st.text_area(
        "Professional Summary",
        key="rb_summary",
        height=120,
        placeholder="Results-driven engineer with 2+ years building scalable apps...",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Next: Skills", type="primary", use_container_width=True):
        data = build_current_resume_data()
        if not data["name"] or not data["email"]:
            st.error("Please enter your full name and email.")
        else:
            set_step(2)

elif step == 2:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Skills</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Group skills by category so the resume stays easy to scan.</div>', unsafe_allow_html=True)
    for i in range(int(st.session_state.rb_num_skills)):
        s1, s2, s3, s4 = st.columns([1.4, 3.3, 1.2, 0.55])
        with s1:
            st.text_input("Category", key=f"rb_scat_{i}", placeholder="Languages")
        with s2:
            st.text_input("Skills", key=f"rb_sval_{i}", placeholder="Python, Java, SQL")
        with s3:
            st.selectbox("Level", ["Basic", "Intermediate", "Expert"], key=f"rb_slvl_{i}")
        with s4:
            if st.button("Delete", key=f"rb_sdel_{i}", use_container_width=True):
                st.session_state.rb_num_skills = max(1, st.session_state.rb_num_skills - 1)
                st.rerun()
    if st.button("Add Skill Category"):
        st.session_state.rb_num_skills += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Back", use_container_width=True):
            set_step(1)
    with b2:
        if st.button("Next: Education", type="primary", use_container_width=True):
            set_step(3)

elif step == 3:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Education</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Add your strongest education entry first.</div>', unsafe_allow_html=True)
    st.session_state.rb_num_edu = st.number_input(
        "Number of education entries", 1, 4, int(st.session_state.rb_num_edu), key="rb_num_edu_input"
    )
    for i in range(int(st.session_state.rb_num_edu)):
        st.markdown(f"**Entry {i + 1}**")
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            st.text_input("Degree *", key=f"rb_deg_{i}", placeholder="B.Tech CS")
        with e2:
            st.text_input("Institution *", key=f"rb_inst_{i}", placeholder="ABC Univ")
        with e3:
            st.text_input("Year", key=f"rb_yr_{i}", placeholder="2020-2024")
        with e4:
            st.text_input("GPA", key=f"rb_gpa_{i}", placeholder="8.5")
    st.markdown('</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Back", use_container_width=True):
            set_step(2)
    with b2:
        if st.button("Next: Experience", type="primary", use_container_width=True):
            if not collect_education():
                st.error("Please add at least one education entry.")
            else:
                set_step(4)

elif step == 4:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Work experience</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Freshers can leave this at 0 and continue to projects.</div>', unsafe_allow_html=True)
    st.session_state.rb_num_exp = st.number_input(
        "Number of jobs", 0, 5, int(st.session_state.rb_num_exp), key="rb_num_exp_input"
    )
    for i in range(int(st.session_state.rb_num_exp)):
        st.markdown(f"**Job {i + 1}**")
        x1, x2, x3 = st.columns(3)
        with x1:
            st.text_input("Title *", key=f"rb_jtitle_{i}", placeholder="Software Engineer")
        with x2:
            st.text_input("Company *", key=f"rb_jcomp_{i}", placeholder="Google")
        with x3:
            st.text_input("Duration", key=f"rb_jdur_{i}", placeholder="Jun 2022 - Present")
        st.text_area(
            "Responsibilities (one per line)",
            key=f"rb_jresp_{i}",
            height=90,
            placeholder="Developed REST APIs\nReduced latency by 30%",
        )
    st.markdown('</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Back", use_container_width=True):
            set_step(3)
    with b2:
        if st.button("Next: Projects & Download", type="primary", use_container_width=True):
            set_step(5)

elif step == 5:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Projects are where your resume proves what you can build.</div>', unsafe_allow_html=True)
    st.session_state.rb_num_proj = st.number_input(
        "Number of projects", 1, 6, int(st.session_state.rb_num_proj), key="rb_num_proj_input"
    )
    for i in range(int(st.session_state.rb_num_proj)):
        st.markdown(f"**Project {i + 1}**")
        p1, p2 = st.columns(2)
        with p1:
            st.text_input("Title *", key=f"rb_ptitle_{i}", placeholder="Skill Gap Analyzer")
        with p2:
            st.text_input("Link", key=f"rb_plink_{i}", placeholder="github.com/you/project")
        st.text_input("Tech", key=f"rb_ptech_{i}", placeholder="Python, React, Docker")
        st.text_area("Description", key=f"rb_pdesc_{i}", height=80, placeholder="Built a web app\nAchieved 95% accuracy")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Certifications</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-note">Optional. Add one certification per line.</div>', unsafe_allow_html=True)
    st.text_area("Certifications", key="rb_certs_raw", height=90, placeholder="AWS Certified Solutions Architect - Amazon (2023)")
    st.markdown('</div>', unsafe_allow_html=True)

    resume_data = build_current_resume_data()
    render_summary(resume_data)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Back", use_container_width=True):
            set_step(4)
    with b2:
        preview_clicked = st.button("Preview Templates", use_container_width=True)
    with b3:
        generate_clicked = st.button("Generate Resume", type="primary", use_container_width=True)

    if preview_clicked or generate_clicked:
        errors = validate_resume_data(resume_data)
        if errors:
            for error in errors:
                st.error(f"Error: {error}")
        else:
            if preview_clicked:
                st.markdown("---")
                st.markdown("### Preview - All Templates")
                templates_list = ["Classic", "Modern", "Minimal", "Creative"]
                pdfs = {}
                with st.spinner("Generating previews..."):
                    for tmpl in templates_list:
                        pdfs[tmpl] = build_resume_pdf(resume_data, template=tmpl)
                tabs = st.tabs([f"{TEMPLATE_META[t]['icon']} {t}" for t in templates_list])
                for tab, tmpl in zip(tabs, templates_list):
                    with tab:
                        pdf_b64 = base64.b64encode(pdfs[tmpl]).decode()
                        st.markdown(
                            f'<iframe src="data:application/pdf;base64,{pdf_b64}" '
                            f'width="100%" height="700px" '
                            f'style="border:1px solid rgba(124,58,237,0.3);border-radius:12px;">'
                            f'</iframe>',
                            unsafe_allow_html=True,
                        )
                        st.download_button(
                            f"Download {tmpl} Template",
                            data=pdfs[tmpl],
                            file_name=f"{resume_data['name'].replace(' ', '_')}_{tmpl}_resume.pdf",
                            mime="application/pdf",
                            key=f"dl_{tmpl}",
                            use_container_width=True,
                        )

            if generate_clicked:
                with st.spinner(f"Building {selected_template} template..."):
                    pdf = build_resume_pdf(resume_data, template=selected_template)
                st.success(f"{selected_template} resume ready!")
                st.download_button(
                    f"Download {selected_template} Resume",
                    data=pdf,
                    file_name=f"{resume_data['name'].replace(' ', '_')}_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

st.markdown('</div>', unsafe_allow_html=True)
