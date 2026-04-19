import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.resume_builder import build_resume_pdf, validate_resume_data
from components.navbar import show_navbar

st.set_page_config(page_title="Resume Builder · SkillGap", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
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
.section-card{background:#f8f7ff;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem;border:1px solid #e5e7eb;}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

st.markdown("## 📝 Resume Builder")
st.markdown("Fill in your details and download a clean, ATS-friendly PDF resume.")
st.markdown("")

db_user = get_user(st.session_state.email)

# ── Section 1: Personal Info ──────────────────────────────────────────────────
st.markdown("### 👤 Personal Information")
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        name     = st.text_input("Full Name *", value=db_user.get("name", ""))
        email    = st.text_input("Email *",     value=db_user.get("email", st.session_state.email))
    with c2:
        phone    = st.text_input("Phone Number", placeholder="+91 9876543210")
        linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/yourname")
    with c3:
        github   = st.text_input("GitHub URL",  placeholder="github.com/yourname")
        location = st.text_input("Location",    placeholder="City, Country")

summary = st.text_area("Professional Summary (2–3 lines)", height=80,
    placeholder="Results-driven software engineer with 2+ years of experience building scalable web applications...")

st.markdown("---")

# ── Section 2: Skills ─────────────────────────────────────────────────────────
st.markdown("### 🧠 Skills")
st.markdown("*Enter skills per category (comma-separated). Leave blank to skip.*")

detected_skills = db_user.get("skills", [])
if detected_skills:
    st.info(f"💡 We detected {len(detected_skills)} skills from your resume. Pre-filled below.")

skill_categories = ["Languages", "Frontend", "Backend", "Databases", "AI/ML", "DevOps/Cloud", "Tools"]
skills_data = {}

sc_cols = st.columns(2)
for i, cat in enumerate(skill_categories):
    # Pre-fill from detected skills if available
    prefill = ""
    if detected_skills:
        from utils.resume_parser import _SKILL_TO_CATEGORY
        cat_skills = [s.title() for s in detected_skills if _SKILL_TO_CATEGORY.get(s.lower()) == cat]
        prefill = ", ".join(cat_skills)

    with sc_cols[i % 2]:
        val = st.text_input(f"{cat}", value=prefill, placeholder=f"e.g. Python, Java, SQL")
        if val.strip():
            skills_data[cat] = [s.strip() for s in val.split(",") if s.strip()]

st.markdown("---")

# ── Section 3: Education ──────────────────────────────────────────────────────
st.markdown("### 🎓 Education")
num_edu = st.number_input("Number of education entries", min_value=1, max_value=4, value=1)
education = []
for i in range(int(num_edu)):
    st.markdown(f"**Entry {i+1}**")
    e1, e2, e3, e4 = st.columns(4)
    with e1: degree      = st.text_input("Degree *",      key=f"deg_{i}", placeholder="B.Tech Computer Science")
    with e2: institution = st.text_input("Institution *", key=f"inst_{i}", placeholder="ABC University")
    with e3: year        = st.text_input("Year",          key=f"yr_{i}",  placeholder="2020 - 2024")
    with e4: gpa         = st.text_input("GPA/Percentage",key=f"gpa_{i}", placeholder="8.5 / 10")
    if degree.strip():
        education.append({"degree": degree, "institution": institution, "year": year, "gpa": gpa})

st.markdown("---")

# ── Section 4: Experience ─────────────────────────────────────────────────────
st.markdown("### 💼 Work Experience")
num_exp = st.number_input("Number of experience entries (0 if fresher)", min_value=0, max_value=5, value=0)
experience = []
for i in range(int(num_exp)):
    st.markdown(f"**Job {i+1}**")
    x1, x2, x3 = st.columns(3)
    with x1: title    = st.text_input("Job Title *",  key=f"jtitle_{i}", placeholder="Software Engineer")
    with x2: company  = st.text_input("Company *",    key=f"jcomp_{i}",  placeholder="Google")
    with x3: duration = st.text_input("Duration",     key=f"jdur_{i}",   placeholder="Jun 2022 - Present")
    resp_raw = st.text_area("Responsibilities (one per line)", key=f"jresp_{i}", height=80,
        placeholder="• Developed REST APIs using FastAPI\n• Reduced latency by 30%")
    responsibilities = [r.lstrip("•-– ").strip() for r in resp_raw.splitlines() if r.strip()]
    if title.strip():
        experience.append({"title": title, "company": company, "duration": duration, "responsibilities": responsibilities})

st.markdown("---")

# ── Section 5: Projects ───────────────────────────────────────────────────────
st.markdown("### 🛠️ Projects")
num_proj = st.number_input("Number of projects", min_value=1, max_value=6, value=2)
projects = []
for i in range(int(num_proj)):
    st.markdown(f"**Project {i+1}**")
    p1, p2 = st.columns(2)
    with p1: proj_title = st.text_input("Project Title *", key=f"ptitle_{i}", placeholder="Skill Gap Analyzer")
    with p2: proj_link  = st.text_input("GitHub/Live Link", key=f"plink_{i}", placeholder="github.com/you/project")
    proj_tech = st.text_input("Technologies Used", key=f"ptech_{i}", placeholder="Python, React, FastAPI, Docker")
    proj_desc = st.text_area("Description (bullet points)", key=f"pdesc_{i}", height=70,
        placeholder="• Built a web app that analyzes skill gaps\n• Achieved 95% skill detection accuracy")
    if proj_title.strip():
        tech_list = [t.strip() for t in proj_tech.split(",") if t.strip()]
        projects.append({"title": proj_title, "description": proj_desc, "tech": tech_list, "link": proj_link})

st.markdown("---")

# ── Section 6: Certifications ─────────────────────────────────────────────────
st.markdown("### 🏆 Certifications (Optional)")
certs_raw = st.text_area("One per line: Name — Issuer (Year)",
    height=80, placeholder="AWS Certified Solutions Architect — Amazon (2023)\nTensorFlow Developer Certificate — Google (2023)")
certifications = []
for line in certs_raw.splitlines():
    if line.strip():
        certifications.append(line.strip())

st.markdown("---")

# ── Generate PDF ──────────────────────────────────────────────────────────────
if st.button("📄 Generate & Download Resume PDF", type="primary", use_container_width=True):
    resume_data = {
        "name":           name,
        "email":          email,
        "phone":          phone,
        "linkedin":       linkedin,
        "github":         github,
        "location":       location,
        "summary":        summary,
        "skills":         skills_data,
        "experience":     experience,
        "education":      education,
        "projects":       projects,
        "certifications": certifications,
    }

    errors = validate_resume_data(resume_data)
    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    else:
        with st.spinner("Building your PDF resume..."):
            pdf_bytes = build_resume_pdf(resume_data)

        safe_name = name.replace(" ", "_") if name else "resume"
        st.success("✅ Resume generated successfully!")
        st.download_button(
            label="⬇️ Download Resume PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.markdown("</div>", unsafe_allow_html=True)
