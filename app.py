import streamlit as st
from components.theme import BG_ANIMATED

st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebarNav"],
[data-testid="stSidebar"], [data-testid="collapsedControl"],
section[data-testid="stSidebar"], .stDeployButton,
[class*="viewerBadge"], [class*="toolbar"] {
    display: none !important; visibility: hidden !important;
}

html, body, .stApp {
    margin: 0 !important; padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background: """ + BG_ANIMATED + """ !important;
    background-size: 100% 100%, 100% 100%, 400% 400% !important;
    animation: bgShift 14s ease infinite !important;
    min-height: 100vh !important;
}
@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.block-container {
    padding: 0 !important; margin: 0 !important;
    max-width: 100% !important; min-width: 100% !important;
}
.stApp > div:first-child { padding-top: 0 !important; }
div[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="stVerticalBlock"] > div { display:flex; flex-direction:column; align-items:center; }
div[data-testid="stMarkdownContainer"] { width:100%; text-align:center; }

/* Particles */
.particles { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; overflow:hidden; }
.p { position:absolute; border-radius:50%; background:rgba(56,189,248,0.07); animation:rise linear infinite; }
@keyframes rise {
    0%   { transform:translateY(110vh) scale(0); opacity:0; }
    5%   { opacity:1; }
    95%  { opacity:0.5; }
    100% { transform:translateY(-10vh) scale(1.2); opacity:0; }
}

