import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
from utils.readiness import calculate_readiness, has_gap_analysis
from utils.skill_analyzer import analyze_skill_gap
from components.navbar import show_navbar

st.set_page_config(page_title="Analytics · SkillGap", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
require_login()

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.block-container{padding:0!important;max-width:100%!important;}
</style>
""", unsafe_allow_html=True)

show_navbar("Analytics")

st.markdown("## 📊 Analytics")
st.markdown("Track your skill progress and readiness over time.")
st.markdown("")

db_user      = get_user(st.session_state.email)
skills       = db_user.get("skills", [])
missing      = db_user.get("missing_skills", [])
resume_score = db_user.get("resume_score", 0)
role         = db_user.get("target_role", "N/A")

if skills and role != "N/A" and not has_gap_analysis(db_user):
    try:
        gap_result = analyze_skill_gap(skills, role)
        missing = gap_result.get("missing_skills", [])
        db_user.update({
            "missing_skills": missing,
            "gap_result": gap_result,
            "gap_analyzed": True,
        })
        update_user(st.session_state.email, {
            "missing_skills": missing,
            "gap_result": gap_result,
            "gap_analyzed": True,
        })
    except ValueError:
        pass

readiness    = calculate_readiness(skills, missing, has_gap_analysis(db_user), db_user.get("gap_result", {}))

c1, c2, c3, c4 = st.columns(4)
c1.metric("📄 Resume Score",   f"{resume_score}%")
c2.metric("✅ Skills Found",   len(skills))
c3.metric("❌ Skills Missing", len(missing))
c4.metric("📈 Readiness",      f"{readiness}%")

st.markdown("---")
cl, cr = st.columns(2)
with cl:
    st.markdown("### 🧠 Skill Match")
    if has_gap_analysis(db_user):
        df = pd.DataFrame({"Category": ["✅ Matched", "❌ Missing"], "Count": [len(skills), len(missing)]}).set_index("Category")
        st.bar_chart(df)
    else:
        st.info("Run Skill Gap Analyzer to calculate matched and missing role skills.")

with cr:
    st.markdown("### 📄 Resume Score")
    st.markdown(f"**Overall: {resume_score}%**")
    st.progress(resume_score / 100)
    df2 = pd.DataFrame({"Component": ["Skills","Sections","Length","Contact","Action Verbs"],
                        "Max Points": [40, 30, 15, 10, 5]}).set_index("Component")
    st.bar_chart(df2)

st.markdown("---")
st.markdown("### 📅 Weekly Progress")
weeks  = ["Week 1","Week 2","Week 3","Week 4","Week 5","Week 6"]
scores = [20, 35, 45, 55, 68, resume_score if resume_score else 72]
st.line_chart(pd.DataFrame({"Resume Score": scores}, index=weeks))

if role != "N/A":
    st.markdown("---")
    status = f"**{readiness}%**" if has_gap_analysis(db_user) else "**Not calculated yet**"
    st.info(f"🎯 Target Role: **{role}** | Readiness: {status}")

st.markdown("</div>", unsafe_allow_html=True)
