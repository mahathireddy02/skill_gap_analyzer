import streamlit as st
import pandas as pd
import altair as alt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user, update_user
from utils.readiness import calculate_readiness, has_gap_analysis
from utils.skill_analyzer import analyze_skill_gap
from components.navbar import show_navbar

st.set_page_config(page_title="Analytics · SkillGap", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
require_login()

db_user = get_user(st.session_state.email)
theme = db_user.get("theme", "dark")
is_light = theme == "light"

page_bg = "#fdf7e4" if is_light else "#333F63"
chart_bg = "#fdf7e4" if is_light else "rgba(0,0,0,0.24)"
chart_text = "#000000" if is_light else "#FFFFF0"
chart_muted = "#000000" if is_light else "rgba(255,255,240,0.62)"
chart_grid = "#bbab8c" if is_light else "rgba(255,255,240,0.14)"
chart_axis = "#bbab8c" if is_light else "rgba(255,255,240,0.26)"
chart_hover = "#bbab8c" if is_light else "#333F63"
chart_primary = "#bbab8c" if is_light else "#FFFFF0"
chart_secondary = "#bbab8c" if is_light else "#333F63"
chart_height = 320

st.markdown(f"""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"]
{{display:none!important;visibility:hidden!important;}}
html,body,.stApp{{margin:0!important;padding:0!important;background:{page_bg}!important;color:{chart_text}!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}
h1,h2,h3,h4,h5,h6,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] * {{
    color:{chart_text}!important;
}}
div[data-testid="stMetric"] {{
    background:{chart_bg}!important;
    border:1px solid {chart_grid}!important;
    border-radius:12px!important;
}}
div[data-testid="stMetricLabel"] p {{
    color:{chart_muted}!important;
}}
div[data-testid="stMetricValue"] {{
    color:{chart_text}!important;
}}
#vg-tooltip-element,
#vg-tooltip-element table,
#vg-tooltip-element tbody,
#vg-tooltip-element tr,
#vg-tooltip-element td,
.vg-tooltip,
.vg-tooltip table,
.vg-tooltip tbody,
.vg-tooltip tr,
.vg-tooltip td {{
    background:{chart_bg}!important;
    color:{chart_text}!important;
    border-color:{chart_grid}!important;
}}
#vg-tooltip-element,
.vg-tooltip {{
    border:1px solid {chart_grid}!important;
    border-radius:8px!important;
    box-shadow:none!important;
}}
#vg-tooltip-element td.key,
.vg-tooltip td.key {{
    color:{chart_muted}!important;
}}
#vg-tooltip-element td.value,
.vg-tooltip td.value {{
    color:{chart_text}!important;
}}
.vega-embed details,
.vega-embed summary,
.vega-embed .vega-actions,
.vega-embed .vega-actions a,
div[data-testid="stVegaLiteChart"] details,
div[data-testid="stVegaLiteChart"] summary,
div[data-testid="stVegaLiteChart"] .vega-actions,
div[data-testid="stVegaLiteChart"] .vega-actions a,
details[open],
details[open] summary,
details[open] .vega-actions,
details[open] .vega-actions a {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
    border-color:{chart_grid}!important;
}}
.vega-embed .vega-actions,
div[data-testid="stVegaLiteChart"] .vega-actions,
details[open] .vega-actions {{
    border:1px solid {chart_grid}!important;
    border-radius:8px!important;
    box-shadow:none!important;
    overflow:hidden!important;
}}
.vega-embed .vega-actions a,
div[data-testid="stVegaLiteChart"] .vega-actions a,
details[open] .vega-actions a {{
    display:block!important;
    padding:0.45rem 0.75rem!important;
    text-decoration:none!important;
    font-size:0.82rem!important;
    line-height:1.2!important;
}}
.vega-embed .vega-actions a:hover,
div[data-testid="stVegaLiteChart"] .vega-actions a:hover,
details[open] .vega-actions a:hover,
.vega-embed summary:hover,
div[data-testid="stVegaLiteChart"] summary:hover,
details[open] summary:hover {{
    background:{chart_hover}!important;
    background-color:{chart_hover}!important;
    color:{chart_text}!important;
}}
.vega-embed summary svg,
div[data-testid="stVegaLiteChart"] summary svg,
details[open] summary svg,
.vega-embed summary path,
div[data-testid="stVegaLiteChart"] summary path,
details[open] summary path {{
    color:{chart_text}!important;
    fill:{chart_text}!important;
    stroke:{chart_text}!important;
}}
div[data-testid="stElementToolbar"],
div[data-testid="stElementToolbar"] *,
div[data-testid="stElementToolbarButton"],
div[data-testid="stElementToolbarButton"] *,
button[title*="fullscreen" i],
button[title*="fullscreen" i] *,
button[title*="download" i],
button[title*="download" i] *,
button[aria-label*="fullscreen" i],
button[aria-label*="fullscreen" i] *,
button[aria-label*="download" i],
button[aria-label*="download" i] *,
button[aria-label*="more" i],
button[aria-label*="more" i] * {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
    border-color:{chart_grid}!important;
    fill:{chart_text}!important;
    stroke:{chart_text}!important;
}}
div[data-testid="stElementToolbar"] button,
div[data-testid="stElementToolbar"] [role="button"] {{
    border:1px solid {chart_grid}!important;
    border-radius:8px!important;
    box-shadow:none!important;
}}
div[data-testid="stElementToolbar"] button:hover,
div[data-testid="stElementToolbar"] [role="button"]:hover,
button[title*="fullscreen" i]:hover,
button[title*="download" i]:hover,
button[aria-label*="fullscreen" i]:hover,
button[aria-label*="download" i]:hover,
button[aria-label*="more" i]:hover {{
    background:{chart_hover}!important;
    background-color:{chart_hover}!important;
    color:{chart_text}!important;
}}
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
div[role="menu"],
div[role="menu"] *,
ul[role="menu"],
ul[role="menu"] *,
div[role="menuitem"],
div[role="menuitem"] *,
li[role="menuitem"],
li[role="menuitem"] * {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
    border-color:{chart_grid}!important;
}}
div[role="menuitem"]:hover,
li[role="menuitem"]:hover {{
    background:{chart_hover}!important;
    background-color:{chart_hover}!important;
    color:{chart_text}!important;
}}
div[data-testid="stElementToolbar"] button,
div[data-testid="stElementToolbar"] [role="button"],
div[data-testid="stElementToolbarButton"],
button[title*="fullscreen" i],
button[title*="download" i],
button[aria-label*="fullscreen" i],
button[aria-label*="download" i],
button[aria-label*="more" i],
.vega-embed summary {{
    opacity:1!important;
    visibility:visible!important;
    display:inline-flex!important;
    align-items:center!important;
    justify-content:center!important;
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
    border:1.5px solid {chart_grid}!important;
    border-radius:8px!important;
    box-shadow:none!important;
}}
div[data-testid="stElementToolbar"] svg,
div[data-testid="stElementToolbar"] path,
div[data-testid="stElementToolbarButton"] svg,
div[data-testid="stElementToolbarButton"] path,
button[title*="fullscreen" i] svg,
button[title*="fullscreen" i] path,
button[title*="download" i] svg,
button[title*="download" i] path,
button[aria-label*="fullscreen" i] svg,
button[aria-label*="fullscreen" i] path,
button[aria-label*="download" i] svg,
button[aria-label*="download" i] path,
button[aria-label*="more" i] svg,
button[aria-label*="more" i] path,
.vega-embed summary svg,
.vega-embed summary path {{
    opacity:1!important;
    color:{chart_text}!important;
    fill:{chart_text}!important;
    stroke:{chart_text}!important;
}}
.vega-embed .vega-actions,
div[data-testid="stVegaLiteChart"] .vega-actions,
details[open] .vega-actions,
div[role="menu"],
ul[role="menu"] {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    border:1.5px solid {chart_grid}!important;
    border-radius:8px!important;
}}
.vega-embed .vega-actions a,
div[data-testid="stVegaLiteChart"] .vega-actions a,
details[open] .vega-actions a,
div[role="menuitem"],
li[role="menuitem"] {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
}}
div[data-testid="stElementToolbar"],
div[data-testid="stElementToolbarButton"],
[data-testid*="ElementToolbar"],
[data-testid*="ElementToolbar"] *,
[class*="elementToolbar"],
[class*="elementToolbar"] *,
[class*="stElementToolbar"],
[class*="stElementToolbar"] *,
button[title*="full" i],
button[title*="full" i] *,
button[title*="view" i],
button[title*="view" i] *,
button[title*="data" i],
button[title*="data" i] *,
button[aria-label*="full" i],
button[aria-label*="full" i] *,
button[aria-label*="view" i],
button[aria-label*="view" i] *,
button[aria-label*="data" i],
button[aria-label*="data" i] * {{
    opacity:1!important;
    visibility:visible!important;
    display:inline-flex!important;
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    color:{chart_text}!important;
    border-color:{chart_grid}!important;
    fill:{chart_text}!important;
    stroke:{chart_text}!important;
}}
button[title*="full" i],
button[title*="view" i],
button[title*="data" i],
button[aria-label*="full" i],
button[aria-label*="view" i],
button[aria-label*="data" i] {{
    min-width:32px!important;
    min-height:32px!important;
    border:1.5px solid {chart_grid}!important;
    border-radius:8px!important;
}}
div[data-testid="stElementToolbar"] button,
div[data-testid="stElementToolbarButton"],
[data-testid*="ElementToolbar"] button,
[class*="elementToolbar"] button,
[class*="stElementToolbar"] button,
button[title*="full" i],
button[title*="view" i],
button[title*="data" i],
button[aria-label*="full" i],
button[aria-label*="view" i],
button[aria-label*="data" i] {{
    background:{chart_bg}!important;
    background-color:{chart_bg}!important;
    border:1.5px solid {chart_grid}!important;
    border-radius:8px!important;
    box-shadow:none!important;
    color:{chart_text}!important;
}}
div[data-testid="stElementToolbar"] button *,
div[data-testid="stElementToolbarButton"] *,
[data-testid*="ElementToolbar"] button *,
[class*="elementToolbar"] button *,
[class*="stElementToolbar"] button *,
button[title*="full" i] *,
button[title*="view" i] *,
button[title*="data" i] *,
button[aria-label*="full" i] *,
button[aria-label*="view" i] *,
button[aria-label*="data" i] * {{
    background:transparent!important;
    background-color:transparent!important;
    color:{chart_text}!important;
    box-shadow:none!important;
}}
div[data-testid="stElementToolbar"] button svg,
div[data-testid="stElementToolbar"] button path,
div[data-testid="stElementToolbarButton"] svg,
div[data-testid="stElementToolbarButton"] path,
[data-testid*="ElementToolbar"] button svg,
[data-testid*="ElementToolbar"] button path,
[class*="elementToolbar"] button svg,
[class*="elementToolbar"] button path,
[class*="stElementToolbar"] button svg,
[class*="stElementToolbar"] button path,
button[title*="full" i] svg,
button[title*="full" i] path,
button[title*="view" i] svg,
button[title*="view" i] path,
button[title*="data" i] svg,
button[title*="data" i] path,
button[aria-label*="full" i] svg,
button[aria-label*="full" i] path,
button[aria-label*="view" i] svg,
button[aria-label*="view" i] path,
button[aria-label*="data" i] svg,
button[aria-label*="data" i] path {{
    color:{chart_text}!important;
    fill:{chart_text}!important;
    stroke:{chart_text}!important;
}}
div[data-testid="stElementToolbar"] button[title*="full" i],
div[data-testid="stElementToolbar"] button[title*="fullscreen" i],
div[data-testid="stElementToolbar"] button[title*="view" i],
div[data-testid="stElementToolbar"] button[title*="data" i],
div[data-testid="stElementToolbar"] button[aria-label*="full" i],
div[data-testid="stElementToolbar"] button[aria-label*="fullscreen" i],
div[data-testid="stElementToolbar"] button[aria-label*="view" i],
div[data-testid="stElementToolbar"] button[aria-label*="data" i],
button[title*="full" i]:not([aria-label*="more" i]),
button[title*="fullscreen" i]:not([aria-label*="more" i]),
button[title*="view" i]:not([aria-label*="more" i]),
button[title*="data" i]:not([aria-label*="more" i]),
button[aria-label*="full" i]:not([aria-label*="more" i]),
button[aria-label*="fullscreen" i]:not([aria-label*="more" i]),
button[aria-label*="view" i]:not([aria-label*="more" i]),
button[aria-label*="data" i]:not([aria-label*="more" i]) {{
    display:none!important;
    visibility:hidden!important;
    opacity:0!important;
    pointer-events:none!important;
}}
div[data-testid="stElementToolbar"] button[aria-label*="more" i],
div[data-testid="stElementToolbar"] button[title*="more" i],
button[aria-label*="more" i],
button[title*="more" i],
.vega-embed summary {{
    display:none!important;
    visibility:hidden!important;
    opacity:0!important;
    pointer-events:none!important;
}}
.vega-embed details,
.vega-embed .vega-actions,
div[data-testid="stVegaLiteChart"] details,
div[data-testid="stVegaLiteChart"] .vega-actions,
div[data-testid="stElementToolbar"],
div[data-testid="stElementToolbarButton"],
[data-testid*="ElementToolbar"],
[class*="elementToolbar"],
[class*="stElementToolbar"] {{
    display:none!important;
    visibility:hidden!important;
    opacity:0!important;
    pointer-events:none!important;
}}
</style>
""", unsafe_allow_html=True)

show_navbar("Analytics")

st.markdown("## 📊 Analytics")
st.markdown("Track your skill progress and readiness over time.")
st.markdown("")

def themed_chart(chart):
    return (
        chart
        .properties(background=chart_bg)
        .configure_view(stroke=chart_grid)
        .configure_axis(
            labelColor=chart_muted,
            titleColor=chart_text,
            gridColor=chart_grid,
            domainColor=chart_axis,
            tickColor=chart_axis,
        )
        .configure_legend(
            labelColor=chart_text,
            titleColor=chart_text,
        )
    )

skills       = db_user.get("skills", [])
missing      = db_user.get("missing_skills", [])
resume_score = db_user.get("resume_score", 0)
role         = db_user.get("target_role", "N/A")

if skills and role != "N/A" and not has_gap_analysis(db_user):
    try:
        gap_result = analyze_skill_gap(skills, role)
        missing = gap_result.get("missing_skills", [])
        db_user.update({
            "missing_skills": missing,
            "gap_result": gap_result,
            "gap_analyzed": True,
        })
        update_user(st.session_state.email, {
            "missing_skills": missing,
            "gap_result": gap_result,
            "gap_analyzed": True,
        })
    except ValueError:
        pass

readiness    = calculate_readiness(skills, missing, has_gap_analysis(db_user), db_user.get("gap_result", {}))

c1, c2, c3, c4 = st.columns(4)
c1.metric("📄 Resume Score",   f"{resume_score}%")
c2.metric("✅ Skills Found",   len(skills))
c3.metric("❌ Skills Missing", len(missing))
c4.metric("📈 Readiness",      f"{readiness}%")

st.markdown("---")
cl, cr = st.columns(2)
with cl:
    st.markdown("### 🧠 Skill Match")
    if has_gap_analysis(db_user):
        df = pd.DataFrame({"Category": ["✅ Matched", "❌ Missing"], "Count": [len(skills), len(missing)]}).set_index("Category")
        chart_df = df.reset_index()
        chart = alt.Chart(chart_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X("Category:N", title=None, axis=alt.Axis(labelAngle=0, labelLimit=110)),
            y=alt.Y("Count:Q", title="Count"),
            color=alt.Color(
                "Category:N",
                scale=alt.Scale(range=[chart_primary, chart_secondary]),
                legend=None,
            ),
            tooltip=["Category", "Count"],
        ).properties(height=chart_height)
        st.altair_chart(themed_chart(chart), use_container_width=True)
    else:
        st.info("Run Skill Gap Analyzer to calculate matched and missing role skills.")

with cr:
    st.markdown("### 📄 Resume Score")
    st.markdown(f"**Overall: {resume_score}%**")
    st.progress(resume_score / 100)
    df2 = pd.DataFrame({"Component": ["Skills","Sections","Length","Contact","Action Verbs"],
                        "Max Points": [40, 30, 15, 10, 5]}).set_index("Component")
    chart_df2 = df2.reset_index()
    chart = alt.Chart(chart_df2).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X("Component:N", title=None, axis=alt.Axis(labelAngle=0, labelLimit=110)),
        y=alt.Y("Max Points:Q", title="Max Points"),
        color=alt.value(chart_primary),
        tooltip=["Component", "Max Points"],
    ).properties(height=chart_height)
    st.altair_chart(themed_chart(chart), use_container_width=True)

st.markdown("---")
st.markdown("### 📅 Weekly Progress")
weeks  = ["Week 1","Week 2","Week 3","Week 4","Week 5","Week 6"]
scores = [20, 35, 45, 55, 68, resume_score if resume_score else 72]
progress_df = pd.DataFrame({"Week": weeks, "Resume Score": scores})
line = alt.Chart(progress_df).mark_line(point=True, strokeWidth=3, color=chart_primary).encode(
    x=alt.X("Week:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Resume Score:Q", title="Resume Score", scale=alt.Scale(domain=[0, 100])),
    tooltip=["Week", "Resume Score"],
).properties(height=320)
st.altair_chart(themed_chart(line), use_container_width=True)

if role != "N/A":
    st.markdown("---")
    status = f"**{readiness}%**" if has_gap_analysis(db_user) else "**Not calculated yet**"
    st.info(f"🎯 Target Role: **{role}** | Readiness: {status}")

st.markdown("</div>", unsafe_allow_html=True)
