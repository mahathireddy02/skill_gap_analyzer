import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, update_user
from utils.scorer import score_resume
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
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Score")

st.markdown("## 📄 Resume Scorer")
st.markdown("Upload your resume or paste text to get an ATS-style score and improvement tips.")
st.markdown("")

upload_tab, paste_tab = st.tabs(["📁 Upload PDF", "📋 Paste Text"])
resume_text = ""

with upload_tab:
    uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded:
        try:
            import pdfplumber
            with pdfplumber.open(uploaded) as pdf:
                resume_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
            st.success("✅ PDF parsed successfully!")
        except ImportError:
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded)
                resume_text = "\n".join(p.extract_text() or "" for p in reader.pages)
                st.success("✅ PDF parsed successfully!")
            except ImportError:
                st.error("Install pdfplumber: pip install pdfplumber")

with paste_tab:
    pasted = st.text_area("Paste your resume text here", height=280,
                          placeholder="Paste your full resume content...")
    if pasted:
        resume_text = pasted

if resume_text:
    st.markdown("---")
    if st.button("🔍 Analyze Resume", type="primary"):
        with st.spinner("Analyzing..."):
            score, skills, suggestions = score_resume(resume_text)
            update_user(st.session_state.email, {"resume_score": score, "skills": skills})

        col1, col2 = st.columns([1, 2])
        with col1:
            color = "#059669" if score >= 70 else "#d97706" if score >= 40 else "#dc2626"
            label = "Excellent 🌟" if score >= 70 else "Good 👍" if score >= 40 else "Needs Work ⚠️"
            st.markdown(f"""
            <div style="background:{color};border-radius:20px;padding:2rem;text-align:center;color:white;">
                <div style="font-size:3.5rem;font-weight:900;">{score}%</div>
                <div style="font-size:1.1rem;font-weight:700;margin-top:0.4rem;">{label}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("### 🧠 Skills Detected")
            if skills:
                cols = st.columns(3)
                for i, skill in enumerate(skills):
                    with cols[i % 3]:
                        st.success(f"✅ {skill}")
            else:
                st.warning("No recognizable skills found.")

        st.markdown("---")
        st.markdown("### 💡 Suggestions")
        if suggestions:
            for tip in suggestions:
                st.info(f"💡 {tip}")
        else:
            st.success("✅ Your resume looks great!")
        st.progress(score / 100)

st.markdown("</div>", unsafe_allow_html=True)
