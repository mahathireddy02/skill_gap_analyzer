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
/* progress */
.prog-wrap {display:flex;align-items:center;gap:0.6rem;margin-bottom:1.5rem;padding: 0 1rem;}
.prog-step {flex:1;height:4px;border-radius:999px;background:rgba(255,255,255,0.1);}
.prog-done {background:linear-gradient(90deg,#7c3aed,#4f46e5);}
.prog-active{background:linear-gradient(90deg,#a78bfa,#818cf8);}
.prog-lbl  {color:rgba(255,255,255,0.4);font-size:0.75rem;white-space:nowrap;}
.auth-card{
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;padding:1.4rem 1.8rem;margin-bottom:1.5rem;
}
.auth-icon {font-size:2rem;display:block;margin-bottom:0.3rem;}
.auth-title{color:#fff;font-size:1.35rem;font-weight:800;margin-bottom:0.1rem;}
.auth-sub  {color:rgba(255,255,255,0.4);font-size:0.84rem;margin-bottom:0.5rem;}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

if "rd_step" not in st.session_state:
    st.session_state.rd_step = 1

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

db_user = get_user(st.session_state.email)
step = st.session_state.rd_step

if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

meta = TEMPLATE_META.get(selected_template, {"icon": "📝"})

def _render_progress():
    s1 = "prog-done" if step > 1 else "prog-active"
    s2 = "prog-done" if step > 2 else ("prog-active" if step == 2 else "prog-step")
    s3 = "prog-done" if step > 3 else ("prog-active" if step == 3 else "prog-step")
    s4 = "prog-done" if step > 4 else ("prog-active" if step == 4 else "prog-step")
    s5 = "prog-active" if step == 5 else "prog-step"
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-step {s1}"></div>
        <div class="prog-step {s2}"></div>
        <div class="prog-step {s3}"></div>
        <div class="prog-step {s4}"></div>
        <div class="prog-step {s5}"></div>
        <span class="prog-lbl">Step {step} of 5</span>
    </div>
    """, unsafe_allow_html=True)

def _render_header(title, icon, sub):
    st.markdown(f"""
    <div class="auth-card">
        <span class="auth-icon">{icon}</span>
        <div class="auth-title">{title}</div>
        <div class="auth-sub">{sub}</div>
        <div style="background:rgba(124,58,237,0.1);border-radius:6px;padding:0.2rem 0.6rem;font-size:0.75rem;display:inline-block;color:#c4b5fd;">
            {meta['icon']} Using {selected_template} template
        </div>
    </div>
    """, unsafe_allow_html=True)

_render_progress()

if step == 1:
    _render_header("Personal Information", "👤", "Fill in your basic contact details and summary.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("Full Name *", value=db_user.get("name", ""), key="rd_name")
        st.text_input("Email *", value=st.session_state.email, key="rd_email")
    with c2:
        st.text_input("Phone", placeholder="+91 9876543210", key="rd_phone")
        st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname", key="rd_linkedin")
    with c3:
        st.text_input("GitHub", placeholder="github.com/yourname", key="rd_github")
        st.text_input("Location", placeholder="City, Country", key="rd_location")
    st.text_area("Professional Summary", height=100, placeholder="Results-driven engineer...", key="rd_summary")
    
    if st.button("Next: Skills →", type="primary", use_container_width=True):
        st.session_state.rd_step = 2
        st.rerun()

elif step == 2:
    _render_header("Skills", "🧠", "Add your technical and soft skills by category.")
    for i in range(st.session_state.num_skills):
        s1, s2, s3, s4 = st.columns([1.5, 3.5, 1.2, 0.5])
        with s1: st.text_input("Category", key=f"scat_{i}", placeholder="e.g. Languages")
        with s2: st.text_input("Skills (comma-separated)", key=f"sval_{i}", placeholder="e.g. Python, SQL")
        with s3: st.selectbox("Level", ["Basic", "Intermediate", "Expert"], key=f"slvl_{i}")
        with s4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"sdel_{i}"):
                st.session_state.num_skills = max(1, st.session_state.num_skills - 1)
                st.rerun()
    if st.button("➕ Add Skill Category"):
        st.session_state.num_skills += 1
        st.rerun()

    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.rd_step = 1
            st.rerun()
    with b2:
        if st.button("Next: Education →", type="primary", use_container_width=True):
            st.session_state.rd_step = 3
            st.rerun()

elif step == 3:
    _render_header("Education", "🎓", "List your academic qualifications.")
    num_edu = st.number_input("Number of entries", 1, 4, 1, key="num_edu")
    for i in range(int(num_edu)):
        st.markdown(f"**Entry {i + 1}**")
        e1, e2, e3, e4 = st.columns(4)
        with e1: st.text_input("Degree *", key=f"deg_{i}", placeholder="B.Tech CS")
        with e2: st.text_input("Institution *", key=f"inst_{i}", placeholder="ABC Univ")
        with e3: st.text_input("Year", key=f"yr_{i}", placeholder="2020-2024")
        with e4: st.text_input("GPA", key=f"gpa_{i}", placeholder="8.5")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.rd_step = 2
            st.rerun()
    with b2:
        if st.button("Next: Experience →", type="primary", use_container_width=True):
            st.session_state.rd_step = 4
            st.rerun()

elif step == 4:
    _render_header("Work Experience", "💼", "Detail your professional background or internships.")
    num_exp = st.number_input("Number of jobs (0 if fresher)", 0, 5, 0, key="num_exp")
    for i in range(int(num_exp)):
        st.markdown(f"**Job {i + 1}**")
        x1, x2, x3 = st.columns(3)
        with x1: st.text_input("Title *", key=f"jtitle_{i}", placeholder="Software Engineer")
        with x2: st.text_input("Company *", key=f"jcomp_{i}", placeholder="Google")
        with x3: st.text_input("Duration", key=f"jdur_{i}", placeholder="Jun 2022 - Present")
        st.text_area("Responsibilities (one per line)", key=f"jresp_{i}", height=80)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.rd_step = 3
            st.rerun()
    with b2:
        if st.button("Next: Projects →", type="primary", use_container_width=True):
            st.session_state.rd_step = 5
            st.rerun()

elif step == 5:
    _render_header("Projects & Certs", "🛠️", "Showcase your work and accomplishments.")
    num_proj = st.number_input("Number of projects", 0, 6, 2, key="num_proj")
    for i in range(int(num_proj)):
        st.markdown(f"**Project {i + 1}**")
        p1, p2 = st.columns(2)
        with p1: st.text_input("Title *", key=f"ptitle_{i}", placeholder="Skill Gap Analyzer")
        with p2: st.text_input("Link", key=f"plink_{i}", placeholder="github.com/...")
        st.text_input("Tech", key=f"ptech_{i}", placeholder="Python, React")
        st.text_area("Description", key=f"pdesc_{i}", height=70)

    st.markdown("### 🏆 Certifications (Optional)")
    st.text_area("One per line", height=80, key="rd_certs", placeholder="AWS Certified...")

    st.markdown("---")

    # Final Assembly and Buttons
    skills_data = {}
    for i in range(st.session_state.num_skills):
        cat = st.session_state.get(f"scat_{i}", "").strip()
        val = st.session_state.get(f"sval_{i}", "").strip()
        if cat and val:
            skills_data[cat] = {"skills": [s.strip() for s in val.split(",") if s.strip()], "level": st.session_state.get(f"slvl_{i}")}

    education = []
    for i in range(int(st.session_state.get("num_edu", 1))):
        deg = st.session_state.get(f"deg_{i}", "").strip()
        if deg: education.append({"degree": deg, "institution": st.session_state.get(f"inst_{i}"), "year": st.session_state.get(f"yr_{i}"), "gpa": st.session_state.get(f"gpa_{i}")})

    experience = []
    for i in range(int(st.session_state.get("num_exp", 0))):
        title = st.session_state.get(f"jtitle_{i}", "").strip()
        if title: experience.append({
            "title": title, "company": st.session_state.get(f"jcomp_{i}"), "duration": st.session_state.get(f"jdur_{i}"),
            "responsibilities": [r.lstrip("•-– ").strip() for r in st.session_state.get(f"jresp_{i}", "").splitlines() if r.strip()]
        })

    projects = []
    for i in range(int(st.session_state.get("num_proj", 0))):
        ptitle = st.session_state.get(f"ptitle_{i}", "").strip()
        if ptitle: projects.append({
            "title": ptitle, "description": st.session_state.get(f"pdesc_{i}"), "link": st.session_state.get(f"plink_{i}"),
            "tech": [t.strip() for t in st.session_state.get(f"ptech_{i}", "").split(",") if t.strip()]
        })

    resume_data = {
        "name": st.session_state.get("rd_name") or "", "email": st.session_state.get("rd_email") or "",
        "phone": st.session_state.get("rd_phone") or "", "linkedin": st.session_state.get("rd_linkedin") or "",
        "github": st.session_state.get("rd_github") or "", "location": st.session_state.get("rd_location") or "",
        "summary": st.session_state.get("rd_summary") or "", "skills": skills_data, "education": education,
        "experience": experience, "projects": projects,
        "certifications": [line.strip() for line in (st.session_state.get("rd_certs") or "").splitlines() if line.strip()]
    }

    b1, b2, b3 = st.columns([1, 2, 2])
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.rd_step = 4
            st.rerun()
    with b2:
        preview_clicked = st.button("👁️ Preview Templates", use_container_width=True)
    with b3:
        generate_clicked = st.button("📄 Generate & Download", type="primary", use_container_width=True)

    if preview_clicked or generate_clicked:
        name = resume_data["name"]
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
