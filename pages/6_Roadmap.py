import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.roadmap import get_roadmap
from components.navbar import show_navbar

st.set_page_config(page_title="Roadmap · SkillGap", page_icon="🛤️", layout="wide", initial_sidebar_state="collapsed")
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

show_navbar("Roadmap")

st.markdown("## 🛤️ Learning Roadmap")
st.markdown("Your personalized step-by-step plan to close the skill gap.")
st.markdown("")

db_user = get_user(st.session_state.email)
missing = db_user.get("missing_skills", [])
role    = db_user.get("target_role", "")

if not missing:
    st.info("No missing skills found. Run the Skill Gap Analyzer first.")
    if st.button("Go to Skill Gap Analyzer →", type="primary"):
        st.switch_page("pages/5_Skill_Gap.py")
else:
    if role:
        st.markdown(f"**Target Role:** 🎯 {role} &nbsp;|&nbsp; **Skills to Learn:** {len(missing)}")
        st.markdown("")

    roadmap = get_roadmap(missing)
    LEVELS  = {
        "beginner":     ("#d1fae5", "#065f46", "🟢 Beginner"),
        "intermediate": ("#fef3c7", "#92400e", "🟡 Intermediate"),
        "advanced":     ("#fee2e2", "#991b1b", "🔴 Advanced"),
    }
    for skill, steps in roadmap.items():
        with st.expander(f"📚 {skill.title()}", expanded=True):
            c1, c2, c3 = st.columns(3)
            for col, level in zip([c1, c2, c3], ["beginner", "intermediate", "advanced"]):
                bg, fg, lbl = LEVELS[level]
                with col:
                    st.markdown(f"""
                    <div style="background:{bg};border-radius:12px;padding:1rem;color:{fg};min-height:110px;">
                        <strong style="font-size:0.85rem;">{lbl}</strong><br><br>
                        <span style="font-size:0.82rem;line-height:1.5;">{steps[level]}</span>
                    </div>""", unsafe_allow_html=True)
            st.markdown("")

    st.markdown("---")
    st.info("💡 Start with Beginner, build projects, then move to Intermediate.")
    st.info("💡 1 hour daily beats 8 hours once a week.")

st.markdown("</div>", unsafe_allow_html=True)
