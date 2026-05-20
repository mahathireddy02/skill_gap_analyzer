import streamlit as st
import sys, os, json as _json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user, delete_account, login as auth_login, _hash as _h
from components.navbar import show_navbar

st.set_page_config(page_title="Profile · SkillGap", page_icon="👤", layout="wide", initial_sidebar_state="collapsed")
require_login()

email   = st.session_state.email
db_user = get_user(email)
theme   = db_user.get("theme", "dark")
if st.query_params.get("action") == "logout":
    st.session_state.clear()
    st.query_params.clear()
    st.switch_page("app.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.block-container{padding:0!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;transition:all 0.2s!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
.stTabs [data-baseweb="tab-list"]{gap:4px;padding:4px;}
.stTabs [data-baseweb="tab"]{border-radius:10px!important;padding:0.4rem 1.2rem!important;font-weight:600!important;}
</style>
""", unsafe_allow_html=True)

show_navbar("Profile")

name    = db_user.get("name", "")
initial = name[0].upper() if name else "U"

st.markdown(f"""
<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:20px;
            padding:1.8rem 2rem;color:white;display:flex;align-items:center;gap:1.5rem;
            margin-bottom:1.5rem;">
    <div style="width:72px;height:72px;background:rgba(255,255,255,0.2);border-radius:50%;
                display:flex;align-items:center;justify-content:center;
                font-size:2rem;font-weight:800;flex-shrink:0;">{initial}</div>
    <div>
        <div style="display:flex;align-items:center;gap:0.75rem;">
            <span style="font-size:1.4rem;font-weight:800;">{name}</span>
            <a href="?action=logout" target="_self"
               style="font-size:0.75rem;font-weight:600;color:rgba(255,255,255,0.9);
                      background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);
                      border-radius:6px;padding:0.2rem 0.6rem;text-decoration:none;
                      transition:background 0.15s;">🚪 Logout</a>
        </div>
        <div style="opacity:0.75;font-size:0.88rem;">{email}</div>
        <div style="margin-top:0.4rem;background:rgba(255,255,255,0.15);
                    border-radius:6px;padding:0.25rem 0.7rem;font-size:0.82rem;display:inline-block;">
            🎯 {db_user.get('target_role','No role set')}
        </div>
    </div>
    <div style="margin-left:auto;opacity:0.6;font-size:0.8rem;text-align:right;line-height:1.9;">
        {'🌙 Dark' if theme == 'dark' else '☀️ Light'}<br>
        {db_user.get('skill_level','Beginner')}<br>
        {db_user.get('experience_type','Student')}<br>
        ⏱️ {db_user.get('time_availability','')}
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👤 Profile", "⚙️ Settings", "⚠️ Danger Zone"])

# TAB 1: Profile
with tab1:
    st.markdown("### ✏️ Edit Profile")
    stored_name = db_user.get("name", "")
    parts = stored_name.split(" ", 1)
    nc1, nc2 = st.columns(2)
    with nc1:
        new_first = st.text_input("First Name", value=parts[0] if parts else "", key="p_fname")
    with nc2:
        new_last  = st.text_input("Last Name",  value=parts[1] if len(parts) > 1 else "", key="p_lname")
    from utils.skill_analyzer import get_roles
    
    import re
    from difflib import get_close_matches

    ALL_ROLES    = get_roles()
    saved_role   = db_user.get("target_role", "").strip()
    is_other     = saved_role and saved_role not in ALL_ROLES
    role_options = ["-- Select a Role --"] + ALL_ROLES + ["Other"]
    default_idx  = (ALL_ROLES.index(saved_role) + 1) if saved_role in ALL_ROLES else (len(role_options)-1 if is_other else 0)

    selected = st.selectbox("Target Role", role_options, index=default_idx, key="p_role_select")
    
    is_valid = True
    new_role = saved_role
    if selected == "-- Select a Role --":
        new_role = ""
    elif selected == "Other":
        custom = st.text_input("Enter custom role", value=saved_role if is_other else "",
                               placeholder="Type your role (e.g. Hotel Manager)",
                               key="p_role_custom", label_visibility="collapsed")
        custom = custom.strip()
        if custom:
            if len(custom) < 3:
                st.error("Role must be at least 3 characters long.")
                is_valid = False
            elif not re.match(r"^[A-Za-z\s\-]+$", custom):
                st.error("Role must contain only letters, spaces, and hyphens.")
                is_valid = False
            else:
                close = get_close_matches(custom.lower(), [r.lower() for r in ALL_ROLES], n=1, cutoff=0.8)
                if close:
                    matched = ALL_ROLES[[r.lower() for r in ALL_ROLES].index(close[0])]
                    st.error(f"Did you mean '{matched}'? Please select it from the dropdown to avoid spelling mistakes.")
                    is_valid = False
                else:
                    new_role = custom
        else:
            new_role = saved_role if is_other else ""
    else:
        new_role = selected

    new_bio  = st.text_area("Bio (optional)", value=db_user.get("bio", ""), key="p_bio",
                             height=80, placeholder="Tell us a bit about yourself...")
    if st.button("💾 Save Profile", type="primary", key="save_profile"):
        if is_valid:
            new_name = f"{new_first.strip()} {new_last.strip()}".strip()
            update_user(email, {"name": new_name, "target_role": new_role, "bio": new_bio})
            st.session_state.user["name"] = new_name
            st.success("✅ Profile saved!")
            st.rerun()
        else:
            st.error("Please fix the errors before saving.")

    st.markdown("---")
    st.markdown("### 📊 Account Stats")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Resume Score",   f"{db_user.get('resume_score', 0)}%")
    s2.metric("Skills Found",   len(db_user.get("skills", [])))
    s3.metric("Skills Missing", len(db_user.get("missing_skills", [])))
    s4.metric("Weeks Done",     len(db_user.get("checked_weeks", [])))

    st.markdown("---")
    st.markdown("### ⚙️ Career Preferences")
    TIME_OPTS  = ["Less than 5 hrs", "5–10 hrs", "10+ hrs"]
    EXP_OPTS   = ["Student", "Fresher", "Working Professional"]
    LEVEL_OPTS = ["Beginner", "Intermediate", "Advanced"]
    sv_time  = db_user.get("time_availability", "5–10 hrs")
    sv_exp   = db_user.get("experience_type",   "Student")
    sv_level = db_user.get("skill_level",        "Beginner")
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        new_time  = st.selectbox("⏰ Time Availability", TIME_OPTS,
                                 index=TIME_OPTS.index(sv_time) if sv_time in TIME_OPTS else 1,
                                 key="p_time")
    with pc2:
        new_exp   = st.selectbox("🎓 Experience", EXP_OPTS,
                                 index=EXP_OPTS.index(sv_exp) if sv_exp in EXP_OPTS else 0,
                                 key="p_exp")
    with pc3:
        new_level = st.selectbox("📊 Skill Level", LEVEL_OPTS,
                                 index=LEVEL_OPTS.index(sv_level) if sv_level in LEVEL_OPTS else 0,
                                 key="p_level")
    if st.button("💾 Save Preferences", key="save_prefs"):
        update_user(email, {
            "time_availability": new_time,
            "experience_type":   new_exp,
            "skill_level":       new_level,
        })
        st.success("✅ Preferences saved!")
        st.rerun()

