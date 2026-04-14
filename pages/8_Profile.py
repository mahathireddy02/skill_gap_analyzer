import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
from components.navbar import show_navbar

st.set_page_config(page_title="Profile · SkillGap", page_icon="👤", layout="wide", initial_sidebar_state="collapsed")
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

show_navbar("Profile")

st.markdown("## 👤 My Profile")
st.markdown("")

email   = st.session_state.email
db_user = get_user(email)
name    = db_user.get("name", "")
initial = name[0].upper() if name else "U"

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:20px;
                padding:2rem;text-align:center;color:white;">
        <div style="width:72px;height:72px;background:rgba(255,255,255,0.2);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    font-size:2rem;font-weight:800;margin:0 auto 1rem;">{initial}</div>
        <h3 style="margin:0 0 0.3rem;font-size:1.2rem;">{name}</h3>
        <p style="opacity:0.75;margin:0;font-size:0.85rem;">{email}</p>
        <div style="margin-top:1rem;background:rgba(255,255,255,0.15);
                    border-radius:8px;padding:0.4rem 0.8rem;font-size:0.85rem;">
            🎯 {db_user.get('target_role','No role set')}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### ✏️ Update Profile")
    new_name    = st.text_input("Full Name",   value=db_user.get("name", ""),        key="p_name")
    target_role = st.text_input("Target Role", value=db_user.get("target_role", ""), key="p_role")

    if st.button("💾 Save Changes", type="primary"):
        update_user(email, {"name": new_name, "target_role": target_role})
        st.session_state.user["name"] = new_name
        st.success("✅ Profile updated!")

    st.markdown("---")
    st.markdown("### 📊 Account Stats")
    s1, s2, s3 = st.columns(3)
    s1.metric("Resume Score",   f"{db_user.get('resume_score', 0)}%")
    s2.metric("Skills Found",   len(db_user.get("skills", [])))
    s3.metric("Skills Missing", len(db_user.get("missing_skills", [])))

st.markdown("---")
with st.expander("⚠️ Danger Zone"):
    st.warning("This will clear all your skill and resume data.")
    if st.button("🗑️ Reset My Data"):
        update_user(email, {"skills": [], "missing_skills": [], "resume_score": 0, "target_role": ""})
        st.success("Data reset.")
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