/* Landing nav */
.lnav {
    display:flex; align-items:center; justify-content:space-between;
    padding:1rem 3rem;
    background:rgba(255,255,255,0.03);
    backdrop-filter:blur(16px);
    border-bottom:1px solid rgba(255,255,255,0.06);
    position:relative; z-index:100;
}
.lnav-logo { font-size:1.25rem; font-weight:800; color:#fff; }
.lnav-logo em { color:#a78bfa; font-style:normal; }
.lnav-tag {
    font-size:0.78rem; color:rgba(255,255,255,0.4);
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    padding:0.25rem 0.75rem; border-radius:999px;
}

/* Hero — everything centered */
.hero {
    text-align:center;
    padding:4.5rem 2rem 1.5rem;
    position:relative; z-index:5;
    animation:fadeUp 0.8s ease both;
    width:100%;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(32px); }
    to   { opacity:1; transform:translateY(0); }
}
.hero-badge {
    display:inline-flex; align-items:center; gap:0.4rem;
    background:rgba(167,139,250,0.1);
    border:1px solid rgba(167,139,250,0.3);
    color:#c4b5fd; padding:0.3rem 1rem;
    border-radius:999px; font-size:0.8rem; font-weight:600;
    margin-bottom:1.5rem;
    animation:glow 2.5s ease-in-out infinite;
}
@keyframes glow {
    0%,100% { box-shadow:0 0 0 0 rgba(167,139,250,0.25); }
    50%      { box-shadow:0 0 0 6px rgba(167,139,250,0); }
}
.hero-icon {
    font-size:5rem; display:block;
    margin:0 auto 0.8rem;
    animation:bob 2.4s ease-in-out infinite;
}
@keyframes bob {
    0%,100% { transform:translateY(0); }
    50%      { transform:translateY(-14px); }
}
.hero-h1 {
    font-size:clamp(2.8rem,5.5vw,4.4rem);
    font-weight:900; color:#fff;
    line-height:1.08; margin:0 0 1rem;
    letter-spacing:-2px;
}
.hero-h1 span {
    background:linear-gradient(135deg,#a78bfa 0%,#60a5fa 50%,#34d399 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero-sub {
    font-size:1.1rem; color:rgba(255,255,255,0.58);
    line-height:1.75;
    width:100%; max-width:560px;
    margin:0 auto 2rem;
    display:block; text-align:center;
}

/* CTA buttons row */
.cta-wrap {
    display:flex; justify-content:center; align-items:center;
    gap:1rem; flex-wrap:wrap;
    padding:0 0 0.5rem;
    position:relative; z-index:5;
}

/* Streamlit button styling */
div[data-testid="stButton"] button {
    font-family:'Inter',sans-serif !important;
    font-weight:700 !important; font-size:0.95rem !important;
    border-radius:12px !important; padding:0.65rem 1.8rem !important;
    transition:all 0.25s ease !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background:linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    box-shadow:0 4px 18px rgba(124,58,237,0.35) !important;
    border:none !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 28px rgba(124,58,237,0.5) !important;
}
div[data-testid="stButton"] button[kind="secondary"] {
    background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.18) !important;
    color:white !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    background:rgba(255,255,255,0.14) !important;
    transform:translateY(-2px) !important;
}

/* Force button columns to center */
div[data-testid="stHorizontalBlock"] {
    justify-content:center !important;
    gap:1rem !important;
}

/* Stats */
.stats {
    display:flex; align-items:center; justify-content:center;
    gap:0; flex-wrap:wrap;
    padding:2rem 0 3.5rem;
    position:relative; z-index:5;
}
.stat { text-align:center; padding:0 2.5rem; }
.stat-n {
    font-size:2rem; font-weight:800;
    background:linear-gradient(135deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height:1;
}
.stat-l { font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:0.2rem; }
.stat-div { width:1px; height:40px; background:rgba(255,255,255,0.1); }

/* Features */
.feats { max-width:1400px; margin:0 auto; padding:0 2rem 4rem; position:relative; z-index:5; }
.feats-h { text-align:center; color:#fff; font-size:1.75rem; font-weight:800; margin-bottom:1.8rem; }
.feats-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:1.1rem; }
.fc {
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px; padding:1.8rem 1.4rem;
    text-align:center; transition:all 0.3s ease; backdrop-filter:blur(12px);
}
.fc:hover {
    background:rgba(255,255,255,0.08); transform:translateY(-7px);
    border-color:rgba(167,139,250,0.35);
    box-shadow:0 16px 40px rgba(124,58,237,0.15);
}
.fc-i { font-size:2.8rem; margin-bottom:0.8rem; display:block; }
.fc-t { color:#fff; font-size:0.98rem; font-weight:700; margin-bottom:0.4rem; }
.fc-d { color:rgba(255,255,255,0.48); font-size:0.82rem; line-height:1.55; }

/* Steps */
.steps { max-width:880px; margin:0 auto; padding:0 2rem 5rem; text-align:center; position:relative; z-index:5; }
.steps-h { color:#fff; font-size:1.75rem; font-weight:800; margin-bottom:1.8rem; }
.steps-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1.2rem; }
.step { color:#fff; }
.step-n {
    width:44px; height:44px;
    background:linear-gradient(135deg,#7c3aed,#4f46e5);
    border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-weight:800; font-size:1rem; margin:0 auto 0.7rem;
}
.step-i { font-size:1.8rem; margin-bottom:0.4rem; }
.step-l { font-size:0.86rem; color:rgba(255,255,255,0.6); }

/* Footer */
.lfoot {
    text-align:center; color:rgba(255,255,255,0.25);
    font-size:0.82rem; padding:1.5rem 2rem;
    border-top:1px solid rgba(255,255,255,0.05);
    position:relative; z-index:5;
}

/* Premium strict palette override */
html,body,.stApp{color:#FFFFF0!important;}
.p{background:rgba(255,255,240,0.07)!important;}
.lnav,.fc{background:rgba(0,0,0,0.24)!important;border-color:rgba(255,255,240,0.12)!important;}
.lnav-logo,.hero-h1,.feats-h,.steps-h,.step,.fc-t{color:#FFFFF0!important;}
.lnav-logo em,.hero-badge,.stat-n,.step-n{color:#FFFFF0!important;background:linear-gradient(180deg,#333F63,#000000D6)!important;-webkit-text-fill-color:#FFFFF0!important;}
.lnav-tag,.hero-sub,.stat-l,.fc-d,.step-l,.lfoot{color:rgba(255,255,240,0.62)!important;}
.hero-h1 span,.stat-n{background:linear-gradient(135deg,#FFFFF0,rgba(255,255,240,0.62))!important;-webkit-background-clip:text!important;background-clip:text!important;-webkit-text-fill-color:transparent!important;}
.hero-badge{border-color:rgba(255,255,240,0.18)!important;box-shadow:0 0 28px rgba(0,0,0,0.24)!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(180deg,#333F63,#000000D6)!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.18)!important;box-shadow:0 14px 32px rgba(0,0,0,0.32)!important;}
div[data-testid="stButton"] button[kind="secondary"]{background:rgba(0,0,0,0.24)!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.16)!important;}
.fc:hover{background:rgba(51,63,99,0.62)!important;border-color:rgba(255,255,240,0.28)!important;box-shadow:0 18px 44px rgba(0,0,0,0.34),0 0 24px rgba(255,255,240,0.08)!important;}
.stat-div,.lfoot{border-color:rgba(255,255,240,0.10)!important;}

/* Responsive landing */
@media (max-width: 1100px) {
    .feats-grid { grid-template-columns:repeat(3, minmax(0, 1fr)); }
    .steps-grid { grid-template-columns:repeat(2, minmax(0, 1fr)); }
    .lnav { padding:0.85rem 1.5rem; }
}
@media (max-width: 760px) {
    .lnav {
        padding:0.75rem 1rem;
        gap:0.75rem;
        flex-wrap:wrap;
        justify-content:center;
    }
    .lnav-logo { width:100%; text-align:center; }
    .hero {
        padding:3rem 1rem 1rem;
    }
    .hero-icon { font-size:3.6rem; }
    .hero-h1 {
        font-size:2.55rem;
        letter-spacing:0;
    }
    .hero-sub {
        font-size:0.98rem;
        line-height:1.6;
        max-width:32rem;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-wrap:wrap!important;
        gap:0.75rem!important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width:100%!important;
        min-width:100%!important;
        flex:1 1 100%!important;
    }
    div[data-testid="stButton"] button {
        width:100%!important;
        min-height:2.65rem!important;
        white-space:normal!important;
    }
    .stats {
        display:grid;
        grid-template-columns:repeat(2, minmax(0, 1fr));
        gap:1rem;
        padding:1.5rem 1rem 2.5rem;
    }
    .stat { padding:0.9rem 0.5rem; }
    .stat-div { display:none; }
    .feats { padding:0 1rem 3rem; }
    .feats-grid { grid-template-columns:1fr; }
    .fc { padding:1.25rem 1rem; border-radius:14px; }
    .fc-i { font-size:2.25rem; }
    .steps { padding:0 1rem 3rem; }
    .steps-grid { grid-template-columns:1fr; }
}
@media (max-width: 420px) {
    .hero-h1 { font-size:2.05rem; }
    .hero-badge { font-size:0.72rem; padding:0.28rem 0.75rem; }
    .stats { grid-template-columns:1fr; }
    .feats-h,.steps-h { font-size:1.35rem; }
}
</style>

<!-- Particles -->
<div class="particles">
  <div class="p" style="width:7px;height:7px;left:7%;animation-duration:14s;animation-delay:0s;"></div>
  <div class="p" style="width:4px;height:4px;left:20%;animation-duration:10s;animation-delay:2s;"></div>
  <div class="p" style="width:10px;height:10px;left:35%;animation-duration:17s;animation-delay:1s;"></div>
  <div class="p" style="width:5px;height:5px;left:52%;animation-duration:12s;animation-delay:3.5s;"></div>
  <div class="p" style="width:8px;height:8px;left:67%;animation-duration:15s;animation-delay:0.5s;"></div>
  <div class="p" style="width:3px;height:3px;left:80%;animation-duration:11s;animation-delay:4s;"></div>
  <div class="p" style="width:6px;height:6px;left:13%;animation-duration:16s;animation-delay:2.5s;"></div>
  <div class="p" style="width:9px;height:9px;left:58%;animation-duration:9s;animation-delay:1.5s;"></div>
  <div class="p" style="width:4px;height:4px;left:88%;animation-duration:18s;animation-delay:3s;"></div>
  <div class="p" style="width:7px;height:7px;left:42%;animation-duration:13s;animation-delay:5s;"></div>
</div>

<!-- Hero -->
<div class="hero">
    <div class="hero-badge">✨ AI-Powered Career Intelligence</div>
    <span class="hero-icon">🎓</span>
    <h1 class="hero-h1">Bridge Your <span>Skill Gap</span></h1>
    <p class="hero-sub">
        Upload your resume, discover exactly what skills you're missing,
        and get a personalized step-by-step roadmap to land your dream tech job.
    </p>
</div>
""", unsafe_allow_html=True)

# ── CTA Buttons ──────────────────────────────────────────
_, c1, c2, _ = st.columns([2.5, 1.4, 0.8, 2.5])
with c1:
    if st.button("🚀 Get Started — Free", use_container_width=True, type="primary", key="cta_signup"):
        st.switch_page("pages/2_Signup.py")
with c2:
    if st.button("🔐 Login", use_container_width=True, key="cta_login"):
        st.switch_page("pages/1_Login.py")

# ── Rest of page (pure HTML) ──────────────────────────────
st.markdown("""
<div class="stats">
    <div class="stat"><div class="stat-n">500+</div><div class="stat-l">Students</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-n">20+</div><div class="stat-l">Job Roles</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-n">100+</div><div class="stat-l">Skills Tracked</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-n">4.9★</div><div class="stat-l">Rating</div></div>
</div>

<div class="feats">
    <div class="feats-h">Everything You Need to Get Hired </div>
    <div class="feats-grid">
        <div class="fc"><span class="fc-i">📄</span><div class="fc-t">Resume Scorer</div><div class="fc-d">ATS-based scoring with keyword analysis and actionable improvement tips.</div></div>
        <div class="fc"><span class="fc-i">🧠</span><div class="fc-t">Skill Gap Analysis</div><div class="fc-d">Compare your skills against 10+ top tech roles and find exactly what's missing.</div></div>
        <div class="fc"><span class="fc-i">🛤️</span><div class="fc-t">Learning Roadmap</div><div class="fc-d">Beginner → Intermediate → Advanced plans for every missing skill.</div></div>
        <div class="fc"><span class="fc-i">📊</span><div class="fc-t">Progress Analytics</div><div class="fc-d">Visual charts to track your skill growth and readiness over time.</div></div>
        <div class="fc"><span class="fc-i">📝</span><div class="fc-t">Resume Builder</div><div class="fc-d">Create professional ATS-friendly resumes with 4 beautiful templates in minutes.</div></div>
    </div>
</div>

<div class="steps">
    <div class="steps-h">How It Works</div>
    <div class="steps-grid">
        <div class="step"><div class="step-n">1</div><div class="step-i">📝</div><div class="step-l">Create your free account</div></div>
        <div class="step"><div class="step-n">2</div><div class="step-i">📄</div><div class="step-l">Upload your resume</div></div>
        <div class="step"><div class="step-n">3</div><div class="step-i">🧠</div><div class="step-l">Analyze your skill gaps</div></div>
        <div class="step"><div class="step-n">4</div><div class="step-i">🚀</div><div class="step-l">Follow your roadmap</div></div>
    </div>
</div>

<div class="lfoot">
    © 2025 SkillGap Analyzer  
</div>
""", unsafe_allow_html=True)
