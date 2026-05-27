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
        _nav_border  = "#bbab8c"
        _btn_color   = "#000000"
        _btn_hover   = "#bbab8c"
        _text_color  = "#000000"
        _active_bg   = "#bbab8c"
        _active_text = "#000000"
        _active_border = "#bbab8c"
        _page_gradient_bg = "#fdf7e4"
        _page_card_bg = "#fdf7e4"
        _page_chip_bg = "#bbab8c"
        _brand_gap_color = "#bbab8c"
        _theme_css   = (
        """
        html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"],
        .main,.block-container{background:""" + BG_LIGHT + """!important;color:#000000!important;}

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
        {color:#000000!important;}

        /* Caption and helper text */
        div[data-testid="stCaptionContainer"] p,
        small, .caption {color:#000000!important;}

        /* Inputs */
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] > div > div,
        div[data-testid="stMultiSelect"] > div > div
        {background:#fdf7e4!important;color:#000000!important;border-color:#bbab8c!important;}

        /* Chat elements */
        div[data-testid="stChatMessage"] {background:#fdf7e4!important;border:1px solid #bbab8c!important;}
        div[data-testid="stChatInput"] textarea {background:#fdf7e4!important;color:#000000!important;}

        /* Metrics */
        div[data-testid="stMetric"]{background:#fdf7e4!important;border:1px solid #bbab8c!important;border-radius:12px;}
        div[data-testid="stMetricLabel"] p{color:#000000!important;}
        div[data-testid="stMetricValue"]{color:#000000!important;}
        div[data-testid="stMetricDelta"]{color:#000000!important;}

        /* Expanders */
        div[data-testid="stExpander"]{background:#fdf7e4!important;border-color:#bbab8c!important;}
        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary span{color:#000000!important;}
        div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p{color:#000000!important;}

        /* Roadmap Page Specific Overrides */
        /* SVG Journey Map */
        #journey-svg .track-bg{stroke:#bbab8c!important;}
        #journey-svg .track-rail{stroke:#bbab8c!important;}
        #journey-svg .station-done .s-circle{fill:#fdf7e4!important;stroke:#bbab8c!important;}
        #journey-svg .station-active .s-circle{fill:#fdf7e4!important;stroke:#bbab8c!important;}
        #journey-svg .station-upcoming .s-circle{fill:#fdf7e4!important;stroke:#bbab8c!important;}
        #journey-svg .s-icon{fill:#000000!important;}
        #journey-svg .station-upcoming .s-icon{fill:#000000!important;}
        #journey-svg .s-label{fill:#000000!important;}
        #journey-svg .s-weeks{fill:#000000!important;}
        #journey-svg #train-glow{filter:none!important;}
        #journey-svg #train-body{fill:#bbab8c!important;}
        #journey-svg #train-dot{fill:#fdf7e4!important;}
        #journey-svg .flag-pole{stroke:#bbab8c!important;}
        #journey-svg .flag-rect{fill:#bbab8c!important;}
        #journey-svg .goal-lbl{fill:#000000!important;}

        /* Detail Panel */
        #detail{background:#fdf7e4!important;border:2px solid #bbab8c!important;box-shadow:none!important;}
        #detail .d-title{color:#000000!important;}
        #detail .d-close{background:#fdf7e4!important;color:#000000!important;border:1px solid #bbab8c!important;}
        #detail .badge-done, #detail .badge-active, #detail .badge-upcoming{background:#fdf7e4!important;color:#000000!important;border:1.5px solid #bbab8c!important;}
        #detail .d-meta{color:#000000!important;}
        #detail .ph-row{color:#000000!important;}
        #detail .ph-badge{background:#fdf7e4!important;color:#000000!important;border:1px solid #bbab8c!important;}
        #detail .d-section{color:#000000!important;text-decoration:underline;text-decoration-color:#bbab8c!important;}
        #detail .d-resources li{color:#000000!important;}
        #detail .d-project{background:#fdf7e4!important;border:2px solid #bbab8c!important;color:#000000!important;}
        #overlay{background:#fdf7e4!important;backdrop-filter:none!important;}

        /* Progress Bar */
        #prog-wrap .prog-label{color:#000000!important;}
        #prog-wrap .prog-bar{background:#fdf7e4!important;border:1px solid #bbab8c!important;}
        #prog-wrap .prog-fill{background:#bbab8c!important;}

        /* Achievements */
        .ba-grid h2{color:#000000!important;}
        .ba-card{background:#fdf7e4!important;border:2px solid #bbab8c!important;}
        .ba-on{background:#fdf7e4!important;border:2px solid #bbab8c!important;box-shadow:none!important;}
        .ba-off{background:#fdf7e4!important;border:1px solid #bbab8c!important;opacity:0.4!important;}
        .ba-icon{color:#000000!important;}
        .ba-title{color:#000000!important;}
        .ba-on .ba-title{color:#000000!important;font-weight:800!important;}
        .ba-desc{color:#000000!important;}
        .ba-status{color:#000000!important;}
        .ba-on .ba-status{color:#000000!important;font-weight:700!important;}
        /* Ensure the HTML component's body background is light */
        .stHtml body{background:""" + COLOR_BG_LIGHT + """!important;}


        /* File Uploader and Buttons */
        div[data-testid="stFileUploader"] section {background-color:#fdf7e4!important; border:1px dashed #bbab8c!important;}
        div[data-testid="stFileUploader"] label, div[data-testid="stFileUploader"] p, div[data-testid="stFileUploader"] small {color:#000000!important;}
        div[data-testid="stFileUploader"] button {background-color:#fdf7e4!important; color:#000000!important; border:1px solid #bbab8c!important;}
        div[data-testid="stButton"] button:not([kind="primary"]), div[data-testid="stDownloadButton"] button {background:#fdf7e4!important; border:1px solid #bbab8c!important; color:#000000!important;}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"]{background:#fdf7e4!important;border:1px solid #bbab8c!important;border-radius:12px;}
        .stTabs [data-baseweb="tab"]{color:#000000!important;}
        .stTabs [aria-selected="true"]{background:#bbab8c!important;color:#000000!important;border-radius:10px;}
        .stTabs [data-baseweb="tab-panel"]{background:transparent!important;}

        /* Cards */
        .stat-card{background:#fdf7e4!important;border-color:#bbab8c!important;}
        .sc-val{color:#000000!important;}
        .sc-lbl{color:#000000!important;}
        .feat-card,.fc-wrap,.score-card,.ats-card,.suggestion-card,
        .roadmap-card,.customize-card,.customize-box,
        .auth-card{background:#fdf7e4!important;border-color:#bbab8c!important;
                   backdrop-filter:none!important;box-shadow:none!important;}
        .fct{color:#000000!important;}
        .fcd{color:#000000!important;}
        .fcb{background:#bbab8c!important;color:#000000!important;border-color:#bbab8c!important;}

        /* Force all inline white text inside cards to dark */
        .fc-wrap div, .fc-wrap p, .fc-wrap span,
        .feat-card div, .feat-card p, .feat-card span,
        .stat-card div, .stat-card p, .stat-card span,
        .score-card div, .score-card p, .score-card span,
        .ats-card div, .ats-card p, .ats-card span,
        .roadmap-card div, .roadmap-card p, .roadmap-card span,
        .customize-card div, .customize-card p, .customize-card span,
        .customize-box div, .customize-box p, .customize-box span,
        .auth-card div, .auth-card p, .auth-card span,
        .auth-title, .prog-lbl, .auth-card h1, .auth-card h2, .auth-card h3, .auth-card h4
        {color:#000000!important;}
        .auth-sub, .prog-lbl{color:#000000!important;}
        .auth-card div[style*="color:#c4b5fd"] {color:#000000!important;}
        .prog-step{background:#bbab8c!important;}
        .prog-done{background:#bbab8c!important;}
        .prog-active{background:#bbab8c!important;}
        .fc-wrap div[style*="rgba(255,255,255,0.55)"],
        .fc-wrap div[style*="color:#fff"],
        .feat-card div[style*="color:#fff"]
        {color:#000000!important;}

        /* Section titles and headings in page body */
        .page-body h1,.page-body h2,.page-body h3,
        .page-body p,.page-body span,.page-body div
        {color:#000000!important;}
        .sec-title{color:#000000!important;}

        /* Skill chips */
        .chip-g{background:#bbab8c!important;color:#000000!important;border-color:#bbab8c!important;}
        .chip-r{background:#bbab8c!important;color:#000000!important;border-color:#bbab8c!important;}

        /* Progress / Skills boxes */
        .progress-box{background:#fdf7e4!important;border-color:#bbab8c!important;}
        .box-title{color:#000000!important;}
        .empty-msg{color:#000000!important;}
        .ats-box{background:#fdf7e4!important;border-color:#bbab8c!important;}
        .ats-label{color:#000000!important;}
        .prog-bg{background:#fdf7e4!important;border:1px solid #bbab8c!important;}

        /* Alerts / info boxes */
        div[data-testid="stAlert"]{background:#fdf7e4!important;color:#000000!important;}
        div[data-testid="stAlert"] p{color:#000000!important;}

        /* Checkboxes and toggles */
        div[data-testid="stCheckbox"] span{color:#000000!important;}
        div[data-testid="stToggle"] span{color:#000000!important;}

        /* Sidebar / page body */
        .page-body{background:""" + COLOR_BG_LIGHT + """!important;}

        /* Progress bars */
        .prog-bg{background:#fdf7e4!important;border:1px solid #bbab8c!important;}

        /* Roadmap SVG background */
        body{background:""" + COLOR_BG_LIGHT + """!important;}

        /* Remove cool-toned inline accents in light mode */
        [style*="#333F63"],
        [style*="#4f46e5"],
        [style*="#7c3aed"],
        [style*="#6366f1"],
        [style*="#60a5fa"],
        [style*="#0ea5e9"],
        [style*="#a78bfa"],
        [style*="#c4b5fd"],
        [style*="#10b981"],
        [style*="#34d399"],
        [style*="#059669"],
        [style*="#ef4444"],
        [style*="#f87171"],
        [style*="#dc2626"],
        [style*="#d97706"],
        [style*="#f59e0b"],
        [style*="#fbbf24"],
        [style*="#fcd34d"],
        [style*="#5eead4"],
        [style*="#fca5a5"],
        [style*="#6b7280"],
        [style*="#9ca3af"],
        [style*="#111827"],
        [style*="#ffffff"],
        [style*="#fff"],
        [style*="rgba(51,63,99"],
        [style*="rgba(124,58,237"],
        [style*="rgba(167,139,250"],
        [style*="rgba(16,185,129"],
        [style*="rgba(239,68,68"],
        [style*="rgba(245,158,11"],
        [style*="rgba(159,140,118"]{
            color:#000000!important;
            border-color:#bbab8c!important;
        }
        [style*="background:#333F63"],
        [style*="background: #333F63"],
        [style*="background-color:#333F63"],
        [style*="background-color: #333F63"],
        [style*="background:#ffffff"],
        [style*="background: #ffffff"],
        [style*="background:#fff"],
        [style*="background: #fff"],
        [style*="background-color:#ffffff"],
        [style*="background-color: #ffffff"],
        [style*="background-color:#fff"],
        [style*="background-color: #fff"],
        [style*="background:#f8fafc"],
        [style*="background: #f8fafc"],
        [style*="background-color:#f8fafc"],
        [style*="background-color: #f8fafc"],
        [style*="background:rgba(0,0,0,0.24)"],
        [style*="background: rgba(0,0,0,0.24)"],
        [style*="background:rgba(255,255,255"],
        [style*="background: rgba(255,255,255"],
        [style*="background:rgba(255,255,240"],
        [style*="background: rgba(255,255,240"],
        [style*="background:rgba(124,58,237"],
        [style*="background:rgba(167,139,250"],
        [style*="background:rgba(16,185,129"],
        [style*="background:rgba(239,68,68"],
        [style*="background:rgba(245,158,11"],
        [style*="background:rgba(159,140,118"],
        [style*="background:linear-gradient"],
        [style*="background: linear-gradient"]{
            background:#fdf7e4!important;
            background-color:#fdf7e4!important;
            color:#000000!important;
            border-color:#bbab8c!important;
        }
        [style*="color:#fff"],
        [style*="color: #fff"],
        [style*="color:white"],
        [style*="color: white"],
        [style*="color:#ffffff"],
        [style*="color: #ffffff"]{
            color:#000000!important;
        }
        [style*="box-shadow"]{box-shadow:none!important;}
        """
        )
    else:
        _bg          = COLOR_BG_DARK
        _nav_bg      = "rgba(0,0,0,0.42)"
        _nav_border  = "rgba(255,255,240,0.12)"
        _btn_color   = "rgba(255,255,240,0.70)"
        _btn_hover   = "rgba(255,255,240,0.10)"
        _text_color  = "#FFFFF0"
        _active_bg   = "#333F63"
        _active_text = "#FFFFF0"
        _active_border = "rgba(255,255,240,0.28)"
        _page_gradient_bg = "rgba(0,0,0,0.24)"
        _page_card_bg = "rgba(0,0,0,0.24)"
        _page_chip_bg = "rgba(51,63,99,0.42)"
        _brand_gap_color = "rgba(255,255,240,0.72)"
        _theme_css   = (
        """
        html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"],
        .main,.block-container{background:""" + BG_STATIC + """!important;color:#FFFFF0!important;}
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stMarkdownContainer"] a,
        div[data-testid="stMarkdownContainer"] strong,
        label,p,h1,h2,h3,h4,h5,span,li,a,strong{color:#FFFFF0!important;}
        div[data-testid="stCaptionContainer"] p,
        small,.caption,.sc-lbl,.fcd,.empty-msg,.coverage-meta,.priority-caption,.auth-sub
        {color:rgba(255,255,240,0.62)!important;}
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] > div > div,
        div[data-testid="stMultiSelect"] > div > div,
        div[data-testid="stChatInput"] textarea
        {background:rgba(0,0,0,0.24)!important;color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;border-radius:12px!important;}
        div[data-testid="stExpander"],
        div[data-testid="stChatMessage"],
        div[data-testid="stMetric"],
        .stat-card,.feat-card,.fc-wrap,.score-card,.ats-card,.suggestion-card,
        .roadmap-card,.customize-card,.customize-box,.auth-card,.progress-box,.ats-box,
        .result-panel,.coverage-card,.top-action-panel,.resume-result-card,.detail-panel,.contact-card,
        .info-pill,.history-card,.cta-box
        {background:rgba(0,0,0,0.26)!important;border:1px solid rgba(255,255,240,0.14)!important;
         box-shadow:0 18px 44px rgba(0,0,0,0.28)!important;backdrop-filter:blur(18px)!important;}
        .stat-card:hover,.feat-card:hover,.fc-wrap:hover,.result-panel:hover,.coverage-card:hover
        {transform:translateY(-3px)!important;border-color:rgba(255,255,240,0.28)!important;
         box-shadow:0 22px 52px rgba(0,0,0,0.36),0 0 24px rgba(255,255,240,0.08)!important;}
        .stTabs [data-baseweb="tab-list"]{background:rgba(0,0,0,0.22)!important;border-radius:12px;}
        .stTabs [data-baseweb="tab"]{color:rgba(255,255,240,0.62)!important;}
        .stTabs [aria-selected="true"]{background:#333F63!important;color:#FFFFF0!important;border-radius:10px;}
        div[data-testid="stMetricLabel"]{color:rgba(255,255,240,0.62)!important;}
        div[data-testid="stMetricValue"]{color:#FFFFF0!important;}
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stDownloadButton"] button[kind="primary"]
        {background:#333F63!important;color:#FFFFF0!important;
         border:1px solid rgba(255,255,240,0.18)!important;box-shadow:none!important;}
        div[data-testid="stButton"] button:not([kind="primary"]),
        div[data-testid="stDownloadButton"] button
        {background:rgba(0,0,0,0.24)!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.16)!important;}
        .chip-g,.chip-r,.chip-y,.gap-chip,.skill-chip,.fc-badge,.fcb,.panel-count,.priority-num
        {background:rgba(51,63,99,0.55)!important;color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;}
        .prog-bg,.coverage-track{background:rgba(0,0,0,0.30)!important;}
        .prog-fill,.coverage-fill,.prog-done,.prog-active{background:#FFFFF0!important;}
        .page-body{background:transparent!important;}
        [style*="#7c3aed"],[style*="#4f46e5"],[style*="#a78bfa"],[style*="#c4b5fd"],
        [style*="#10b981"],[style*="#34d399"],[style*="#059669"],[style*="#ef4444"],
        [style*="#f87171"],[style*="#dc2626"],[style*="#d97706"],[style*="#0ea5e9"],
        [style*="#f59e0b"],[style*="#fbbf24"],[style*="#fcd34d"],[style*="#5eead4"],
        [style*="#fca5a5"]{color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;}
        [style*="rgba(124,58,237"],[style*="rgba(167,139,250"],[style*="rgba(16,185,129"],
        [style*="rgba(239,68,68"],[style*="rgba(245,158,11"],[style*="linear-gradient"]
        {background:rgba(0,0,0,0.24)!important;border-color:rgba(255,255,240,0.18)!important;color:#FFFFF0!important;}
        [style*="box-shadow"]{box-shadow:none!important;}
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
    background:{_active_bg}!important;
    color:{_active_text}!important;
    border-color:{_active_border}!important;
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

/* Keep gradients on page backgrounds only. Inner UI surfaces stay flat. */
.page-body [style*="linear-gradient"],
.page-body div[style*="linear-gradient"],
.page-body section[style*="linear-gradient"]{{
    background:{_page_gradient_bg}!important;
}}
.page-body div[data-testid="stButton"] button[kind="primary"],
.page-body div[data-testid="stDownloadButton"] button[kind="primary"]{{
    background:{_active_bg}!important;
    box-shadow:none!important;
}}
.page-body .stat-card,.page-body .feat-card,.page-body .fc-wrap,.page-body .progress-box,
.page-body .ats-box,.page-body .result-panel,.page-body .coverage-card,.page-body .top-action-panel,
.page-body .resume-result-card,.page-body .detail-panel,.page-body .contact-card,.page-body .info-pill,
.page-body .history-card,.page-body .cta-box,.page-body .auth-card,.page-body .template-preview-card,
.page-body .user-msg,.page-body .bot-msg{{
    background:{_page_card_bg}!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
}}
.page-body .chip-g,.page-body .chip-r,.page-body .chip-y,.page-body .gap-chip,
.page-body .skill-chip,.page-body .fc-badge,.page-body .fcb,.page-body .panel-count,
.page-body .priority-num{{
    background:{_page_chip_bg}!important;
}}

/* Responsive app shell */
img,svg,canvas,iframe,video{{max-width:100%;}}
div[data-testid="stMarkdownContainer"]{{overflow-wrap:anywhere;}}
div[data-testid="stButton"] button,
div[data-testid="stDownloadButton"] button{{min-height:2.35rem!important;white-space:normal!important;}}

@media (max-width: 1180px){{
    div[data-testid="stHorizontalBlock"]:first-of-type{{
        overflow-x:auto!important;
        overflow-y:hidden!important;
        justify-content:flex-start!important;
        padding:0.35rem 0.8rem!important;
        scrollbar-width:thin;
        -webkit-overflow-scrolling:touch;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type > div{{
        min-width:max-content!important;
        flex:0 0 auto!important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{{
        padding:0.32rem 0.55rem!important;
    }}
    .page-body{{padding:1.25rem 1rem 1.6rem!important;}}
}}

@media (max-width: 760px){{
    .page-body{{padding:1rem 0.75rem 1.4rem!important;}}
    .block-container{{width:100%!important;min-width:0!important;}}
    div[data-testid="stHorizontalBlock"]:not(:first-of-type){{
        flex-wrap:wrap!important;
        gap:0.75rem!important;
    }}
    div[data-testid="stHorizontalBlock"]:not(:first-of-type) > div[data-testid="column"]{{
        width:100%!important;
        min-width:100%!important;
        flex:1 1 100%!important;
    }}
    .stTabs [data-baseweb="tab-list"]{{
        overflow-x:auto!important;
        flex-wrap:nowrap!important;
        scrollbar-width:thin;
    }}
    .stTabs [data-baseweb="tab"]{{
        flex:0 0 auto!important;
        white-space:nowrap!important;
    }}
    .stat-card,.feat-card,.fc-wrap,.progress-box,.ats-box,.result-panel,.coverage-card,
    .top-action-panel,.resume-result-card,.detail-panel,.contact-card,.info-pill,.history-card,.cta-box{{
        border-radius:14px!important;
        padding:1rem!important;
    }}
    .gap-hero-top,.skill-grid,.coverage-grid,.priority-list,.suggestion-grid{{
        display:grid!important;
        grid-template-columns:1fr!important;
    }}
    .gap-score{{text-align:left!important;min-width:0!important;}}
    .gap-score-num{{font-size:2.45rem!important;}}
    .history-row{{grid-template-columns:1fr!important;gap:0.35rem!important;}}
    .history-head{{display:none!important;}}
    .score-num{{font-size:2.5rem!important;}}
    .template-preview-card{{height:auto!important;min-height:300px!important;}}
    .template-preview-frame{{height:240px!important;}}
    .user-msg,.bot-msg{{max-width:94%!important;width:fit-content!important;}}
    [style*="grid-template-columns:1fr 1fr"]{{
        grid-template-columns:1fr!important;
    }}
    [style*="width:260px"]{{
        width:100%!important;max-width:260px!important;
    }}
}}

@media (max-width: 430px){{
    .page-body{{padding:0.8rem 0.55rem 1.2rem!important;}}
    div[data-testid="stHorizontalBlock"]:first-of-type{{
        padding:0.3rem 0.5rem!important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{{
        font-size:0.72rem!important;
        padding:0.28rem 0.45rem!important;
    }}
    h1{{font-size:1.55rem!important;line-height:1.18!important;}}
    h2{{font-size:1.25rem!important;line-height:1.2!important;}}
    h3{{font-size:1.05rem!important;line-height:1.25!important;}}
    div[data-testid="stMetricValue"]{{font-size:1.35rem!important;}}
    .gap-score-num{{font-size:2rem!important;}}
    .chip-g,.chip-r,.chip-y,.gap-chip,.skill-chip{{font-size:0.72rem!important;padding:0.25rem 0.55rem!important;}}
}}
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
            f'<span style="color:{_brand_gap_color};">Gap</span></p>',
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
