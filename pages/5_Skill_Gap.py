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
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
.chip-g{display:inline-block;background:#d1fae5;color:#065f46;border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.chip-r{display:inline-block;background:#fee2e2;color:#991b1b;border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.chip-y{display:inline-block;background:#fef3c7;color:#92400e;border-radius:999px;
    padding:0.2rem 0.65rem;font-size:0.8rem;font-weight:600;margin:0.15rem;}
.tier-box{background:rgba(124,58,237,0.1);border-radius:12px;padding:0.8rem 1rem;margin-bottom:0.5rem;
    border-left:4px solid #4f46e5;}
</style>
""", unsafe_allow_html=True)

show_navbar("Skill Gap")

st.markdown("## 🧠 Skill Gap Analyzer")
st.markdown("")

db_user     = get_user(st.session_state.email)
user_skills = db_user.get("skills", [])
target_role = db_user.get("target_role", "").strip()

if not target_role:
    st.warning("⚠️ No target role set. Please update it in your Profile.")
    if st.button("👤 Go to Profile", type="primary"):
        st.switch_page("pages/8_Profile.py")
    st.stop()

st.markdown(
    f'<div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);'
    f'border-radius:10px;padding:0.5rem 1rem;font-size:0.9rem;margin-bottom:1rem;">'
    f'🎯 Analyzing for: <strong>{target_role}</strong> '
    f'<span style="font-size:0.75rem;opacity:0.5;">(✏️ change in Profile)</span></div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:

    if not user_skills:
        st.warning("⚠️ No skills detected from resume.")
        manual = st.text_input("Enter your skills manually (comma-separated)",
                               placeholder="e.g. Python, SQL, Excel")
        if st.button("🔍 Analyze Gap", type="primary", use_container_width=True):
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
                        })
                        st.session_state["gap_result"] = result
                    except ValueError as e:
                        st.error(f"❌ {e}")
                        st.info(f"Supported roles: {', '.join(get_roles())}")
    else:
        st.markdown(f"**Your skills:** {len(user_skills)} detected")
        if st.button("🔍 Analyze Gap", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                try:
                    result = analyze_skill_gap(user_skills, target_role)
                    update_user(st.session_state.email, {
                        "target_role":    target_role,
                        "missing_skills": result["missing_skills"],
                    })
                    st.session_state["gap_result"] = result
                except ValueError as e:
                    st.error(f"❌ {e}")
                    st.info(f"Supported roles: {', '.join(get_roles())}")

    st.markdown("---")
    st.markdown("### 💡 Best Role Matches")
    if user_skills:
        suggestions = suggest_roles(user_skills, top_n=3)
        for s in suggestions:
            grade_color = "#059669" if s["score"] >= 65 else "#d97706" if s["score"] >= 40 else "#dc2626"
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);'
                f'border-radius:10px;padding:0.5rem 0.8rem;margin-bottom:0.4rem;">'
                f'<span style="font-weight:600;font-size:0.88rem;">{s["role"]}</span>'
                f'<span style="font-weight:800;color:{grade_color};font-size:0.9rem;">'
                f'{s["score"]}% ({s["grade"]})</span></div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Upload your resume to see role suggestions.")

with col2:
    if "gap_result" in st.session_state:
        r = st.session_state["gap_result"]

        # ── Score Header ──────────────────────────────────────────────────
        score = r["score"]
        grade = r["grade"]
        color = "#059669" if score >= 65 else "#d97706" if score >= 40 else "#dc2626"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:16px;
                    padding:1.2rem 1.8rem;color:white;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:0.85rem;opacity:0.8;">Match Score for</div>
                    <div style="font-size:1.3rem;font-weight:800;">{r['role']}</div>
                    <div style="font-size:0.82rem;opacity:0.75;margin-top:0.2rem;">{r['role_description']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:3rem;font-weight:900;line-height:1;">{score}%</div>
                    <div style="font-size:1.2rem;font-weight:700;">Grade: {grade}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Tier Breakdown ────────────────────────────────────────────────
        st.markdown("#### 📊 Skill Tier Coverage")
        t1, t2, t3 = st.columns(3)
        tier_data = r.get("tier_breakdown", {})
        for col, (tier, label, color_t) in zip(
            [t1, t2, t3],
            [("core", "🔴 Core Skills", "#dc2626"),
             ("important", "🟡 Important", "#d97706"),
             ("nice_to_have", "🟢 Nice to Have", "#059669")]
        ):
            td = tier_data.get(tier, {})
            cov = td.get("coverage", 0)
            with col:
                st.markdown(
                    f'<div class="tier-box"><div style="font-size:0.8rem;font-weight:700;color:{color_t};">'
                    f'{label}</div><div style="font-size:1.6rem;font-weight:900;">{cov}%</div>'
                    f'<div style="font-size:0.75rem;color:#6b7280;">{td.get("matched",0)}/{td.get("total",0)} skills</div></div>',
                    unsafe_allow_html=True
                )

        st.markdown("")

        # ── Matched / Missing ─────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ✅ Matched Skills")
            if r["matched_skills"]:
                chips = "".join(f'<span class="chip-g">✅ {s.title()}</span>' for s in r["matched_skills"])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.info("No matching skills yet.")

        with c2:
            st.markdown("#### ❌ Missing Skills")
            if r["missing_skills"]:
                chips = "".join(f'<span class="chip-r">❌ {s.title()}</span>' for s in r["missing_skills"])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.success("🎉 You have all required skills!")

        # ── Partial Matches ───────────────────────────────────────────────
        if r.get("partial_matches"):
            st.markdown("#### 🟡 Partial Matches (Close but not exact)")
            for pm in r["partial_matches"]:
                st.markdown(
                    f'<span class="chip-y">~{pm["required"].title()} '
                    f'(you have: {pm["user_has"]}, {int(pm["similarity"]*100)}% match)</span>',
                    unsafe_allow_html=True
                )
            st.markdown("")

        # ── Recommendations ───────────────────────────────────────────────
        if r["recommendations"]:
            st.markdown("#### 🎯 Priority Skills to Learn")
            st.markdown("*In order of importance for this role:*")
            for i, skill in enumerate(r["recommendations"][:6], 1):
                st.markdown(f"**{i}.** {skill.title()}")

        st.markdown("")
        if r["missing_skills"]:
            if st.button("🛤️ Generate Personalized Roadmap", type="primary", use_container_width=True):
                st.switch_page("pages/6_Roadmap.py")

st.markdown("</div>", unsafe_allow_html=True)
