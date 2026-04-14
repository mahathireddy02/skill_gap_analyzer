import streamlit as st

def show_navbar(active="Dashboard"):
    name    = st.session_state.get("user", {}).get("name", "User")
    first   = name.split()[0]

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],[data-testid="stSidebarNav"],[data-testid="stSidebar"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"],.stDeployButton,
[class*="viewerBadge"],[class*="toolbar"]{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;font-family:'Inter',sans-serif!important;}
.block-container{padding:0!important;margin:0!important;max-width:100%!important;}
div[data-testid="stAppViewContainer"]>section{padding-top:0!important;}

/* Navbar column strip */
div[data-testid="stHorizontalBlock"]:first-of-type{
    background:#0d0b1e;
    border-bottom:1px solid rgba(255,255,255,0.08);
    padding:0.45rem 1.2rem!important;
    margin:0!important;
    align-items:center!important;
    gap:0.2rem!important;
    position:sticky;top:0;z-index:9999;
}

/* All buttons inside navbar strip */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
    background:transparent!important;
    border:1px solid transparent!important;
    color:rgba(255,255,255,0.65)!important;
    font-size:0.82rem!important;
    font-weight:500!important;
    padding:0.32rem 0.75rem!important;
    border-radius:8px!important;
    white-space:nowrap!important;
    height:auto!important;
    min-height:unset!important;
    line-height:1.4!important;
    box-shadow:none!important;
    transition:all 0.15s!important;
    width:100%!important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
    background:rgba(255,255,255,0.08)!important;
    color:#fff!important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button[kind="primary"]{
    background:rgba(167,139,250,0.18)!important;
    color:#a78bfa!important;
    border-color:rgba(167,139,250,0.35)!important;
    font-weight:600!important;
}
.page-body{padding:1.6rem 2rem 2rem;}
</style>
""", unsafe_allow_html=True)

    nav_items = [
        ("🏠 Dashboard",    "Dashboard",    "pages/3_Dashboard.py"),
        ("📄 Resume Score", "Resume Score", "pages/4_Resume_Score.py"),
        ("🧠 Skill Gap",    "Skill Gap",    "pages/5_Skill_Gap.py"),
        ("🛤️ Roadmap",      "Roadmap",      "pages/6_Roadmap.py"),
        ("📊 Analytics",    "Analytics",    "pages/7_Analytics.py"),
    ]

    # logo(1.2) + 5 nav(0.9 each) + spacer(2.5) + profile(0.9) + logout(0.75)
    cols = st.columns([1.2, 0.9, 0.9, 0.9, 0.85, 0.9, 2.5, 0.9, 0.75])

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

    with cols[7]:
        if st.button(f"👤 {first}", key="nb_profile", use_container_width=True):
            st.switch_page("pages/8_Profile.py")

    with cols[8]:
        if st.button("🚪", key="nb_logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