# TAB 2: Settings
with tab2:
    st.markdown("### 🔑 Change Password")
    cur_pw = st.text_input("Current Password", type="password", key="cp_cur")
    pw1, pw2 = st.columns(2)
    with pw1:
        new_pw = st.text_input("New Password", type="password", key="cp_new", placeholder="Min 6 characters")
    with pw2:
        cnf_pw = st.text_input("Confirm New Password", type="password", key="cp_cnf")
    if st.button("🔄 Update Password", type="primary", key="cp_btn"):
        if not all([cur_pw, new_pw, cnf_pw]):
            st.error("Fill in all fields.")
        elif len(new_pw) < 6:
            st.error("New password must be at least 6 characters.")
        elif new_pw != cnf_pw:
            st.error("Passwords do not match.")
        else:
            ok, _ = auth_login(email, cur_pw)
            if not ok:
                st.error("Current password is incorrect.")
            else:
                update_user(email, {"password": _h(new_pw)})
                st.success("✅ Password updated!")

    st.markdown("---")

    st.markdown("### 🔔 Notifications")
    notif = db_user.get("notifications", {"weekly_reminder": True, "tips": True})
    n1 = st.toggle("📅 Weekly progress reminder", value=notif.get("weekly_reminder", True), key="n_weekly")
    st.caption("Shows a reminder banner when you log in after 7+ days.")
    n2 = st.toggle("💡 Learning tips on dashboard", value=notif.get("tips", True), key="n_tips")
    st.caption("Shows a daily tip card on your dashboard.")
    if st.button("💾 Save Notification Settings", key="save_notif"):
        update_user(email, {"notifications": {"weekly_reminder": n1, "tips": n2}})
        st.success("✅ Saved!")

# TAB 3: Danger Zone
with tab3:
    st.markdown("### ⚠️ Danger Zone")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 🗑️ Reset All Data")
    st.warning("Clears your resume score, skills, missing skills, and roadmap progress. Your account stays active.")
    if st.button("🗑️ Reset My Data", key="reset_data"):
        update_user(email, {
            "skills": [], "missing_skills": [], "gap_result": {}, "gap_analyzed": False,
            "resume_score": 0, "target_role": "", "checked_weeks": [], "roadmap_result": None,
            "resume_score_history": [],
            "resume_file_hashes": [],
            "resume_content_hashes": []
        })
        for key in ["resume_result", "resume_file_key", "duplicate_resume_key", "gap_result"]:
            st.session_state.pop(key, None)
        st.success("✅ All data reset.")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 🚨 Delete Account")
    st.error("⚠️ Permanently deletes your account and all data. This cannot be undone.")
    confirm = st.text_input("Type your email address to confirm", placeholder=email, key="del_confirm")
    if st.button("🚨 Delete My Account", type="primary", key="del_btn"):
        if confirm.strip().lower() != email.strip().lower():
            st.error("❌ Email doesn't match.")
        else:
            delete_account(email)
            st.query_params.clear()
            st.session_state.clear()
            st.switch_page("app.py")
