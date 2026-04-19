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

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{{font-family:'Inter',sans-serif!important;box-sizing:border-box;}}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{{display:none!important;visibility:hidden!important;}}
html,body{{margin:0!important;padding:0!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}
div[data-testid="stButton"] button{{font-weight:700!important;border-radius:10px!important;transition:all 0.2s!important;}}
div[data-testid="stButton"] button[kind="primary"]{{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}}
.stTabs [data-baseweb="tab-list"]{{gap:4px;padding:4px;}}
.stTabs [data-baseweb="tab"]{{border-radius:10px!important;padding:0.4rem 1.2rem!important;font-weight:600!important;}}
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
        <div style="font-size:1.4rem;font-weight:800;">{name}</div>
        <div style="opacity:0.75;font-size:0.88rem;">{email}</div>
        <div style="margin-top:0.4rem;background:rgba(255,255,255,0.15);
                    border-radius:6px;padding:0.25rem 0.7rem;font-size:0.82rem;display:inline-block;">
            🎯 {db_user.get('target_role','No role set')}
        </div>
    </div>
    <div style="margin-left:auto;opacity:0.6;font-size:0.8rem;">
        {'🌙 Dark' if theme == 'dark' else '☀️ Light'}
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👤 Profile", "⚙️ Settings", "⚠️ Danger Zone"])

# ── TAB 1: Profile ────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### ✏️ Edit Profile")
    stored_name = db_user.get("name", "")
    parts = stored_name.split(" ", 1)
    nc1, nc2 = st.columns(2)
    with nc1:
        new_first = st.text_input("First Name", value=parts[0] if parts else "", key="p_fname")
    with nc2:
        new_last  = st.text_input("Last Name",  value=parts[1] if len(parts) > 1 else "", key="p_lname")
    new_role = st.text_input("Target Role", value=db_user.get("target_role", ""), key="p_role",
                              placeholder="e.g. Data Scientist, Full Stack Developer")
    new_bio  = st.text_area("Bio (optional)", value=db_user.get("bio", ""), key="p_bio",
                             height=80, placeholder="Tell us a bit about yourself...")
    if st.button("💾 Save Profile", type="primary", key="save_profile"):
        new_name = f"{new_first.strip()} {new_last.strip()}".strip()
        update_user(email, {"name": new_name, "target_role": new_role, "bio": new_bio})
        st.session_state.user["name"] = new_name
        st.success("✅ Profile saved!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Account Stats")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Resume Score",   f"{db_user.get('resume_score', 0)}%")
    s2.metric("Skills Found",   len(db_user.get("skills", [])))
    s3.metric("Skills Missing", len(db_user.get("missing_skills", [])))
    s4.metric("Weeks Done",     len(db_user.get("checked_weeks", [])))

# ── TAB 2: Settings ───────────────────────────────────────────────────────────
with tab2:

    # Appearance — single toggle
    st.markdown("### 🎨 Appearance")
    cur_theme = db_user.get("theme", "dark")
    new_light = st.toggle("☀️ Light Mode", value=(cur_theme == "light"), key="theme_toggle")
    if new_light != (cur_theme == "light"):
        update_user(email, {"theme": "light" if new_light else "dark"})
        st.rerun()

    st.markdown("---")

    # Change Password
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

    # Notifications
    st.markdown("### 🔔 Notifications")
    notif = db_user.get("notifications", {"weekly_reminder": True, "tips": True})
    n1 = st.toggle("📅 Weekly progress reminder", value=notif.get("weekly_reminder", True), key="n_weekly")
    st.caption("Shows a reminder banner when you log in after 7+ days.")
    n2 = st.toggle("💡 Learning tips on dashboard", value=notif.get("tips", True), key="n_tips")
    st.caption("Shows a daily tip card on your dashboard.")
    if st.button("💾 Save Notification Settings", key="save_notif"):
        update_user(email, {"notifications": {"weekly_reminder": n1, "tips": n2}})
        st.success("✅ Saved!")

    st.markdown("---")

    # Export
    st.markdown("### 📦 Export My Data")
    export = {
        "name":           db_user.get("name"),
        "email":          email,
        "target_role":    db_user.get("target_role"),
        "skills":         db_user.get("skills", []),
        "missing_skills": db_user.get("missing_skills", []),
        "resume_score":   db_user.get("resume_score", 0),
    }
    st.download_button(
        label="⬇️ Download My Data (JSON)",
        data=_json.dumps(export, indent=2),
        file_name="skillgap_my_data.json",
        mime="application/json",
        use_container_width=True,
    )

# ── TAB 3: Danger Zone ────────────────────────────────────────────────────────
with tab3:
    st.markdown("### ⚠️ Danger Zone")
    with st.expander("🗑️ Reset All Data"):
        st.warning("Clears resume score, skills, and roadmap progress. Your account stays.")
        if st.button("🗑️ Reset My Data", key="reset_data"):
            update_user(email, {"skills": [], "missing_skills": [], "resume_score": 0, "target_role": "", "checked_weeks": []})
            st.success("✅ All data reset.")
            st.rerun()

    st.markdown("")
    with st.expander("🚨 Delete Account"):
        st.error("**Permanently deletes your account and all data. Cannot be undone.**")
        confirm = st.text_input("Type your email to confirm", placeholder=email, key="del_confirm")
        if st.button("🚨 Delete My Account", type="primary", key="del_btn"):
            if confirm.strip().lower() != email.strip().lower():
                st.error("Email doesn't match.")
            else:
                delete_account(email)
                st.session_state.clear()
                st.switch_page("app.py")
