import streamlit as st

def show_navbar(active="Dashboard"):
    name    = st.session_state.get("user", {}).get("name", "User")
    first   = name.split()[0]

    # ── Apply saved theme ─────────────────────────────────────────────────────
    if st.session_state.get("email"):
        import sys, os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from utils.auth import get_user as _get_user
        _u = _get_user(st.session_state.email) or {}
        _theme = _u.get("theme", "dark")
    else:
        _theme = "dark"

    if _theme == "light":
        _theme_css = """
        html,body,.stApp{background:#f5f4ff!important;color:#1a1a2e!important;}
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        label,.stTextInput label,.stSelectbox label,
        .stRadio label,.stCheckbox label,
        p,h1,h2,h3,h4,span
        {color:#1a1a2e!important;}
        div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea
        {background:#fff!important;color:#1a1a2e!important;border-color:#d1d5db!important;}
        div[data-testid="stMetric"]{background:#fff!important;border:1px solid #e5e7eb!important;}
        div[data-testid="stMetricLabel"]{color:#6b7280!important;}
        div[data-testid="stMetricValue"]{color:#1a1a2e!important;}
        div[data-testid="stExpander"]{background:#fff!important;border-color:#e5e7eb!important;}
        div[data-testid="stExpander"] summary p{color:#1a1a2e!important;}
        .stTabs [data-baseweb="tab-list"]{background:#ede9fe!important;border-radius:12px;}
        .stTabs [data-baseweb="tab"]{color:#4b5563!important;}
        .stTabs [aria-selected="true"]{background:#7c3aed!important;color:#fff!important;border-radius:10px;}
        .stat-card,.feat-card{background:#fff!important;border-color:#e5e7eb!important;}
        .fct{color:#1a1a2e!important;} .fcd{color:#4b5563!important;}
        """
        _nav_btn_color = "rgba(30,27,75,0.85)"
        _nav_btn_hover_bg = "rgba(124,58,237,0.12)"
        _nav_bg = "#ede9fe"
        _nav_border = "#c4b5fd"
    else:
        _theme_css = """
        html,body,.stApp{background:linear-gradient(-45deg,#0f0c29,#1a1a2e,#0f0c29)!important;color:#fff!important;}
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        label{color:rgba(255,255,255,0.85)!important;}
        div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea
        {background:rgba(255,255,255,0.07)!important;color:#fff!important;border-color:rgba(255,255,255,0.15)!important;}
        div[data-testid="stExpander"]{background:rgba(255,255,255,0.04)!important;border-color:rgba(255,255,255,0.1)!important;}
        .stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,0.06)!important;border-radius:12px;}
        .stTabs [data-baseweb="tab"]{color:rgba(255,255,255,0.6)!important;}
        .stTabs [aria-selected="true"]{background:#7c3aed!important;color:#fff!important;border-radius:10px;}
        div[data-testid="stMetric"]{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.08)!important;}
        div[data-testid="stMetricLabel"]{color:rgba(255,255,255,0.5)!important;}
        div[data-testid="stMetricValue"]{color:#fff!important;}
        """
        _nav_btn_color = "rgba(255,255,255,0.65)"
        _nav_btn_hover_bg = "rgba(255,255,255,0.08)"
        _nav_bg = "#0d0b1e"
        _nav_border = "rgba(255,255,255,0.08)"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],[data-testid="stSidebarNav"],[data-testid="stSidebar"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"],.stDeployButton,
[class*="viewerBadge"],[class*="toolbar"]{{display:none!important;visibility:hidden!important;}}
html,body{{margin:0!important;padding:0!important;font-family:'Inter',sans-serif!important;}}
.block-container{{padding:0!important;margin:0!important;max-width:100%!important;}}
div[data-testid="stAppViewContainer"]>section{{padding-top:0!important;}}
{_theme_css}
div[data-testid="stHorizontalBlock"]:first-of-type{{
    background:{_nav_bg};
    border-bottom:1px solid {_nav_border};
    padding:0.45rem 1.2rem!important;
    margin:0!important;
    align-items:center!important;
    gap:0.2rem!important;
    position:sticky;top:0;z-index:9999;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{{
    background:transparent!important;
    border:1px solid transparent!important;
    color:{_nav_btn_color}!important;
    font-size:0.8rem!important;
    font-weight:500!important;
    padding:0.28rem 0.4rem!important;
    border-radius:8px!important;
    white-space:nowrap!important;
    height:auto!important;
    min-height:unset!important;
    line-height:1.4!important;
    box-shadow:none!important;
    transition:all 0.15s!important;
    width:100%!important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{{
    background:{_nav_btn_hover_bg}!important;
    color:{'#1a1a2e' if _theme == 'light' else '#fff'}!important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button[kind="primary"]{{
    background:rgba(124,58,237,0.18)!important;
    color:#7c3aed!important;
    border-color:rgba(124,58,237,0.4)!important;
    font-weight:700!important;
}}
.page-body{{padding:1.6rem 2rem 2rem;}}
</style>
""", unsafe_allow_html=True)

    nav_items = [
        ("🏠 Home",      "Dashboard",       "pages/3_Dashboard.py"),
        ("📄 Resume",    "Resume Score",    "pages/4_Resume_Score.py"),
        ("🧠 Skill Gap", "Skill Gap",       "pages/5_Skill_Gap.py"),
        ("🛤️ Roadmap",   "Roadmap",         "pages/6_Roadmap.py"),
        ("📊 Analytics", "Analytics",       "pages/7_Analytics.py"),
        ("📝 Builder",   "Resume Builder",  "pages/10_Resume_Builder.py"),
        ("🤖 Chatbot",   "Chatbot",         "pages/9_Chatbot.py"),
    ]

    # logo(1.2) + 7 nav(1.0 each) + spacer(0.5) + profile(1.0) + logout(0.5)
    cols = st.columns([1.2, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 0.5])

    with cols[0]:
        st.markdown(
            '<p style="color:#fff;font-size:1.05rem;font-weight:800;margin:0;'
            'padding:0.3rem 0.4rem;white-space:nowrap;">🎓 Skill'
            '<span style="color:#a78bfa;">Gap</span></p>',
            unsafe_allow_html=True
        )

    for i, (label, key, path) in enumerate(nav_items):
        with cols[i + 1]:
            is_active = active.lower() == key.lower()
            if st.button(label, key=f"nb_{key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.switch_page(path)

    # cols[6] = spacer, leave empty

    with cols[9]:
        if st.button(f"👤 {first}", key="nb_profile", use_container_width=True):
            st.switch_page("pages/8_Profile.py")

    with cols[10]:
        if st.button("🚪", key="nb_logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
