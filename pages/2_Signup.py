import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import signup

st.set_page_config(page_title="Sign Up · SkillGap", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

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
.block-container { padding: 2rem 1rem !important; max-width: 100% !important; }

.auth-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 2rem 2.2rem 1.6rem;
    animation: slideUp 0.55s ease both;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}
.auth-icon  { font-size: 2.6rem; text-align: center; display: block; margin-bottom: 0.4rem; }
.auth-title { text-align: center; color: #fff; font-size: 1.55rem; font-weight: 800; margin-bottom: 0.2rem; }
.auth-sub   { text-align: center; color: rgba(255,255,255,0.45); font-size: 0.86rem; margin-bottom: 1.4rem; }
.sec-lbl    { color: rgba(255,255,255,0.35); font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin: 1rem 0 0.2rem; }

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
div[data-testid="stSelectbox"] label { color: rgba(255,255,255,0.65) !important; font-size: 0.85rem !important; }
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

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
.or-div {
    display: flex; align-items: center; gap: 0.8rem;
    color: rgba(255,255,255,0.25); font-size: 0.78rem;
    margin: 1rem 0;
}
.or-div::before, .or-div::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.08); }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("user"):
    st.switch_page("pages/3_Dashboard.py")

_, back_col, _ = st.columns([1, 6, 1])
with back_col:
    if st.button("← Back to Home", key="su_back"):
        st.switch_page("app.py")

_, center, _ = st.columns([1, 1.5, 1])

with center:
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
        first_name = st.text_input("First Name", placeholder="John", key="su_fname")
    with nc2:
        last_name  = st.text_input("Last Name",  placeholder="Doe",  key="su_lname")
    email = st.text_input("Email Address", placeholder="you@example.com", key="su_email")

    st.markdown('<div class="sec-lbl">🔑 Password</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        password = st.text_input("Password",         type="password", placeholder="Min 6 chars", key="su_pw")
    with c2:
        confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat",      key="su_cpw")

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
    if st.button("🚀 Create My Account", use_container_width=True, type="primary", key="su_btn"):
        name = f"{first_name.strip()} {last_name.strip()}".strip()
        if not all([first_name, last_name, email, password, confirm, sec_a]):
            st.error("Please fill in all fields.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, msg = signup(name, email, password, sec_q, sec_a)
            if ok:
                st.success("🎉 Account created! Please login.")
                st.switch_page("pages/1_Login.py")
            else:
                st.error(f"❌ {msg}")

    st.markdown('<div class="or-div">or</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.4);font-size:0.85rem;margin:0 0 0.5rem;'>Already have an account?</p>", unsafe_allow_html=True)
    if st.button("🔐 Sign In Instead", use_container_width=True, key="su_login"):
        st.switch_page("pages/1_Login.py")
