import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
from utils.skill_analyzer import analyze_skill_gap, get_roles, suggest_roles
from components.navbar import show_navbar

st.set_page_config(page_title="Skill Gap · SkillGap", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")
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
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;border:1px solid rgba(255,255,240,0.18)!important;}
.chip-g{display:inline-block;background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.chip-r{display:inline-block;background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.chip-y{display:inline-block;background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.tier-box{background:rgba(124,58,237,0.12);border-radius:12px;padding:0.8rem 1rem;margin-bottom:0.5rem;
    border-left:4px solid #7c3aed;color:#fff;}
.tier-box div{color:#fff!important;}
.gap-result{display:flex;flex-direction:column;gap:1rem;width:100%;}
.gap-hero{background:rgba(0,0,0,0.24);
    border:1px solid rgba(255,255,255,0.14);border-radius:18px;padding:1.25rem 1.35rem;color:#fff;
    box-shadow:0 18px 45px rgba(15,23,42,0.25);}
.gap-hero-top{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;}
.gap-eyebrow{font-size:0.72rem;text-transform:uppercase;font-weight:800;letter-spacing:0.08em;opacity:0.76;}
.gap-role{font-size:1.45rem;font-weight:900;line-height:1.15;margin-top:0.2rem;}
.gap-desc{font-size:0.86rem;opacity:0.78;margin-top:0.35rem;max-width:40rem;line-height:1.45;}
.gap-score{text-align:right;min-width:130px;}
.gap-score-num{font-size:3.25rem;font-weight:950;line-height:0.9;}
.gap-grade{display:inline-block;margin-top:0.45rem;padding:0.22rem 0.62rem;border-radius:999px;
    background:rgba(255,255,255,0.18);font-weight:850;font-size:0.9rem;}
.result-section-title{font-size:0.92rem;font-weight:900;margin:0.1rem 0 0.7rem;}
.coverage-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0.75rem;}
.coverage-card{background:var(--gap-card-bg,#111827);border:1px solid var(--gap-card-border,rgba(148,163,184,0.22));
    border-radius:14px;padding:0.85rem 0.95rem;min-height:112px;}
.coverage-title{font-size:0.77rem;font-weight:850;margin-bottom:0.35rem;}
.coverage-value{font-size:1.75rem;font-weight:950;color:var(--gap-text,#fff);line-height:1;}
.coverage-meta{font-size:0.76rem;color:var(--gap-muted,rgba(255,255,255,0.58));margin-top:0.35rem;}
.coverage-track{height:7px;background:var(--gap-track,rgba(255,255,255,0.1));border-radius:999px;overflow:hidden;margin-top:0.7rem;}
.coverage-fill{height:100%;border-radius:999px;}
.skill-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0.85rem;}
.result-panel{background:var(--gap-card-bg,#111827);border:1px solid var(--gap-card-border,rgba(148,163,184,0.22));
    border-radius:16px;padding:1rem;min-height:172px;}
.panel-head{display:flex;justify-content:space-between;align-items:center;gap:0.8rem;margin-bottom:0.75rem;}
.panel-title{font-size:0.92rem;font-weight:900;color:var(--gap-text,#fff);}
.panel-count{font-size:0.72rem;font-weight:800;color:var(--gap-muted,rgba(255,255,255,0.68));
    background:var(--gap-pill-bg,rgba(255,255,255,0.08));border-radius:999px;padding:0.18rem 0.55rem;white-space:nowrap;}
.chip-list{display:flex;flex-wrap:wrap;gap:0.38rem;}
.gap-chip{display:inline-flex;align-items:center;border-radius:999px;padding:0.32rem 0.68rem;
    font-size:0.78rem;font-weight:750;line-height:1.25;border:1px solid transparent;}
.gap-chip.good{background:rgba(16,185,129,0.14);color:#5eead4;border-color:rgba(16,185,129,0.28);}
.gap-chip.bad{background:rgba(239,68,68,0.13);color:#fca5a5;border-color:rgba(239,68,68,0.28);}
.gap-chip.warn{background:rgba(245,158,11,0.13);color:#fcd34d;border-color:rgba(245,158,11,0.30);}
.empty-note{background:var(--gap-empty-bg,rgba(255,255,255,0.06));border:1px dashed var(--gap-empty-border,rgba(255,255,255,0.16));
    border-radius:12px;padding:0.8rem;color:var(--gap-muted,rgba(255,255,255,0.72));font-size:0.84rem;}
.priority-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0.5rem;}
.priority-row{display:flex;align-items:center;gap:0.55rem;background:var(--gap-row-bg,#0f172a);
    border:1px solid var(--gap-row-border,rgba(148,163,184,0.18));border-radius:12px;padding:0.62rem 0.72rem;}
.priority-num{width:1.55rem;height:1.55rem;border-radius:999px;display:inline-flex;align-items:center;
    justify-content:center;background:rgba(124,58,237,0.22);color:#c4b5fd;font-size:0.75rem;font-weight:900;flex:0 0 auto;}
.priority-skill{font-size:0.85rem;font-weight:800;color:var(--gap-text,#fff);}
.priority-caption{font-size:0.8rem;color:var(--gap-muted,rgba(255,255,255,0.58));margin:-0.35rem 0 0.7rem;}
.skill-count-line{font-weight:800;margin:-0.25rem 0 0.45rem;line-height:1.2;color:var(--gap-text,#fff)!important;}
.top-action-band{display:grid;grid-template-columns:minmax(220px,0.8fr) minmax(360px,1.6fr);gap:1rem;margin:0.25rem 0 1rem;}
.top-action-panel{background:var(--gap-card-bg,#111827);border:1px solid var(--gap-card-border,rgba(148,163,184,0.22));
    border-radius:14px;padding:0.9rem 1rem;}
.suggestion-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0.65rem;}
.suggestion-card{display:flex;justify-content:space-between;align-items:center;gap:0.6rem;background:var(--gap-row-bg,#0f172a);
    border:1px solid var(--gap-row-border,rgba(148,163,184,0.18));border-radius:12px;padding:0.62rem 0.72rem;}
.suggestion-role{font-weight:800;font-size:0.84rem;color:var(--gap-text,#fff)!important;}
.suggestion-score{font-weight:900;font-size:0.84rem;white-space:nowrap;}

/* Strict premium dark palette */
html,body,.stApp{color:#FFFFF0!important;}
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.18)!important;box-shadow:none!important;}
.gap-hero,.tier-box,.coverage-card,.result-panel,.top-action-panel,.suggestion-card,.priority-row{background:rgba(0,0,0,0.24)!important;border-color:rgba(255,255,240,0.14)!important;color:#FFFFF0!important;box-shadow:none!important;backdrop-filter:none!important;}
.gap-grade,.panel-count,.priority-num,.gap-chip.good,.gap-chip.bad,.gap-chip.warn,.chip-g,.chip-r,.chip-y{background:rgba(51,63,99,0.42)!important;color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;}
.gap-role,.gap-score-num,.coverage-value,.panel-title,.priority-skill,.suggestion-role,.result-section-title,.skill-count-line{color:#FFFFF0!important;}
.gap-desc,.gap-eyebrow,.coverage-meta,.priority-caption{color:rgba(255,255,240,0.62)!important;}
.coverage-track{background:rgba(0,0,0,0.30)!important;}
.coverage-fill{background:#FFFFF0!important;}
@media(max-width:900px){.gap-hero-top,.skill-grid{grid-template-columns:1fr;display:grid}.gap-score{text-align:left}
    .coverage-grid,.priority-list,.top-action-band,.suggestion-grid{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)

show_navbar("Skill Gap")

st.markdown("## 🧠 Skill Gap Analyzer")

db_user     = get_user(st.session_state.email)
user_skills = db_user.get("skills", [])
target_role = db_user.get("target_role", "").strip()
theme       = db_user.get("theme", "dark")

if theme == "light":
    st.markdown("""
    <style>
    :root,.page-body{--gap-card-bg:#fdf7e4;--gap-card-border:#bbab8c;--gap-text:#000000;
        --gap-muted:#000000;--gap-track:#fdf7e4;--gap-pill-bg:#bbab8c;--gap-empty-bg:#fdf7e4;
        --gap-empty-border:#bbab8c;--gap-row-bg:#fdf7e4;--gap-row-border:#bbab8c;}
    .gap-hero,.tier-box{background:#fdf7e4!important;border-color:#bbab8c!important;color:#000000!important;}
    .gap-hero div,.gap-hero span,.gap-role,.gap-score-num,.gap-desc,.gap-eyebrow,.gap-grade{color:#FFFFF0!important;}
    .gap-hero div,.gap-hero span,.gap-role,.gap-score-num,.gap-desc,.gap-eyebrow,.gap-grade{color:#000000!important;}
    .coverage-card,.result-panel,.top-action-panel{background:#fdf7e4!important;border-color:#bbab8c!important;}
    .priority-row,.suggestion-card{background:#fdf7e4!important;border-color:#bbab8c!important;}
    .coverage-track{background:#fdf7e4!important;border:1px solid #bbab8c!important;}
    .coverage-value,.panel-title,.priority-skill,.suggestion-role,.result-section-title,.skill-count-line{color:#000000!important;}
    .coverage-meta,.panel-count,.priority-caption,.empty-note{color:#000000!important;}
    .panel-count,.priority-num{background:#bbab8c!important;color:#000000!important;border-color:#bbab8c!important;}
    .empty-note{background:#fdf7e4!important;border-color:#bbab8c!important;}
    .gap-chip.good,.gap-chip.bad,.gap-chip.warn{background:#bbab8c!important;color:#000000!important;border-color:#bbab8c!important;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    :root,.page-body{--gap-card-bg:rgba(0,0,0,0.26);--gap-card-border:rgba(255,255,240,0.14);--gap-text:#FFFFF0;
        --gap-muted:rgba(255,255,240,0.66);--gap-track:rgba(0,0,0,0.30);--gap-pill-bg:rgba(51,63,99,0.42);
        --gap-empty-bg:rgba(0,0,0,0.22);--gap-empty-border:rgba(255,255,240,0.16);
        --gap-row-bg:rgba(0,0,0,0.24);--gap-row-border:rgba(255,255,240,0.14);}
    .gap-chip.good,.gap-chip.bad,.gap-chip.warn{background:rgba(51,63,99,0.42)!important;color:#FFFFF0!important;border-color:rgba(255,255,240,0.18)!important;}
    </style>
    """, unsafe_allow_html=True)

result_accent = "#bbab8c" if theme == "light" else "#FFFFF0"

if not target_role:
    st.warning("⚠️ No target role set. Please update it in your Profile.")
    if st.button("👤 Go to Profile", type="primary"):
        st.switch_page("pages/8_Profile.py")
    st.stop()

st.markdown(
    f'<div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);'
    f'border-radius:10px;padding:0.5rem 1rem;font-size:0.9rem;margin-bottom:0.55rem;">'
    f'🎯 Analyzing for: <strong>{target_role}</strong> '
    f'<span style="font-size:0.75rem;opacity:0.5;">(✏️ change in Profile)</span></div>',
    unsafe_allow_html=True,
)

action_info, action_button = st.columns([3, 1], gap="medium")

if not user_skills:
    st.warning("No skills detected from resume.")
    manual = st.text_input("Enter your skills manually (comma-separated)",
                           placeholder="e.g. Python, SQL, Excel")
    with action_button:
        run_gap = st.button("Analyze Gap", type="primary", use_container_width=True)
    if run_gap:
        skills_to_use = [s.strip().lower() for s in manual.split(",") if s.strip()]
        if not skills_to_use:
            st.error("Please enter at least one skill.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    result = analyze_skill_gap(skills_to_use, target_role)
                    update_user(st.session_state.email, {
                        "target_role":    target_role,
                        "missing_skills": result["missing_skills"],
                        "skills":         skills_to_use,
                        "gap_result":     result,
                        "gap_analyzed":   True,
                    })
                    st.session_state["gap_result"] = result
                except ValueError as e:
                    st.error(f"{e}")
                    st.info(f"Supported roles: {', '.join(get_roles())}")
else:
    with action_info:
        st.markdown(f'<div class="skill-count-line">Your skills: {len(user_skills)} detected</div>', unsafe_allow_html=True)
    with action_button:
        run_gap = st.button("Analyze Gap", type="primary", use_container_width=True)
    if run_gap:
        with st.spinner("Analyzing..."):
            try:
                result = analyze_skill_gap(user_skills, target_role)
                update_user(st.session_state.email, {
                    "target_role":    target_role,
                    "missing_skills": result["missing_skills"],
                    "gap_result":     result,
                    "gap_analyzed":   True,
                })
                st.session_state["gap_result"] = result
            except ValueError as e:
                st.error(f"{e}")
                st.info(f"Supported roles: {', '.join(get_roles())}")

st.markdown('<div class="top-action-panel"><div class="panel-head"><div class="panel-title">Best Role Matches</div></div>', unsafe_allow_html=True)
if user_skills:
    suggestions = suggest_roles(user_skills, top_n=3)
    cards = []
    for s in suggestions:
        grade_color = result_accent
        cards.append(
            f'<div class="suggestion-card"><span class="suggestion-role">{s["role"]}</span>'
            f'<span class="suggestion-score" style="color:{grade_color}!important;">'
            f'{s["score"]}% ({s["grade"]})</span></div>'
        )
    st.markdown(f'<div class="suggestion-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
else:
    st.info("Upload your resume to see role suggestions.")
st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    if "gap_result" in st.session_state:
        r = st.session_state["gap_result"]

        def _skill_chips(items, cls, prefix=""):
            return "".join(
                f'<span class="gap-chip {cls}">{prefix}{s.title()}</span>'
                for s in items
            )

        def _empty_note(text):
            return f'<div class="empty-note">{text}</div>'

        score = r["score"]
        grade = r["grade"]

        st.markdown(f"""
        <div class="gap-result">
        <div class="gap-hero">
            <div class="gap-hero-top">
                <div>
                    <div class="gap-eyebrow">Match Score for</div>
                    <div class="gap-role">{r['role']}</div>
                    <div class="gap-desc">{r['role_description']}</div>
                </div>
                <div class="gap-score">
                    <div class="gap-score-num">{score}%</div>
                    <div class="gap-grade">Grade: {grade}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tier_data = r.get("tier_breakdown", {})
        tier_cards = []
        for tier, label, color_t in [
            ("core", "Core Skills", result_accent),
            ("important", "Important", result_accent),
            ("nice_to_have", "Nice to Have", result_accent),
        ]:
            td = tier_data.get(tier, {})
            cov = td.get("coverage", 0)
            tier_cards.append(
                f'<div class="coverage-card">'
                f'<div class="coverage-title" style="color:{color_t}!important;">{label}</div>'
                f'<div class="coverage-value">{cov}%</div>'
                f'<div class="coverage-meta">{td.get("matched",0)}/{td.get("total",0)} skills</div>'
                f'<div class="coverage-track"><div class="coverage-fill" '
                f'style="width:{min(cov,100)}%;background:{color_t};"></div></div>'
                f'</div>'
            )
        st.markdown(
            '<div class="result-section-title">Skill Tier Coverage</div>'
            f'<div class="coverage-grid">{"".join(tier_cards)}</div>',
            unsafe_allow_html=True,
        )

        matched_body = (
            f'<div class="chip-list">{_skill_chips(r["matched_skills"], "good")}</div>'
            if r["matched_skills"] else _empty_note("No matching skills yet.")
        )
        missing_body = (
            f'<div class="chip-list">{_skill_chips(r["missing_skills"], "bad")}</div>'
            if r["missing_skills"] else _empty_note("You have all required skills!")
        )
        st.markdown(f"""
        <div class="skill-grid">
            <div class="result-panel">
                <div class="panel-head">
                    <div class="panel-title">Matched Skills</div>
                    <div class="panel-count">{len(r["matched_skills"])} found</div>
                </div>
                {matched_body}
            </div>
            <div class="result-panel">
                <div class="panel-head">
                    <div class="panel-title">Missing Skills</div>
                    <div class="panel-count">{len(r["missing_skills"])} missing</div>
                </div>
                {missing_body}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if r.get("partial_matches"):
            partial_chips = []
            for pm in r["partial_matches"]:
                partial_chips.append(
                    f'<span class="gap-chip warn">~{pm["required"].title()} '
                    f'(you have: {pm["user_has"]}, {int(pm["similarity"]*100)}% match)</span>'
                )
            st.markdown(
                '<div class="result-panel">'
                '<div class="panel-head"><div class="panel-title">Partial Matches (Close but not exact)</div>'
                f'<div class="panel-count">{len(r["partial_matches"])} close</div></div>'
                f'<div class="chip-list">{"".join(partial_chips)}</div></div>',
                unsafe_allow_html=True,
            )

        if r["recommendations"]:
            priority_rows = []
            for i, skill in enumerate(r["recommendations"][:6], 1):
                priority_rows.append(
                    f'<div class="priority-row"><span class="priority-num">{i}</span>'
                    f'<span class="priority-skill">{skill.title()}</span></div>'
                )
            st.markdown(
                '<div class="result-panel">'
                '<div class="panel-head"><div class="panel-title">Priority Skills to Learn</div>'
                '<div class="panel-count">Top 6</div></div>'
                '<div class="priority-caption">In order of importance for this role:</div>'
                f'<div class="priority-list">{"".join(priority_rows)}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
        if r["missing_skills"]:
            if st.button("\U0001f6e4\ufe0f Generate Personalized Roadmap", type="primary", use_container_width=True):
                st.switch_page("pages/6_Roadmap.py")

st.markdown("</div>", unsafe_allow_html=True)
