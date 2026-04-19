import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import login, send_reset_email, verify_reset_token, reset_password_with_token

st.set_page_config(page_title="Login · SkillGap", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebarNav"],
[data-testid="stSidebar"], [data-testid="collapsedControl"],
section[data-testid="stSidebar"], .stDeployButton,
.st-emotion-cache-zq5wmm, .st-emotion-cache-1dp5vir,
[class*="viewerBadge"], [class*="toolbar"]
{ display: none !important; visibility: hidden !important; }

html, body { margin: 0 !important; padding: 0 !important; }
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e) !important;
    background-size: 400% 400% !important;
    animation: bgShift 10s ease infinite !important;
    min-height: 100vh !important;
}
@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.block-container {
    padding: 2rem 1rem 2rem !important;
    max-width: 100% !important;
}

/* Card */
.auth-wrap {
    max-width: 440px;
    margin: 0 auto;
    animation: slideUp 0.55s ease both;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}
.auth-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 2.2rem 2.2rem 1.8rem;
}
.auth-icon { font-size: 2.8rem; text-align: center; display: block; margin-bottom: 0.4rem; }
.auth-title { text-align: center; color: #fff; font-size: 1.6rem; font-weight: 800; margin-bottom: 0.2rem; }
.auth-sub   { text-align: center; color: rgba(255,255,255,0.45); font-size: 0.88rem; margin-bottom: 1.6rem; }

/* Inputs */
div[data-testid="stTextInput"] label { color: rgba(255,255,255,0.65) !important; font-size: 0.85rem !important; font-weight: 500 !important; }
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-size: 0.92rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.12) !important;
}

/* Buttons */
div[data-testid="stButton"] button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.3) !important;
    border: none !important;
}
div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: rgba(255,255,255,0.8) !important;
}

/* Divider */
.or-div {
    display: flex; align-items: center; gap: 0.8rem;
    color: rgba(255,255,255,0.25); font-size: 0.78rem;
    margin: 1rem 0;
}
.or-div::before, .or-div::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(255,255,255,0.08);
}

/* Alert overrides */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)

if st.session_state.get("user"):
    st.switch_page("pages/3_Dashboard.py")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# Handle reset link token from email
params = st.query_params
if "token" in params and "email" in params and st.session_state.auth_mode != "forgot2":
    st.session_state.reset_token = params["token"]
    st.session_state.reset_email = params["email"]
    st.session_state.auth_mode   = "forgot2"
    st.query_params.clear()

# Back to home
_, back_col, _ = st.columns([1, 6, 1])
with back_col:
    if st.button("← Back to Home", key="back_home"):
        st.switch_page("app.py")

# Center the card
_, center, _ = st.columns([1, 1.4, 1])

with center:

    # ══════════════════════════════════════════════════════
    # LOGIN
    # ══════════════════════════════════════════════════════
    if st.session_state.auth_mode == "login":
        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">🔐</span>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-sub">Sign in to continue your learning journey</div>
        </div>
        """, unsafe_allow_html=True)

        email    = st.text_input("Email Address", placeholder="you@example.com", key="li_email")
        password = st.text_input("Password", type="password", placeholder="Your password", key="li_pw")

        fp_col, _ = st.columns([1, 2])
        with fp_col:
            if st.button("Forgot password?", key="go_forgot"):
                st.session_state.auth_mode = "forgot1"
                st.rerun()

        if st.button("🚀 Sign In", use_container_width=True, type="primary", key="li_btn"):
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                ok, result = login(email, password)
                if ok:
                    st.session_state.user  = result
                    st.session_state.email = email
                    st.switch_page("pages/3_Dashboard.py")
                else:
                    st.error(f"❌ {result}")

        st.markdown('<div class="or-div">or</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.4);font-size:0.85rem;margin:0 0 0.5rem;'>Don't have an account?</p>", unsafe_allow_html=True)
        if st.button("✨ Create Free Account", use_container_width=True, key="go_signup"):
            st.switch_page("pages/2_Signup.py")

    # ══════════════════════════════════════════════════════
    # FORGOT — Step 1: enter email, send reset link
    # ══════════════════════════════════════════════════════
    elif st.session_state.auth_mode == "forgot1":
        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">🔑</span>
            <div class="auth-title">Forgot Password?</div>
            <div class="auth-sub">Enter your email and we'll send you a reset link</div>
        </div>
        """, unsafe_allow_html=True)

        fe = st.text_input("Email Address", placeholder="you@example.com", key="fp_email")

        if st.button("Send Reset Link →", use_container_width=True, type="primary", key="fp_send"):
            if not fe:
                st.error("Please enter your email.")
            else:
                ok, result = send_reset_email(fe.strip().lower())
                if not ok:
                    st.error(f"❌ {result}")
                elif result.startswith("DEV_LINK:"):
                    # Dev mode: no SMTP configured, show link directly
                    link = result.replace("DEV_LINK:", "")
                    st.success("✅ Reset link generated (dev mode — no SMTP configured):")
                    st.code(link)
                    st.info("💡 To enable real emails, set SMTP_EMAIL and SMTP_PASSWORD environment variables.")
                else:
                    st.success(f"✅ Reset link sent to **{fe}**. Check your inbox!")

        if st.button("← Back to Login", key="fp_back1"):
            st.session_state.auth_mode = "login"
            st.rerun()

    # ══════════════════════════════════════════════════════
    # RESET — arrived via token link (?token=...&email=...)
    # ══════════════════════════════════════════════════════
    elif st.session_state.auth_mode == "forgot2":
        token = st.session_state.get("reset_token", "")
        email = st.session_state.get("reset_email", "")

        st.markdown("""
        <div class="auth-card">
            <span class="auth-icon">🔒</span>
            <div class="auth-title">Set New Password</div>
            <div class="auth-sub">Choose a strong new password</div>
        </div>
        """, unsafe_allow_html=True)

        new_pw = st.text_input("New Password",     type="password", placeholder="Min 6 characters", key="fp_npw")
        cnf_pw = st.text_input("Confirm Password", type="password", placeholder="Repeat password",  key="fp_cpw")

        if st.button("🔄 Reset Password", use_container_width=True, type="primary", key="fp_reset"):
            if not new_pw or not cnf_pw:
                st.error("Please fill in both fields.")
            elif len(new_pw) < 6:
                st.error("Password must be at least 6 characters.")
            elif new_pw != cnf_pw:
                st.error("Passwords do not match.")
            else:
                ok, msg = reset_password_with_token(email, token, new_pw)
                if ok:
                    st.success("✅ Password reset! You can now login.")
                    for k in ["reset_token", "reset_email"]:
                        st.session_state.pop(k, None)
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        if st.button("← Back", key="fp_back2"):
            st.session_state.auth_mode = "login"
            st.rerun()
