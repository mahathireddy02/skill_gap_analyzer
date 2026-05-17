import sys, os
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import signup
from utils.skill_analyzer import get_roles, ROLE_DATASET
from components.role_autocomplete import role_autocomplete
from components.theme import BG_ANIMATED

st.set_page_config(page_title="Sign Up · SkillGap", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

if st.session_state.get("user"):
    st.switch_page("pages/3_Dashboard.py")

# ── Session state init ────────────────────────────────────────────────────────
if "su_step"   not in st.session_state: st.session_state.su_step   = 1
if "su_data"   not in st.session_state: st.session_state.su_data   = {}
if "su_custom" not in st.session_state: st.session_state.su_custom = []
if "su_role"   not in st.session_state: st.session_state.su_role   = ""

ALL_ROLES  = get_roles()
ALL_SKILLS = sorted(set(
    s for rd in ROLE_DATASET.values()
    for tier in ("core", "important", "nice_to_have")
    for s in rd.get(tier, [])
))

step = st.session_state.su_step

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],[data-testid="stSidebarNav"],[data-testid="stSidebar"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"],.stDeployButton,
[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.stApp{
    background:""" + BG_ANIMATED + """!important;
    background-size:100% 100%,100% 100%,400% 400%!important;
    animation:bgShift 14s ease infinite!important;
    min-height:100vh!important;
}
@keyframes bgShift{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}
.block-container{padding:2rem 1rem!important;max-width:100%!important;}
.auth-card{
    background:rgba(255,255,255,0.055);backdrop-filter:blur(24px);
    border:1px solid rgba(255,255,255,0.1);border-radius:24px;
    padding:1.6rem 2.2rem 1.2rem;animation:slideUp 0.45s ease both;
}
@keyframes slideUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:translateY(0);}}
.auth-icon {font-size:2.4rem;text-align:center;display:block;margin-bottom:0.3rem;}
.auth-title{text-align:center;color:#fff;font-size:1.5rem;font-weight:800;margin-bottom:0.1rem;}
.auth-sub  {text-align:center;color:rgba(255,255,255,0.4);font-size:0.84rem;margin-bottom:1rem;}
.sec-lbl   {color:rgba(255,255,255,0.35);font-size:0.7rem;font-weight:600;
             text-transform:uppercase;letter-spacing:0.8px;margin:0.9rem 0 0.2rem;}
/* progress */
.prog-wrap {display:flex;align-items:center;gap:0.6rem;margin-bottom:1.2rem;}
.prog-step {flex:1;height:4px;border-radius:999px;background:rgba(255,255,255,0.1);}
.prog-done {background:linear-gradient(90deg,#7c3aed,#4f46e5);}
.prog-active{background:linear-gradient(90deg,#a78bfa,#818cf8);}
.prog-lbl  {color:rgba(255,255,255,0.4);font-size:0.75rem;white-space:nowrap;}
/* inputs */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label
{color:rgba(255,255,255,0.65)!important;font-size:0.85rem!important;font-weight:500!important;}
div[data-testid="stTextInput"] input{
    background:rgba(255,255,255,0.07)!important;
    border:1px solid rgba(255,255,255,0.12)!important;
    border-radius:10px!important;color:#fff!important;font-size:0.92rem!important;
}
div[data-testid="stTextInput"] input:focus{
    border-color:rgba(167,139,250,0.5)!important;
    box-shadow:0 0 0 3px rgba(167,139,250,0.12)!important;
}
div[data-testid="stSelectbox"]>div>div,
div[data-testid="stMultiSelect"]>div>div{
    background:rgba(255,255,255,0.07)!important;
    border:1px solid rgba(255,255,255,0.12)!important;
    border-radius:10px!important;color:#fff!important;
}
div[data-testid="stRadio"] label{color:rgba(255,255,255,0.75)!important;font-size:0.88rem!important;}
div[data-testid="stRadio"]>div{gap:0.5rem!important;}
/* buttons */
div[data-testid="stButton"] button{
    font-family:'Inter',sans-serif!important;font-weight:700!important;
    border-radius:10px!important;font-size:0.92rem!important;transition:all 0.2s!important;
}
div[data-testid="stButton"] button[kind="primary"]{
    background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;
    box-shadow:0 4px 16px rgba(124,58,237,0.3)!important;border:none!important;
}
div[data-testid="stButton"] button[kind="secondary"]{
    background:rgba(255,255,255,0.07)!important;
    border:1px solid rgba(255,255,255,0.15)!important;
    color:rgba(255,255,255,0.8)!important;
}
/* autocomplete pills */
.ac-pill-wrap{
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
    border-radius:10px;padding:0.45rem 0.5rem;margin-top:0.25rem;
    display:flex;flex-wrap:wrap;gap:0.3rem;
}
.or-div{display:flex;align-items:center;gap:0.8rem;
    color:rgba(255,255,255,0.25);font-size:0.78rem;margin:1rem 0;}
.or-div::before,.or-div::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.08);}
</style>
""", unsafe_allow_html=True)

# ── Back to home ──────────────────────────────────────────────────────────────
_, back_col, _ = st.columns([1, 6, 1])
with back_col:
    if st.button("← Back to Home", key="su_back"):
        st.session_state.su_step = 1
        st.session_state.su_data = {}
        st.session_state.su_custom = []
        st.session_state.su_role = ""
        st.switch_page("app.py")

_, center, _ = st.columns([1, 1.5, 1])

with center:

    # ── Progress bar ──────────────────────────────────────────────────────────
    s1 = "prog-done" if step > 1 else "prog-active"
    s2 = "prog-done" if step > 2 else ("prog-active" if step == 2 else "prog-step")
    s3 = "prog-active" if step == 3 else "prog-step"
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-step {s1}"></div>
        <div class="prog-step {s2}"></div>
        <div class="prog-step {s3}"></div>
        <span class="prog-lbl">Step {step} of 3</span>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 1 — Personal Info (original, unchanged)
    # ══════════════════════════════════════════════════════════════════════════
    if step == 1:
        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">✨</span>
            <div class="auth-title">Create Your Account</div>
            <div class="auth-sub">Join thousands of students accelerating their careers</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-lbl">👤 Personal Info</div>', unsafe_allow_html=True)
        nc1, nc2 = st.columns(2)
        with nc1:
            first_name = st.text_input("First Name", placeholder="John", key="su_fname",
                                       value=st.session_state.su_data.get("first_name", ""))
        with nc2:
            last_name  = st.text_input("Last Name",  placeholder="Doe",  key="su_lname",
                                       value=st.session_state.su_data.get("last_name", ""))
        email = st.text_input("Email Address", placeholder="you@example.com", key="su_email",
                              value=st.session_state.su_data.get("email", ""))

        st.markdown('<div class="sec-lbl">🔑 Password</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            password = st.text_input("Password", type="password", placeholder="Min 6 chars", key="su_pw")
        with c2:
            confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat", key="su_cpw")

        st.markdown('<div class="sec-lbl">🛡️ Security Question — used for password reset</div>', unsafe_allow_html=True)
        sec_q = st.selectbox("Security Question", [
            "What was the name of your first pet?",
            "What city were you born in?",
            "What is your mother's maiden name?",
            "What was the name of your first school?",
            "What is your favourite movie?",
        ], key="su_sq")
        sec_a = st.text_input("Your Answer", placeholder="Answer (case-insensitive)", key="su_sa")

        st.markdown("")
        if st.button("Next → Career & Skills", use_container_width=True, type="primary", key="su_next1"):
            if not all([first_name.strip(), last_name.strip(), email.strip(), password, confirm, sec_a.strip()]):
                st.error("Please fill in all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")
            else:
                st.session_state.su_data.update({
                    "first_name": first_name.strip(),
                    "last_name":  last_name.strip(),
                    "email":      email.strip(),
                    "password":   password,
                    "sec_q":      sec_q,
                    "sec_a":      sec_a.strip(),
                })
                st.session_state.su_step = 2
                st.rerun()

        st.markdown('<div class="or-div">or</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.4);font-size:0.85rem;margin:0 0 0.5rem;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button("🔐 Sign In Instead", use_container_width=True, key="su_login"):
            st.switch_page("pages/1_Login.py")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 2 — Career & Skills
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 2:
        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">🎯</span>
            <div class="auth-title">Career & Skills</div>
            <div class="auth-sub">Help us personalise your learning journey</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Target Role with autocomplete ─────────────────────────────────────
        st.markdown('<div class="sec-lbl">🎯 Target Role</div>', unsafe_allow_html=True)
        target_role = role_autocomplete(ALL_ROLES, default=st.session_state.su_role,
                                        key="su_role", dark=True)
        st.session_state.su_role = target_role

        if target_role:
            bg  = "rgba(124,58,237,0.15)" if target_role in ALL_ROLES else "rgba(255,255,255,0.06)"
            bd  = "rgba(124,58,237,0.35)" if target_role in ALL_ROLES else "rgba(255,255,255,0.15)"
            lbl = target_role if target_role in ALL_ROLES else f"{target_role} (custom)"
            st.markdown(
                f'<div style="background:{bg};border:1px solid {bd};border-radius:8px;'
                f'padding:0.3rem 0.8rem;font-size:0.82rem;color:#c4b5fd;margin-top:0.3rem;">'
                f'🎯 {lbl}</div>',
                unsafe_allow_html=True,
            )

        # ── Skill Level ───────────────────────────────────────────────────────
        st.markdown('<div class="sec-lbl">📊 Skill Level</div>', unsafe_allow_html=True)
        saved_level = st.session_state.su_data.get("skill_level", "Beginner")
        skill_level = st.radio(
            "Skill Level", ["Beginner", "Intermediate", "Advanced"],
            horizontal=True, label_visibility="collapsed",
            index=["Beginner", "Intermediate", "Advanced"].index(saved_level),
            key="su_level",
        )

        # ── Existing Skills ───────────────────────────────────────────────────
        st.markdown('<div class="sec-lbl">🧠 Existing Skills</div>', unsafe_allow_html=True)

        all_options  = ALL_SKILLS + [s for s in st.session_state.su_custom if s not in ALL_SKILLS]
        saved_skills = st.session_state.su_data.get("skills", [])
        selected     = st.multiselect(
            "Select skills you already have",
            options=all_options,
            default=[s for s in saved_skills if s in all_options],
            label_visibility="collapsed",
            key="su_skills_ms",
        )

        # Custom skill add
        ca, cb = st.columns([3, 1])
        with ca:
            new_skill = st.text_input("", placeholder="Add a custom skill e.g. Figma, Blender",
                                      label_visibility="collapsed", key="su_new_skill")
        with cb:
            if st.button("＋ Add", key="su_add_skill", use_container_width=True):
                ns = new_skill.strip().lower()
                if ns and ns not in st.session_state.su_custom and ns not in ALL_SKILLS:
                    st.session_state.su_custom.append(ns)
                    st.rerun()

        final_skills = list(dict.fromkeys(selected + st.session_state.su_custom))
        if final_skills:
            chips = "".join(
                f'<span style="display:inline-block;background:rgba(124,58,237,0.2);color:#c4b5fd;'
                f'border:1px solid rgba(124,58,237,0.35);border-radius:999px;'
                f'padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:600;margin:0.15rem;">'
                f'{s.title()}</span>'
                for s in final_skills
            )
            st.markdown(f'<div style="margin-top:0.4rem;line-height:2;">{chips}</div>',
                        unsafe_allow_html=True)

        st.markdown("")

        # ── Navigation ────────────────────────────────────────────────────────
        b1, b2 = st.columns(2)
        with b1:
            if st.button("← Back", use_container_width=True, key="su_back2"):
                st.session_state.su_step = 1
                st.rerun()
        with b2:
            if st.button("Next → Time & Experience", use_container_width=True,
                         type="primary", key="su_next2"):
                if not target_role:
                    st.error("Please enter or select your target role.")
                else:
                    st.session_state.su_data.update({
                        "target_role": target_role,
                        "skill_level": skill_level,
                        "skills":      final_skills,
                    })
                    st.session_state.su_step = 3
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — Time & Experience
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 3:
        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">⏱️</span>
            <div class="auth-title">Time & Experience</div>
            <div class="auth-sub">We'll tailor your roadmap to fit your schedule</div>
        </div>
        """, unsafe_allow_html=True)

        # Time Availability
        st.markdown('<div class="sec-lbl">⏰ Time Available Per Week</div>', unsafe_allow_html=True)
        TIME_OPTS  = ["Less than 5 hrs", "5–10 hrs", "10+ hrs"]
        saved_time = st.session_state.su_data.get("time_availability", "5–10 hrs")
        if saved_time not in TIME_OPTS: saved_time = "5–10 hrs"
        time_avail = st.radio("Time", TIME_OPTS, horizontal=True,
                              label_visibility="collapsed",
                              index=TIME_OPTS.index(saved_time), key="su_time")
        time_hints = {
            "Less than 5 hrs": ("🐢", "Relaxed pace — 1 skill per week"),
            "5–10 hrs":        ("🚶", "Steady pace — 2–3 skills per week"),
            "10+ hrs":         ("🚀", "Fast track — full immersion"),
        }
        st.markdown(
            f'<div style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);'
            f'border-radius:8px;padding:0.35rem 0.9rem;font-size:0.82rem;color:#c4b5fd;margin:0.3rem 0 0.9rem;">'
            f'{time_hints[time_avail][0]} {time_hints[time_avail][1]}</div>',
            unsafe_allow_html=True)

        # Experience Type
        st.markdown('<div class="sec-lbl">🎓 Current Status</div>', unsafe_allow_html=True)
        EXP_OPTS  = ["Student", "Fresher", "Working Professional"]
        EXP_ICONS = {"Student": "🎓", "Fresher": "🌱", "Working Professional": "💼"}
        EXP_DESC  = {
            "Student":              "Currently studying — building skills for the future",
            "Fresher":              "Recently graduated — ready to land the first job",
            "Working Professional": "Already working — upskilling or switching roles",
        }
        saved_exp = st.session_state.su_data.get("experience_type", "Student")
        if saved_exp not in EXP_OPTS: saved_exp = "Student"
        exp_type = st.radio("Experience", EXP_OPTS, horizontal=True,
                            label_visibility="collapsed",
                            index=EXP_OPTS.index(saved_exp), key="su_exp")
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);'
            f'border-radius:8px;padding:0.35rem 0.9rem;font-size:0.82rem;'
            f'color:rgba(255,255,255,0.55);margin:0.3rem 0 1rem;">'
            f'{EXP_ICONS[exp_type]} {EXP_DESC[exp_type]}</div>',
            unsafe_allow_html=True)

        # Summary
        d = st.session_state.su_data
        st.markdown(
            f'<div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.2);'
            f'border-radius:12px;padding:0.75rem 1rem;font-size:0.8rem;'
            f'color:rgba(255,255,255,0.6);margin-bottom:1rem;line-height:1.9;">'
            f'<strong style="color:#c4b5fd;">📋 Summary</strong><br>'
            f'👤 {d.get("first_name","")} {d.get("last_name","")} &nbsp;·&nbsp; '
            f'🎯 {d.get("target_role","")} &nbsp;·&nbsp; '
            f'📊 {d.get("skill_level","")} &nbsp;·&nbsp; '
            f'🧠 {len(d.get("skills",[]))} skills</div>',
            unsafe_allow_html=True)

        # Navigation
        b1, b2 = st.columns(2)
        with b1:
            if st.button("← Back", use_container_width=True, key="su_back3"):
                st.session_state.su_step = 2
                st.rerun()
        with b2:
            if st.button("🚀 Create My Account", use_container_width=True,
                         type="primary", key="su_finish"):
                name = f"{d['first_name']} {d['last_name']}"
                ok, msg = signup(
                    name, d["email"], d["password"],
                    security_q        = d["sec_q"],
                    security_a        = d["sec_a"],
                    target_role       = d["target_role"],
                    skill_level       = d["skill_level"],
                    skills            = d.get("skills", []),
                    time_availability = time_avail,
                    experience_type   = exp_type,
                )
                if ok:
                    st.session_state.su_step   = 1
                    st.session_state.su_data   = {}
                    st.session_state.su_custom = []
                    st.session_state.su_role   = ""
                    st.success("🎉 Account created! Please login.")
                    st.switch_page("pages/1_Login.py")
                else:
                    st.error(f"❌ {msg}")
