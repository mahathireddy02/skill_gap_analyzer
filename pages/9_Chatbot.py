import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from components.navbar import show_navbar
from utils.chatbot_engine import get_response

st.set_page_config(page_title="Chatbot · SkillGap", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
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
.user-msg{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;
    border-radius:16px 16px 4px 16px;padding:0.7rem 1rem;margin:0.5rem 0 0.5rem auto;
    max-width:70%;font-size:0.9rem;line-height:1.5;width:fit-content;}
.bot-msg{background:#f7f6f3;color:#1e293b;
    border-radius:16px 16px 16px 4px;padding:0.7rem 1rem;margin:0.5rem auto 0.5rem 0;
    max-width:75%;font-size:0.9rem;line-height:1.6;width:fit-content;border:1px solid #e8e6e1;}
</style>
""", unsafe_allow_html=True)

show_navbar("Chatbot")

db_user      = get_user(st.session_state.email)
user_skills  = db_user.get("skills", [])
missing      = db_user.get("missing_skills", [])
target_role  = db_user.get("target_role", "")
resume_score = db_user.get("resume_score", 0)
name         = st.session_state.user.get("name", "there").split()[0]

CHAT_CTX = {
    "name": name,
    "user_skills": user_skills,
    "missing": missing,
    "target_role": target_role,
    "resume_score": resume_score,
}

def reply(text: str) -> str:
    return get_response(text, CHAT_CTX)

st.markdown("## 🤖 SkillGap Chatbot")
st.caption("Career, skills, resumes, roadmaps, interviews, and learning — ask anything related to the app.")
st.markdown("")

if "chat_history" not in st.session_state:
    intro = f"Hey {name}! I'm your SkillGap assistant.\n\n"
    if target_role:
        intro += f"Target role: **{target_role}**. "
    if user_skills:
        intro += f"**{len(user_skills)}** skills detected, **{len(missing)}** gaps.\n\n"
    else:
        intro += "Upload your resume on **Resume Score** to get started.\n\n"
    intro += "Ask about skills, learning paths, interviews, or type **help**."
    st.session_state.chat_history = [{"role": "bot", "text": intro}]

q1, q2, q3, q4, q5 = st.columns(5)
for col, label, prompt in [
    (q1, "📋 My Skills", "my skills"),
    (q2, "❌ Missing Skills", "missing skills"),
    (q3, "📄 Resume Score", "my resume score"),
    (q4, "🛤️ My Roadmap", "my roadmap"),
    (q5, "💼 Career Tips", "career tips"),
]:
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            st.session_state.chat_history.append({"role": "bot", "text": reply(prompt)})
            st.rerun()

st.markdown("---")

for msg in st.session_state.chat_history:
    css = "user-msg" if msg["role"] == "user" else "bot-msg"
    prefix = "🧑" if msg["role"] == "user" else "🤖"
    text = msg["text"].replace("\n", "<br>")
    st.markdown(f'<div class="{css}">{prefix} {text}</div>', unsafe_allow_html=True)

st.markdown("")

with st.form("chat_form", clear_on_submit=True):
    c1, c2 = st.columns([6, 1])
    with c1:
        user_input = st.text_input(
            "",
            placeholder="e.g. how to learn react, interview tips, improve resume...",
            label_visibility="collapsed",
        )
    with c2:
        sent = st.form_submit_button("Send", use_container_width=True, type="primary")

if sent and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
    st.session_state.chat_history.append({"role": "bot", "text": reply(user_input.strip())})
    st.rerun()

if len(st.session_state.chat_history) > 3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [{
            "role": "bot",
            "text": f"Chat cleared. How can I help you, {name}?",
        }]
        st.rerun()
