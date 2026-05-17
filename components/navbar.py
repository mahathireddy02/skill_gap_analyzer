import streamlit as st
from components.theme import BG_LIGHT, BG_STATIC, COLOR_BG_DARK, COLOR_BG_LIGHT, COLOR_NAV_DARK, COLOR_SURFACE_LIGHT

def show_navbar(active="Dashboard"):
    name  = st.session_state.get("user", {}).get("name", "User")
    first = name.split()[0]

    # ── Load theme ────────────────────────────────────────────────────────────
    if st.session_state.get("email"):
        import sys, os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from utils.auth import get_user as _gu, update_user as _upd
        _u     = _gu(st.session_state.email) or {}
        _theme = _u.get("theme", "dark")
    else:
        _theme = "dark"

    # ── Handle toggle click BEFORE rendering ──────────────────────────────────
    st.session_state.pop("_do_theme_toggle", False)
    _just_changed = st.session_state.pop("_theme_just_changed", False)

    # ── Theme colours ─────────────────────────────────────────────────────────
    if _theme == "light":
        _bg          = COLOR_BG_LIGHT
        _nav_bg      = COLOR_SURFACE_LIGHT
        _nav_border  = "#cbd5e1"
        _btn_color   = "rgba(30,27,75,0.85)"
        _btn_hover   = "rgba(124,58,237,0.12)"
        _text_color  = "#1a1a2e"
        _theme_css   = (
        """
        html,body,.stApp{background:""" + BG_LIGHT + """!important;color:#1a1a2e!important;}

        /* All text elements */
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stMarkdownContainer"] a,
        div[data-testid="stMarkdownContainer"] strong,
        div[data-testid="stMarkdownContainer"] em,
        label, .stTextInput label, .stSelectbox label,
        .stRadio label, .stCheckbox label,
        .stSlider label, .stNumberInput label,
        .stTextArea label, .stDateInput label,
        p, h1, h2, h3, h4, h5, span, li, a, strong
        {color:#1a1a2e!important;}

        /* Caption and helper text */
        div[data-testid="stCaptionContainer"] p,
        small, .caption {color:#4b5563!important;}

        /* Inputs */
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input
        {background:#fff!important;color:#1a1a2e!important;border-color:#d1d5db!important;}

        /* Select boxes */
        div[data-testid="stSelectbox"] > div > div
        {background:#fff!important;color:#1a1a2e!important;border-color:#d1d5db!important;}

        /* Metrics */
        div[data-testid="stMetric"]{background:#fff!important;border:1px solid #e5e7eb!important;border-radius:12px;}
        div[data-testid="stMetricLabel"] p{color:#6b7280!important;}
        div[data-testid="stMetricValue"]{color:#1a1a2e!important;}
        div[data-testid="stMetricDelta"]{color:#059669!important;}

        /* Expanders */
        div[data-testid="stExpander"]{background:#fff!important;border-color:#e5e7eb!important;}
        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary span{color:#1a1a2e!important;}
        div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p{color:#374151!important;}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"]{background:#ede9fe!important;border-radius:12px;}
        .stTabs [data-baseweb="tab"]{color:#4b5563!important;}
        .stTabs [aria-selected="true"]{background:#7c3aed!important;color:#fff!important;border-radius:10px;}
        .stTabs [data-baseweb="tab-panel"]{background:transparent!important;}

        /* Cards */
        .stat-card{background:#fff!important;border-color:#e5e7eb!important;}
        .sc-val{color:#1a1a2e!important;}
        .sc-lbl{color:#6b7280!important;}
        .feat-card,.fc-wrap{background:#fff!important;border-color:#e5e7eb!important;}
        .fct{color:#1a1a2e!important;}
        .fcd{color:#4b5563!important;}
        .fcb{background:rgba(124,58,237,0.1)!important;color:#7c3aed!important;}

        /* Force all inline white text inside cards to dark */
        .fc-wrap div, .fc-wrap p, .fc-wrap span,
        .feat-card div, .feat-card p, .feat-card span,
        .stat-card div, .stat-card p, .stat-card span
        {color:#1a1a2e!important;}
        .fc-wrap div[style*="rgba(255,255,255,0.55)"],
        .fc-wrap div[style*="color:#fff"],
        .feat-card div[style*="color:#fff"]
        {color:#4b5563!important;}

        /* Section titles and headings in page body */
        .page-body h1,.page-body h2,.page-body h3,
        .page-body p,.page-body span,.page-body div
        {color:#1a1a2e!important;}
        .sec-title{color:#1a1a2e!important;}

        /* Skill chips */
        .chip-g{background:#d1fae5!important;color:#065f46!important;border-color:#6ee7b7!important;}
        .chip-r{background:#fee2e2!important;color:#991b1b!important;border-color:#fca5a5!important;}

        /* Progress / Skills boxes */
        .progress-box{background:#fff!important;border-color:#e5e7eb!important;}
        .box-title{color:#1a1a2e!important;}
        .empty-msg{color:#6b7280!important;}
        .ats-box{background:#fff!important;border-color:#e5e7eb!important;}
        .ats-label{color:#1a1a2e!important;}
        .prog-bg{background:#e5e7eb!important;}

        /* Alerts / info boxes */
        div[data-testid="stAlert"]{background:#fff!important;color:#1a1a2e!important;}
        div[data-testid="stAlert"] p{color:#1a1a2e!important;}

        /* Checkboxes and toggles */
        div[data-testid="stCheckbox"] span{color:#1a1a2e!important;}
        div[data-testid="stToggle"] span{color:#1a1a2e!important;}

        /* Sidebar / page body */
        .page-body{background:""" + COLOR_BG_LIGHT + """!important;}

        /* Progress bars */
        .prog-bg{background:#e5e7eb!important;}

        /* Roadmap SVG background */
        body{background:""" + COLOR_BG_LIGHT + """!important;}
        """
        )
    else:
        _bg          = COLOR_BG_DARK
        _nav_bg      = COLOR_NAV_DARK
        _nav_border  = "rgba(255,255,255,0.08)"
        _btn_color   = "rgba(255,255,255,0.65)"
        _btn_hover   = "rgba(255,255,255,0.08)"
        _text_color  = "#ffffff"
        _theme_css   = (
        """
        html,body,.stApp{background:""" + BG_STATIC + """!important;color:#fff!important;}
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
        )

    # ── Bottom-to-top reveal animation (only fires right after toggle) ────────
    _anim_css = ""
    if _just_changed:
        _anim_css = """
        @keyframes wipeDiag {
            0%   { clip-path: circle(0% at 100% 0%); }
            100% { clip-path: circle(150% at 100% 0%); }
        }
        .stApp {
            animation: wipeDiag 0.7s cubic-bezier(0.25,0.1,0.25,1) forwards !important;
        }
        """

    # ── Inject all CSS ────────────────────────────────────────────────────────
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
{_anim_css}

/* ── Navbar row ── */
div[data-testid="stHorizontalBlock"]:first-of-type{{
    background:{_nav_bg};
    border-bottom:1px solid {_nav_border};
    padding:0.3rem 1.2rem!important;
    margin:0!important;
    align-items:center!important;
    gap:0.15rem!important;
    position:sticky;top:0;z-index:9999;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{{
    background:transparent!important;
    border:1px solid transparent!important;
    color:{_btn_color}!important;
    font-size:0.78rem!important;
    font-weight:500!important;
    padding:0.22rem 0.35rem!important;
    border-radius:8px!important;
    white-space:nowrap!important;
    height:auto!important;min-height:unset!important;
    line-height:1.3!important;box-shadow:none!important;
    transition:all 0.15s!important;width:100%!important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{{
    background:{_btn_hover}!important;
    color:{_text_color}!important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button[kind="primary"]{{
    background:rgba(124,58,237,0.18)!important;
    color:#7c3aed!important;
    border-color:rgba(124,58,237,0.4)!important;
    font-weight:700!important;
}}

/* ── Profile+theme mini block ── */
.profile-block{{
    display:flex;flex-direction:column;align-items:flex-end;gap:1px;
    padding:0.1rem 0;
}}
.theme-sub-btn{{
    background:none;border:none;cursor:pointer;
    font-size:0.68rem;color:{_btn_color};
    font-family:'Inter',sans-serif;
    padding:0 0.35rem;opacity:0.65;
    transition:opacity 0.15s;line-height:1.4;
    text-align:right;width:100%;
}}
.theme-sub-btn:hover{{opacity:1;}}

.page-body{{padding:1.6rem 2rem 2rem;}}
</style>
""", unsafe_allow_html=True)

    # ── Nav items ─────────────────────────────────────────────────────────────
    nav_items = [
        ("🏠 Home",      "Dashboard",      "pages/3_Dashboard.py"),
        ("📄 Resume",    "Resume Score",   "pages/4_Resume_Score.py"),
        ("🧠 Skill Gap", "Skill Gap",      "pages/5_Skill_Gap.py"),
        ("🛤️ Roadmap",   "Roadmap",        "pages/6_Roadmap.py"),
        ("📊 Analytics", "Analytics",      "pages/7_Analytics.py"),
        ("📝 Builder",   "Resume Builder", "pages/10_Resume_Builder.py"),
        ("🤖 Chatbot",   "Chatbot",        "pages/9_Chatbot.py"),
    ]

    # logo + 7 nav + spacer + theme + profile
    cols = st.columns([1.2, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.3, 0.5, 1.0])

    with cols[0]:
        st.markdown(
            f'<p style="color:{_text_color};font-size:1.05rem;font-weight:800;margin:0;'
            f'padding:0.3rem 0.4rem;white-space:nowrap;">🎓 Skill'
            f'<span style="color:#a78bfa;">Gap</span></p>',
            unsafe_allow_html=True
        )

    for i, (label, key, path) in enumerate(nav_items):
        with cols[i + 1]:
            is_active = active.lower() == key.lower()
            if st.button(label, key=f"nb_{key}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.switch_page(path)

    with cols[9]:
        _icon = "☀️" if _theme == "dark" else "🌙"
        if st.button(_icon, key="nb_theme", use_container_width=True):
            _new = "light" if _theme == "dark" else "dark"
            _upd(st.session_state.email, {"theme": _new})
            st.session_state["_theme_just_changed"] = True
            st.rerun()

    with cols[10]:
        if st.button(f"👤 {first}", key="nb_profile", use_container_width=True):
            st.switch_page("pages/8_Profile.py")

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
