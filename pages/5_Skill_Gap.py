import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
from utils.analyzer import get_roles, analyze_gap
from components.navbar import show_navbar

st.set_page_config(page_title="Skill Gap · SkillGap", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")
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

show_navbar("Skill Gap")

st.markdown("## 🧠 Skill Gap Analyzer")
st.markdown("Select your target role to see matched and missing skills.")
st.markdown("")

db_user     = get_user(st.session_state.email)
user_skills = db_user.get("skills", [])

col1, col2 = st.columns([1, 2])
with col1:
    role = st.selectbox("🎯 Target Role", get_roles())
    if st.button("Analyze Gap", type="primary", use_container_width=True):
        matched, missing, required = analyze_gap(user_skills, role)
        update_user(st.session_state.email, {"target_role": role, "missing_skills": missing})
        st.session_state["gap_result"] = (matched, missing, required, role)

with col2:
    if not user_skills:
        st.warning("⚠️ No skills found. Upload your resume first.")
        if st.button("Go to Resume Score →"):
            st.switch_page("pages/4_Resume_Score.py")

if "gap_result" in st.session_state:
    matched, missing, required, role = st.session_state["gap_result"]
    total = len(required)
    pct   = int(len(matched) / total * 100) if total else 0

    st.markdown("---")
    st.markdown(f"### 📊 Results for: **{role}**")
    m1, m2, m3 = st.columns(3)
    m1.metric("✅ Matched", len(matched))
    m2.metric("❌ Missing", len(missing))
    m3.metric("📈 Match Rate", f"{pct}%")
    st.progress(pct / 100)
    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ✅ Your Strengths")
        if matched:
            for s in matched: st.success(f"✅ {s}")
        else:
            st.info("No matching skills yet.")
    with c2:
        st.markdown("### ❌ Skills to Learn")
        if missing:
            for s in missing: st.error(f"❌ {s}")
            st.markdown("")
            if st.button("🛤️ Generate Roadmap", type="primary"):
                st.switch_page("pages/6_Roadmap.py")
        else:
            st.success("🎉 You have all required skills!")

st.markdown("</div>", unsafe_allow_html=True)
