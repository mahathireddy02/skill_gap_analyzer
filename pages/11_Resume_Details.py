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
h3 {
    border-bottom: 1px solid """ + border_color + """;
    padding-bottom: 8px;
    margin-top: 25px !important;
}
/* Align trash icon and buttons better with input fields */
div[data-testid="column"] {display: flex; flex-direction: column; justify-content: flex-end;}
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {align-items: flex-end !important;}
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

if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

meta = TEMPLATE_META.get(selected_template, {"icon": "📝"})

top_left, top_right = st.columns([3, 1])
with top_left:
    st.markdown("## 📝 Resume Details")
    st.caption("Fill in your information and generate a professional PDF resume.")
with top_right:
    if st.button("Change Template", use_container_width=True):
        st.switch_page("pages/10_Resume_Builder.py")

st.markdown(
    f'<div style="background:{info_bg};border:1px solid {info_border};'
    f'border-radius:10px;padding:0.5rem 1rem;font-size:0.88rem;margin:0.6rem 0 0.2rem;color:{text_color};">'
    f'{meta["icon"]} Using <strong style="color:#7c3aed;">{selected_template}</strong> template</div>',
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("### 👤 Personal Information")
c1, c2, c3 = st.columns(3)
with c1:
    name = st.text_input("Full Name *", value=db_user.get("name", ""))
    email = st.text_input("Email *", value=st.session_state.email)
with c2:
    phone = st.text_input("Phone", placeholder="+91 9876543210")
    linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
with c3:
    github = st.text_input("GitHub", placeholder="github.com/yourname")
    location = st.text_input("Location", placeholder="City, Country")

summary = st.text_area(
    "Professional Summary",
    height=70,
    placeholder="Results-driven engineer with 2+ years building scalable apps...",
)

st.markdown("---")

st.markdown("### 🧠 Skills")
st.caption("Add skills by category. Click + to add more rows.")

skills_data = {}
for i in range(st.session_state.num_skills):
    s1, s2, s3, s4 = st.columns([1.5, 3.5, 1.2, 0.5])
    with s1:
        cat = st.text_input("Category", key=f"scat_{i}", placeholder="e.g. Languages")
    with s2:
        val = st.text_input("Skills (comma-separated)", key=f"sval_{i}", placeholder="e.g. Python, Java, SQL")
    with s3:
        level = st.selectbox("Level", ["Basic", "Intermediate", "Expert"], key=f"slvl_{i}")
    with s4:
        if st.button("🗑️", key=f"sdel_{i}", use_container_width=True):
            st.session_state.num_skills = max(1, st.session_state.num_skills - 1)
            st.rerun()
    if cat.strip() and val.strip():
        skills_data[cat] = {"skills": [s.strip() for s in val.split(",") if s.strip()], "level": level}

if st.button("➕ Add Skill Category"):
    st.session_state.num_skills += 1
    st.rerun()

st.markdown("---")

st.markdown("### 🎓 Education")
num_edu = st.number_input("Number of entries", 1, 4, 1, key="num_edu")
education = []
for i in range(int(num_edu)):
    st.markdown(f"**Entry {i + 1}**")
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        deg = st.text_input("Degree *", key=f"deg_{i}", placeholder="B.Tech CS")
    with e2:
        inst = st.text_input("Institution *", key=f"inst_{i}", placeholder="ABC Univ")
    with e3:
        yr = st.text_input("Year", key=f"yr_{i}", placeholder="2020-2024")
    with e4:
        gpa = st.text_input("GPA", key=f"gpa_{i}", placeholder="8.5")
    if deg.strip():
        education.append({"degree": deg, "institution": inst, "year": yr, "gpa": gpa})

st.markdown("---")

st.markdown("### 💼 Work Experience")
num_exp = st.number_input("Number of jobs (0 if fresher)", 0, 5, 0, key="num_exp")
experience = []
for i in range(int(num_exp)):
    st.markdown(f"**Job {i + 1}**")
    x1, x2, x3 = st.columns(3)
    with x1:
        title = st.text_input("Title *", key=f"jtitle_{i}", placeholder="Software Engineer")
    with x2:
        comp = st.text_input("Company *", key=f"jcomp_{i}", placeholder="Google")
    with x3:
        dur = st.text_input("Duration", key=f"jdur_{i}", placeholder="Jun 2022 - Present")
    resp = st.text_area(
        "Responsibilities (one per line)",
        key=f"jresp_{i}",
        height=70,
        placeholder="• Developed REST APIs\n• Reduced latency by 30%",
    )
    if title.strip():
        experience.append({
            "title": title,
            "company": comp,
            "duration": dur,
            "responsibilities": [r.lstrip("•-– ").strip() for r in resp.splitlines() if r.strip()],
        })

st.markdown("---")

st.markdown("### 🛠️ Projects")
num_proj = st.number_input("Number of projects", 1, 6, 2, key="num_proj")
projects = []
for i in range(int(num_proj)):
    st.markdown(f"**Project {i + 1}**")
    p1, p2 = st.columns(2)
    with p1:
        ptitle = st.text_input("Title *", key=f"ptitle_{i}", placeholder="Skill Gap Analyzer")
    with p2:
        plink = st.text_input("Link", key=f"plink_{i}", placeholder="github.com/you/project")
    ptech = st.text_input("Tech", key=f"ptech_{i}", placeholder="Python, React, Docker")
    pdesc = st.text_area("Description", key=f"pdesc_{i}", height=60, placeholder="• Built a web app\n• Achieved 95% accuracy")
    if ptitle.strip():
        projects.append({
            "title": ptitle,
            "description": pdesc,
            "tech": [t.strip() for t in ptech.split(",") if t.strip()],
            "link": plink,
        })

st.markdown("---")

st.markdown("### 🏆 Certifications (Optional)")
certs_raw = st.text_area("One per line", height=70, placeholder="AWS Certified Solutions Architect - Amazon (2023)")
certifications = [line.strip() for line in certs_raw.splitlines() if line.strip()]

st.markdown("---")

resume_data = {
    "name": name,
    "email": email,
    "phone": phone,
    "linkedin": linkedin,
    "github": github,
    "location": location,
    "summary": summary,
    "skills": skills_data,
    "experience": experience,
    "education": education,
    "projects": projects,
    "certifications": certifications,
}

b1, b2 = st.columns(2)
with b1:
    preview_clicked = st.button("👁️ Preview All Templates", use_container_width=True)
with b2:
    generate_clicked = st.button("📄 Generate & Download Resume", type="primary", use_container_width=True)

if preview_clicked or generate_clicked:
    errors = validate_resume_data(resume_data)
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        if preview_clicked:
            st.markdown("---")
            st.markdown("### 👁️ Preview - All 4 Templates")
            st.caption("Click any tab to preview. Use the download button below each preview.")
            templates_list = ["Classic", "Modern", "Minimal", "Creative"]
            pdfs = {}
            with st.spinner("Generating all 4 previews..."):
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
                    st.markdown("")
                    st.download_button(
                        f"⬇️ Download {tmpl} Template",
                        data=pdfs[tmpl],
                        file_name=f"{name.replace(' ', '_')}_{tmpl}_resume.pdf",
                        mime="application/pdf",
                        key=f"dl_{tmpl}",
                        use_container_width=True,
                    )

        if generate_clicked:
            with st.spinner(f"Building {selected_template} template..."):
                pdf = build_resume_pdf(resume_data, template=selected_template)
            st.success(f"✅ {selected_template} resume ready!")
            st.download_button(
                f"⬇️ Download {selected_template} Resume",
                data=pdf,
                file_name=f"{name.replace(' ', '_')}_resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
