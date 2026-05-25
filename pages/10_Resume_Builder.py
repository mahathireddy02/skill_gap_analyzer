import streamlit as st
import sys, os
import base64
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.resume_builder import build_resume_pdf, validate_resume_data
from components.navbar import show_navbar

st.set_page_config(page_title="Resume Builder", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
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
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;border:1px solid rgba(255,255,240,0.18)!important;}
.template-preview-card{height:340px;display:flex;flex-direction:column;border-radius:14px;overflow:hidden;margin-bottom:6px;background:#fff;}
.template-preview-frame{width:100%;height:286px;border:0;background:#fff;display:block;}
.template-preview-footer{min-height:54px;padding:0.5rem 0.75rem;display:flex;justify-content:space-between;align-items:center;gap:0.6rem;
    background:#f8fafc;border-top:1px solid #e5e7eb;}
.template-preview-tags{font-size:0.66rem;font-weight:800;color:#111827;line-height:1.25;}
.template-preview-name{font-size:0.72rem;font-weight:900;white-space:nowrap;}
html,body,.stApp{color:#FFFFF0!important;}
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.18)!important;box-shadow:none!important;}
.template-preview-card{background:rgba(0,0,0,0.24)!important;border:1px solid rgba(255,255,240,0.14)!important;box-shadow:none!important;}
.template-preview-frame{background:#333F63!important;}
.template-preview-footer{background:rgba(0,0,0,0.24)!important;border-color:rgba(255,255,240,0.14)!important;color:#FFFFF0!important;}
.template-preview-tags,.template-preview-name{color:#FFFFF0!important;}
[style*="#7c3aed"],[style*="#4f46e5"],[style*="#059669"],[style*="#ffffff"],[style*="#fff"]{color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;}
[style*="rgba(124,58,237"],[style*="linear-gradient"]{background:rgba(0,0,0,0.24)!important;border-color:rgba(255,255,240,0.18)!important;color:#FFFFF0!important;}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

st.markdown("## 📝 Resume Builder")
st.caption("Pick a template, fill in your details, and download a professional PDF resume.")
st.markdown("")

db_user = get_user(st.session_state.email)

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_template" not in st.session_state:
    st.session_state.selected_template = None
if "template_chosen" not in st.session_state:
    st.session_state.template_chosen = False
if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

# ── Template metadata for preview cards ──────────────────────────────────────
TEMPLATE_META = {
    "Classic": {
        "icon": "📄", "accent": "#000000", "header_bg": "#ffffff",
        "header_text": "#000000", "sec_color": "#000000", "hr": "#000000",
        "desc": "Black & white, centered name. Traditional and ATS-safe.",
        "tags": ["Traditional", "ATS-Safe", "B&W"],
    },
    "Modern": {
        "icon": "✨", "accent": "#4f46e5", "header_bg": "#4f46e5",
        "header_text": "#ffffff", "sec_color": "#4f46e5", "hr": "#4f46e5",
        "desc": "Indigo header band, colored section titles. Clean and professional.",
        "tags": ["Popular", "Colorful", "Tech"],
    },
    "Minimal": {
        "icon": "🎯", "accent": "#059669", "header_bg": "#ffffff",
        "header_text": "#111827", "sec_color": "#059669", "hr": "#059669",
        "desc": "Green accents, lots of whitespace. Simple and elegant.",
        "tags": ["Clean", "Minimal", "Green"],
    },
    "Creative": {
        "icon": "🎨", "accent": "#7c3aed", "header_bg": "#7c3aed",
        "header_text": "#ffffff", "sec_color": "#7c3aed", "hr": "#7c3aed",
        "desc": "Purple header, bold section labels. Stands out from the crowd.",
        "tags": ["Bold", "Creative", "Purple"],
    },
}


PREVIEW_SAMPLE_DATA = {
    "name": "John Smith",
    "email": "john@email.com",
    "phone": "+91 9876543210",
    "location": "Mumbai",
    "linkedin": "linkedin.com/in/johnsmith",
    "github": "github.com/johnsmith",
    "summary": "Results-driven Software Engineer with experience building scalable web applications, APIs, and data-driven products.",
    "skills": {
        "Languages": {"skills": ["Python", "Java", "SQL"], "level": "Expert"},
        "Tools": {"skills": ["Docker", "Git", "AWS"], "level": "Intermediate"},
        "Frameworks": {"skills": ["FastAPI", "React"], "level": "Intermediate"},
    },
    "experience": [{
        "title": "Software Engineer",
        "company": "Google",
        "duration": "2022 - Present",
        "responsibilities": [
            "Built scalable REST APIs for production workflows",
            "Reduced service latency by 30%",
        ],
    }],
    "education": [{
        "degree": "B.Tech Computer Science",
        "institution": "ABC University",
        "year": "2020 - 2024",
        "gpa": "8.5",
    }],
    "projects": [{
        "title": "Skill Gap Analyzer",
        "description": "AI-assisted resume and career readiness platform",
        "tech": ["Python", "Streamlit"],
        "link": "",
    }],
    "certifications": ["AWS Certified Cloud Practitioner"],
}


@st.cache_data(show_spinner=False)
def _preview_pdf_b64(template: str) -> str:
    pdf = build_resume_pdf(PREVIEW_SAMPLE_DATA, template=template)
    return base64.b64encode(pdf).decode("ascii")


def _preview_pdf_card(template: str, meta: dict, border: str, shadow: str) -> str:
    pdf_b64 = _preview_pdf_b64(template)
    tags = " | ".join(meta["tags"])
    return f"""
<div class="template-preview-card" style="border:{border};box-shadow:{shadow};">
  <iframe class="template-preview-frame"
          src="data:application/pdf;base64,{pdf_b64}#toolbar=0&navpanes=0&scrollbar=0&view=FitH"></iframe>
  <div class="template-preview-footer">
    <div class="template-preview-tags">{tags}</div>
    <div class="template-preview-name" style="color:{meta['accent']};">{meta['icon']} {template}</div>
  </div>
</div>"""

# ── Template preview cards ────────────────────────────────────────────────────
st.markdown("### 🎨 Choose a Template")
st.caption("Each card is rendered from the same PDF template used for download. Click **Select** to choose one.")
st.markdown("")

cols = st.columns(4, gap="small")
for col, (tmpl, meta) in zip(cols, TEMPLATE_META.items()):
    with col:
        is_sel = st.session_state.selected_template == tmpl
        border = f"3px solid {meta['accent']}" if is_sel else "2px solid #e5e7eb"
        shadow = f"0 6px 24px {meta['accent']}44" if is_sel else "0 2px 8px rgba(0,0,0,0.06)"
        st.markdown(
            _preview_pdf_card(tmpl, meta, border, shadow),
            unsafe_allow_html=True
        )
        btn_label = "✅ Selected" if is_sel else f"Select {tmpl}"
        btn_type  = "primary" if is_sel else "secondary"
        if st.button(btn_label, key=f"tmpl_{tmpl}", use_container_width=True, type=btn_type):
            st.session_state.selected_template = tmpl
            st.session_state.template_chosen   = True
            st.switch_page("pages/11_Resume_Details.py")

st.markdown("")
if not st.session_state.template_chosen:
    st.info("👆 Select a template above to continue filling in your resume details.")
else:
    st.success(f"{st.session_state.selected_template} template selected.")
    if st.button("Continue to Resume Details", type="primary", use_container_width=True):
        st.switch_page("pages/11_Resume_Details.py")

st.stop()

# ── Gate: must pick a template first ─────────────────────────────────────────
if not st.session_state.template_chosen:
    st.markdown("")
    st.info("👆 Select a template above to continue filling in your resume details.")
    st.stop()

selected_template = st.session_state.selected_template
meta = TEMPLATE_META[selected_template]
st.markdown(
    f'<div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.25);'
    f'border-radius:10px;padding:0.5rem 1rem;font-size:0.88rem;margin:0.6rem 0 0.2rem;">'
    f'{meta["icon"]} Using <strong>{selected_template}</strong> template '
    f'<span style="opacity:0.5;font-size:0.78rem;">— fill your details below</span></div>',
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Personal Info ─────────────────────────────────────────────────────────────
st.markdown("### 👤 Personal Information")
c1, c2, c3 = st.columns(3)
with c1:
    name  = st.text_input("Full Name *", value=db_user.get("name", ""))
    email = st.text_input("Email *",     value=st.session_state.email)
with c2:
    phone    = st.text_input("Phone",    placeholder="+91 9876543210")
    linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
with c3:
    github   = st.text_input("GitHub",   placeholder="github.com/yourname")
    location = st.text_input("Location", placeholder="City, Country")

summary = st.text_area("Professional Summary", height=70,
    placeholder="Results-driven engineer with 2+ years building scalable apps...")

st.markdown("---")

# ── Skills ────────────────────────────────────────────────────────────────────
st.markdown("### 🧠 Skills")
st.caption("Add skills by category. Click + to add more rows.")

skills_data = {}
for i in range(st.session_state.num_skills):
    s1, s2, s3, s4 = st.columns([1.5, 3.5, 1.2, 0.5])
    with s1:
        cat = st.text_input("Category", key=f"scat_{i}", placeholder="e.g. Languages")
    with s2:
        val = st.text_input("Skills (comma-separated)", key=f"sval_{i}",
                            placeholder="e.g. Python, Java, SQL")
    with s3:
        level = st.selectbox("Level", ["Basic", "Intermediate", "Expert"], key=f"slvl_{i}")
    with s4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️", key=f"sdel_{i}"):
            st.session_state.num_skills = max(1, st.session_state.num_skills - 1)
            st.rerun()
    if cat.strip() and val.strip():
        skills_data[cat] = {"skills": [s.strip() for s in val.split(",") if s.strip()], "level": level}

if st.button("➕ Add Skill Category"):
    st.session_state.num_skills += 1
    st.rerun()

st.markdown("---")

# ── Education ─────────────────────────────────────────────────────────────────
st.markdown("### 🎓 Education")
num_edu = st.number_input("Number of entries", 1, 4, 1, key="num_edu")
education = []
for i in range(int(num_edu)):
    st.markdown(f"**Entry {i+1}**")
    e1, e2, e3, e4 = st.columns(4)
    with e1: deg  = st.text_input("Degree *",      key=f"deg_{i}",  placeholder="B.Tech CS")
    with e2: inst = st.text_input("Institution *", key=f"inst_{i}", placeholder="ABC Univ")
    with e3: yr   = st.text_input("Year",          key=f"yr_{i}",   placeholder="2020-2024")
    with e4: gpa  = st.text_input("GPA",           key=f"gpa_{i}",  placeholder="8.5")
    if deg.strip():
        education.append({"degree": deg, "institution": inst, "year": yr, "gpa": gpa})

st.markdown("---")

# ── Experience ────────────────────────────────────────────────────────────────
st.markdown("### 💼 Work Experience")
num_exp = st.number_input("Number of jobs (0 if fresher)", 0, 5, 0, key="num_exp")
experience = []
for i in range(int(num_exp)):
    st.markdown(f"**Job {i+1}**")
    x1, x2, x3 = st.columns(3)
    with x1: title = st.text_input("Title *",   key=f"jtitle_{i}", placeholder="Software Engineer")
    with x2: comp  = st.text_input("Company *", key=f"jcomp_{i}",  placeholder="Google")
    with x3: dur   = st.text_input("Duration",  key=f"jdur_{i}",   placeholder="Jun 2022 - Present")
    resp = st.text_area("Responsibilities (one per line)", key=f"jresp_{i}", height=70,
        placeholder="• Developed REST APIs\n• Reduced latency by 30%")
    if title.strip():
        experience.append({
            "title": title, "company": comp, "duration": dur,
            "responsibilities": [r.lstrip("•-– ").strip() for r in resp.splitlines() if r.strip()],
        })

st.markdown("---")

# ── Projects ──────────────────────────────────────────────────────────────────
st.markdown("### 🛠️ Projects")
num_proj = st.number_input("Number of projects", 1, 6, 2, key="num_proj")
projects = []
for i in range(int(num_proj)):
    st.markdown(f"**Project {i+1}**")
    p1, p2 = st.columns(2)
    with p1: ptitle = st.text_input("Title *", key=f"ptitle_{i}", placeholder="Skill Gap Analyzer")
    with p2: plink  = st.text_input("Link",    key=f"plink_{i}",  placeholder="github.com/you/project")
    ptech = st.text_input("Tech", key=f"ptech_{i}", placeholder="Python, React, Docker")
    pdesc = st.text_area("Description", key=f"pdesc_{i}", height=60,
        placeholder="• Built a web app\n• Achieved 95% accuracy")
    if ptitle.strip():
        projects.append({
            "title": ptitle, "description": pdesc,
            "tech": [t.strip() for t in ptech.split(",") if t.strip()], "link": plink,
        })

st.markdown("---")

# ── Certifications ────────────────────────────────────────────────────────────
st.markdown("### 🏆 Certifications (Optional)")
certs_raw = st.text_area("One per line", height=70,
    placeholder="AWS Certified Solutions Architect — Amazon (2023)")
certifications = [line.strip() for line in certs_raw.splitlines() if line.strip()]

st.markdown("---")

# ── Generate ──────────────────────────────────────────────────────────────────
resume_data = {
    "name": name, "email": email, "phone": phone,
    "linkedin": linkedin, "github": github, "location": location,
    "summary": summary, "skills": skills_data,
    "experience": experience, "education": education,
    "projects": projects, "certifications": certifications,
}

b1, b2 = st.columns(2)
with b1:
    preview_clicked  = st.button("👁️ Preview All Templates", use_container_width=True)
with b2:
    generate_clicked = st.button("📄 Generate & Download Resume", type="primary", use_container_width=True)

if preview_clicked or generate_clicked:
    errors = validate_resume_data(resume_data)
    if errors:
        for e in errors:
            st.error(f"❌ {e}")
    else:
        if preview_clicked:
            st.markdown("---")
            st.markdown("### 👁️ Preview — All 4 Templates")
            st.caption("Click any tab to preview. Use the download button below each preview.")
            templates_list = ["Classic", "Modern", "Minimal", "Creative"]
            icons = {t: TEMPLATE_META[t]["icon"] for t in templates_list}
            pdfs  = {}
            with st.spinner("Generating all 4 previews..."):
                for tmpl in templates_list:
                    pdfs[tmpl] = build_resume_pdf(resume_data, template=tmpl)
            tabs = st.tabs([f"{icons[t]} {t}" for t in templates_list])
            for tab, tmpl in zip(tabs, templates_list):
                with tab:
                    import base64
                    b64 = base64.b64encode(pdfs[tmpl]).decode()
                    st.markdown(
                        f'<iframe src="data:application/pdf;base64,{b64}" '
                        f'width="100%" height="700px" '
                        f'style="border:1px solid rgba(124,58,237,0.3);border-radius:12px;">'
                        f'</iframe>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("")
                    st.download_button(
                        f"⬇️ Download {tmpl} Template",
                        data=pdfs[tmpl],
                        file_name=f"{name.replace(' ','_')}_{tmpl}_resume.pdf",
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
                file_name=f"{name.replace(' ','_')}_resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
