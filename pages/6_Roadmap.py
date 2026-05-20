import streamlit as st
import streamlit.components.v1 as components
import json, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.roadmap_generator import generate_roadmap
from components.navbar import show_navbar

st.set_page_config(page_title="Roadmap · SkillGap", page_icon="🛤️", layout="wide", initial_sidebar_state="collapsed")
require_login()

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body,.stApp{margin:0!important;padding:0!important;background:#0a0e17!important;}
.block-container{padding:1rem 2rem!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
div[data-testid="stMetric"]{background:rgba(255,255,255,0.05);border-radius:12px;padding:0.8rem 1rem;border:1px solid rgba(255,255,255,0.08);}
div[data-testid="stMetric"] label{color:rgba(255,255,255,0.5)!important;}
div[data-testid="stMetric"] div{color:#fff!important;}
</style>
""", unsafe_allow_html=True)

show_navbar("Roadmap")

db_user = get_user(st.session_state.email)
role    = db_user.get("target_role", "").strip()

# Always use freshest missing_skills tied to the current role
# Priority: live gap_result in session > saved gap_result in DB > saved missing_skills
_gap = st.session_state.get("gap_result") or db_user.get("gap_result", {})
if _gap and _gap.get("role", "").lower() == role.lower():
    missing = _gap.get("missing_skills", [])
else:
    missing = db_user.get("missing_skills", [])

# Pull signup/profile preferences as defaults
_time_map  = {"Less than 5 hrs": 3.5, "5–10 hrs": 7.0, "10+ hrs": 12.0}
_exp_eff   = {"Student": 1.0, "Fresher": 0.9, "Working Professional": 0.7}
_saved_time  = db_user.get("time_availability", "5–10 hrs")
_saved_level = db_user.get("skill_level", "Beginner")
_saved_exp   = db_user.get("experience_type", "Student")
_default_hpw = round(_time_map.get(_saved_time, 7.0) * _exp_eff.get(_saved_exp, 1.0), 1)
_default_hpd = min(round(_default_hpw / 7, 1), 8.0)
_level_opts  = ["Beginner", "Intermediate", "Advanced"]
_level_idx   = _level_opts.index(_saved_level) if _saved_level in _level_opts else 0

if not role:
    st.info("No target role set. Run the Skill Gap Analyzer first.")
    if st.button("Go to Skill Gap Analyzer", type="primary"):
        st.switch_page("pages/5_Skill_Gap.py")
    st.stop()

if not missing:
    st.success(f"🎉 You already have all required skills for **{role}**! No roadmap needed.")
    if st.button("Re-run Skill Gap Analyzer", type="primary"):
        st.switch_page("pages/5_Skill_Gap.py")
    st.stop()

if "checked_weeks" not in st.session_state:
    saved = db_user.get("checked_weeks", [])
    st.session_state.checked_weeks = set(saved)

if "roadmap_result" not in st.session_state and db_user.get("roadmap_result"):
    saved_rm = db_user["roadmap_result"]
    # Only restore if it was generated for the same role and same missing skills
    # DO NOT restore old roadmaps - force regeneration for fresh customization
    if False:  # Disabled - always force fresh generation
        if (saved_rm.get("role", "").lower() == role.lower() and
                set(saved_rm.get("phase_plan") and
                    [p["skill"] for p in saved_rm["phase_plan"]] or []) ==
                set(s.lower() for s in missing)):
            st.session_state["roadmap_result"] = saved_rm

st.markdown("## 🛤️ Learning Roadmap")
st.caption(f"Target Role: **{role}** · {len(missing)} skills to learn")

# ── Settings Form ─────────────────────────────────────────────────────────────
with st.expander("⚙️ Customize Roadmap", expanded="roadmap_result" not in st.session_state):
    st.markdown(
        f'<div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.2);'
        f'border-radius:8px;padding:0.4rem 0.9rem;font-size:0.82rem;color:#a78bfa;margin-bottom:0.8rem;">'
        f'ℹ️ Pre-filled from your profile — <strong>{_saved_level}</strong>, '
        f'<strong>{_saved_time}</strong>/week, <strong>{_saved_exp}</strong>. Adjust if needed.</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        skill_level   = st.selectbox("Your Level", _level_opts, index=_level_idx)
        hours_per_day = st.slider("Hours/day", 0.5, 8.0, _default_hpd, 0.5)
    with c2:
        deadline_months = st.selectbox("Timeline", [1,2,3,6,9,12], index=2,
                            format_func=lambda x: f"{x} month{'s' if x>1 else ''}")
        budget = st.radio("Budget", ["free","paid"],
                    format_func=lambda x: "Free" if x=="free" else "Paid OK", horizontal=True)
    with c3:
        learning_style = st.selectbox("Learning Style",
                            ["mixed","videos","projects","docs","courses"],
                            format_func=lambda x: {"mixed":"Mixed","videos":"Videos (YouTube)",
                                "projects":"Project-based","docs":"Documentation","courses":"Courses"}[x])
        interests = st.text_input("Interests (optional)", placeholder="e.g. finance, gaming")

    if st.button("Generate Roadmap", type="primary", use_container_width=True):
        with st.spinner("Building your personalized roadmap..."):
            result = generate_roadmap(
                role=role, missing_skills=missing,
                skill_level=skill_level.lower(),
                hours_per_week=hours_per_day * 7,
                deadline_months=deadline_months,
                learning_style=learning_style,
                budget=budget, interests=interests,
            )
            st.session_state["roadmap_result"] = result
            st.session_state.checked_weeks = set()
            from utils.auth import update_user
            update_user(st.session_state.email, {"roadmap_result": result, "checked_weeks": []})
        st.rerun()

if "roadmap_result" not in st.session_state:
    st.stop()

rm = st.session_state["roadmap_result"]
tl          = rm.get("timeline", {})
phases      = rm.get("phase_plan", [])
weekly      = rm.get("weekly_plan", [])
checked     = st.session_state.checked_weeks
total_weeks = tl.get("total_weeks", 0)

done_weeks  = len(checked)
pct         = int(done_weeks / total_weeks * 100) if total_weeks else 0
current_week = done_weeks + 1

# ── Metrics ───────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Hours",  f"{tl.get('total_hours',0)}h")
m2.metric("Total Weeks",  f"{total_weeks}w")
m3.metric("Duration",     f"{tl.get('total_months',0)} months")
m4.metric("Progress",     f"{pct}%")
st.markdown("")

# ── Weekly checklist (Streamlit-native, below the map) ────────────────────────
def render_checklist():
    st.markdown("### ✅ Weekly Checklist")
    st.caption(f"{done_weeks} of {total_weeks} weeks completed")
    for phase in phases:
        p_weeks    = list(range(phase["start_week"], phase["end_week"] + 1))
        phase_done = all(w in checked for w in p_weeks)
        with st.expander(
            f"{'✅' if phase_done else '🔵'} {phase['skill'].title()} (Week {phase['start_week']}–{phase['end_week']})",
            expanded=not phase_done
        ):
            for w in p_weeks:
                entry = next((e for e in weekly if e["week"] == w), None)
                if not entry: continue
                is_done  = w in checked
                is_today = w == current_week
                label = (f"✅ Week {w} — {entry['focus']}" if is_done
                         else f"📍 Week {w} — {entry['focus']} ← Today" if is_today
                         else f"Week {w} — {entry['focus']}")
                val = st.checkbox(label, value=is_done, key=f"week_{w}")
                if is_today or is_done:
                    st.caption(entry["tasks"])
                if entry.get("project") and (is_today or is_done):
                    st.caption(f"🏁 Project: {entry['project']}")
                if val != is_done:
                    if val: st.session_state.checked_weeks.add(w)
                    else:   st.session_state.checked_weeks.discard(w)
                    from utils.auth import update_user
                    update_user(st.session_state.email, {"checked_weeks": list(st.session_state.checked_weeks)})
                    st.rerun()

# ── Build station data for JS ─────────────────────────────────────────────────
stations = []
for phase in phases:
    p_weeks  = list(range(phase["start_week"], phase["end_week"] + 1))
    all_done = all(w in checked for w in p_weeks)
    is_active = current_week in p_weeks
    status = "done" if all_done else "active" if is_active else "upcoming"
    resources_html = "".join(f"<li>{r}</li>" for r in phase["resources"])
    phases_html = "".join(
        f'<div class="ph-row"><span class="ph-badge ph-{k}">{k.title()}</span><span>{v}</span></div>'
        for k, v in phase["phases"].items()
    )
    stations.append({
        "id":       phase["phase_num"],
        "skill":    phase["skill"].title(),
        "status":   status,
        "weeks":    f"Week {phase['start_week']}–{phase['end_week']}",
        "hours":    phase["hours"],
        "project":  phase.get("project", ""),
        "resources_html": resources_html,
        "phases_html":    phases_html,
    })

stations_json = json.dumps(stations)
train_pos     = (done_weeks / total_weeks) if total_weeks else 0
n_stations    = len(stations)
# Each station needs ~200px min; clamp between 900 and 6000
svg_width     = max(900, n_stations * 200)

# ── HTML/SVG Journey Map ──────────────────────────────────────────────────────
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:#fff;font-family:'Inter',system-ui,sans-serif;color:#333;overflow-x:hidden;}}
  #map-wrap{{width:100%;overflow-x:auto;overflow-y:visible;padding:20px 0 10px;-webkit-overflow-scrolling:touch;}}
  #map-wrap::-webkit-scrollbar{{height:4px;}}
  #map-wrap::-webkit-scrollbar-track{{background:rgba(255,255,255,0.04);}}
  #map-wrap::-webkit-scrollbar-thumb{{background:#4338ca;border-radius:4px;}}
  #journey-svg{{display:block;min-width:{svg_width}px;}}

  /* Station circles */
  .station-done   .s-circle{{fill:#10b981;stroke:#34d399;filter:drop-shadow(0 0 8px #10b98188);}}
  .station-active .s-circle{{fill:#7c3aed;stroke:#a78bfa;filter:drop-shadow(0 0 14px #7c3aedaa);animation:pulse 1.6s ease-in-out infinite;}}
  .station-upcoming .s-circle{{fill:#1e1b4b;stroke:#4338ca;}}
  @keyframes pulse{{0%,100%{{r:18;}}50%{{r:22;}}}}

  .station-done   .s-icon{{fill:#fff;font-size:14px;}}
  .station-active .s-icon{{fill:#000;font-size:14px;}}
  .station-upcoming .s-icon{{fill:#555;font-size:14px;}}

  .s-label{{font-size:12px;font-weight:700;fill:#000;text-anchor:middle;}}
  .s-weeks{{font-size:10px;fill:#000;text-anchor:middle;}}

  .station-group{{cursor:pointer;transition:transform .2s;}}
  .station-group:hover .s-circle{{stroke-width:3;}}

  /* Track */
  .track-bg{{stroke:#ccc;stroke-width:8;fill:none;stroke-linecap:round;}}
  .track-done{{stroke:url(#trackGrad);stroke-width:8;fill:none;stroke-linecap:round;stroke-dasharray:var(--dash);stroke-dashoffset:0;transition:stroke-dasharray 1s ease;}}
  .track-rail{{stroke:#eee;stroke-width:2;fill:none;stroke-dasharray:12 18;}}

  /* Train */
  #train{{transition:all 1.2s cubic-bezier(.4,0,.2,1);}}
  #train-glow{{filter:drop-shadow(0 0 8px #0000cc88);}}

  /* Detail panel */
  #detail{{
    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.92);
    background:#fff;
    border:1px solid #ccc;
    border-radius:20px;padding:24px 28px;width:min(520px,90vw);
    max-height:80vh;overflow-y:auto;
    box-shadow:0 12px 40px rgba(0,0,0,0.2);
    opacity:0;pointer-events:none;
    transition:all .25s cubic-bezier(.4,0,.2,1);
    z-index:9999;
  }}
  #detail.open{{opacity:1;pointer-events:all;transform:translate(-50%,-50%) scale(1);}}
  #overlay{{position:fixed;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);
    opacity:0;pointer-events:none;transition:opacity .25s;z-index:9998;}}
  #overlay.open{{opacity:1;pointer-events:all;}}

  .d-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;}}
  .d-title{{font-size:1.25rem;font-weight:800;}}
  .d-close{{background:#f0f0f0;border:1px solid #ccc;color:#000;width:32px;height:32px;
    border-radius:50%;cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;}}
  .d-close:hover{{background:#e0e0e0;}}
  .d-badge{{display:inline-block;padding:3px 12px;border-radius:999px;font-size:0.75rem;font-weight:700;margin-bottom:14px;}}
  .badge-done{{background:#e6ffe6;color:#006600;border:1px solid #ccffcc;}}
  .badge-active{{background:#e6e6ff;color:#0000cc;border:1px solid #ccccff;}}
  .badge-upcoming{{background:#f0f0f0;color:#333333;border:1px solid #cccccc;}}
  .d-meta{{color:#000;font-size:0.85rem;margin-bottom:16px;}}
  .ph-row{{display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;font-size:0.83rem;line-height:1.5;color:#000;}}
  .ph-badge{{flex-shrink:0;padding:2px 8px;border-radius:6px;font-size:0.72rem;font-weight:700;margin-top:1px;}}
  .ph-beginner{{background:#e6ffe6;color:#006600;}}
  .ph-intermediate{{background:#fff8e6;color:#cc6600;}}
  .ph-advanced{{background:#ffe6e6;color:#cc0000;}}
  .d-section{{font-size:0.78rem;font-weight:700;color:#000;text-transform:uppercase;letter-spacing:.08em;margin:14px 0 8px;}}
  .d-resources ul{{padding-left:16px;}}
  .d-resources li{{font-size:0.83rem;color:#000;margin-bottom:4px;}}
  .d-project{{background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);
    border-radius:10px;padding:10px 14px;font-size:0.83rem;color:#000;margin-top:12px;}}

  /* Progress bar */
  #prog-wrap{{padding:0 24px 16px;}}
  .prog-label{{display:flex;justify-content:space-between;font-size:0.8rem;color:#555;margin-bottom:6px;}}
  .prog-bar{{height:6px;background:#eee;border-radius:999px;overflow:hidden;}}
  .prog-fill{{height:100%;background:linear-gradient(90deg,#7c3aed,#34d399);border-radius:999px;
    transition:width 1s ease;}}
</style>
</head>
<body>

<div id="prog-wrap">
  <div class="prog-label"><span>🚂 Journey Progress</span><span id="pct-label">{pct}%</span></div>
  <div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>
</div>

<div id="map-wrap">
  <svg id="journey-svg" xmlns="http://www.w3.org/2000/svg"></svg>
</div>

<div id="overlay" onclick="closeDetail()"></div>
<div id="detail">
  <div class="d-header">
    <div class="d-title" id="d-title"></div>
    <button class="d-close" onclick="closeDetail()">✕</button>
  </div>
  <div id="d-badge" class="d-badge"></div>
  <div class="d-meta" id="d-meta"></div>
  <div id="d-phases"></div>
  <div class="d-section">📚 Resources</div>
  <div class="d-resources" id="d-resources"></div>
  <div id="d-project"></div>
</div>

<script>
const STATIONS = {stations_json};
const TRAIN_POS = {train_pos};

const N = STATIONS.length;
const W = {svg_width};
const H = 260;
const PAD = 80;
const CY  = H / 2;

// Generate zigzag Y positions for visual interest
function stationY(i) {{
  if (N <= 1) return CY;
  const amp = Math.min(80, H * 0.28);
  return CY + Math.sin(i * Math.PI * 0.85) * amp;
}}

function stationX(i) {{
  if (N <= 1) return W / 2;
  return PAD + (i / (N - 1)) * (W - PAD * 2);
}}

const pts = STATIONS.map((_, i) => ({{ x: stationX(i), y: stationY(i) }}));

// Build smooth cubic bezier path through all points
function buildPath(points) {{
  if (points.length === 1) return `M ${{points[0].x}} ${{points[0].y}}`;
  let d = `M ${{points[0].x}} ${{points[0].y}}`;
  for (let i = 0; i < points.length - 1; i++) {{
    const p0 = points[i], p1 = points[i+1];
    const cx = (p0.x + p1.x) / 2;
    d += ` C ${{cx}} ${{p0.y}}, ${{cx}} ${{p1.y}}, ${{p1.x}} ${{p1.y}}`;
  }}
  return d;
}}

const pathD = buildPath(pts);

const svg = document.getElementById('journey-svg');
svg.setAttribute('width', W);
svg.setAttribute('height', H);
svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);

// Defs
svg.innerHTML = `
<defs>
  <linearGradient id="trackGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#7c3aed"/>
    <stop offset="100%" stop-color="#10b981"/>
  </linearGradient>
  <radialGradient id="trainGrad" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#e0d7ff"/>
    <stop offset="100%" stop-color="#7c3aed"/>
  </radialGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>`;

// Track background
const trackBg = document.createElementNS('http://www.w3.org/2000/svg','path');
trackBg.setAttribute('d', pathD);
trackBg.setAttribute('class','track-bg');
svg.appendChild(trackBg);

// Rail dashes (decorative)
const rail = document.createElementNS('http://www.w3.org/2000/svg','path');
rail.setAttribute('d', pathD);
rail.setAttribute('class','track-rail');
svg.appendChild(rail);

// Completed track (animated fill)
const trackDone = document.createElementNS('http://www.w3.org/2000/svg','path');
trackDone.setAttribute('d', pathD);
trackDone.setAttribute('class','track-done');
trackDone.setAttribute('id','track-done');
svg.appendChild(trackDone);

// Measure total path length and set dash
const tempPath = document.createElementNS('http://www.w3.org/2000/svg','path');
tempPath.setAttribute('d', pathD);
document.body.appendChild(tempPath);
const totalLen = tempPath.getTotalLength();
document.body.removeChild(tempPath);

const doneLen = totalLen * TRAIN_POS;
trackDone.style.strokeDasharray = `${{doneLen}} ${{totalLen}}`;

// Stations
STATIONS.forEach((s, i) => {{
  const x = pts[i].x, y = pts[i].y;
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class', `station-group station-${{s.status}}`);
  g.setAttribute('transform', `translate(${{x}},${{y}})`);
  g.setAttribute('data-id', i);
  g.style.cursor = 'pointer';

  // Outer ring for active
  if (s.status === 'active') {{
    const ring = document.createElementNS('http://www.w3.org/2000/svg','circle');
    ring.setAttribute('r','28');
    ring.setAttribute('fill','none');
    ring.setAttribute('stroke','#7c3aed');
    ring.setAttribute('stroke-width','2');
    ring.setAttribute('opacity','0.4');
    ring.style.animation = 'pulse-ring 1.6s ease-in-out infinite';
    g.appendChild(ring);
  }}

  const circle = document.createElementNS('http://www.w3.org/2000/svg','circle');
  circle.setAttribute('r','18');
  circle.setAttribute('class','s-circle');
  circle.setAttribute('stroke-width','2');
  g.appendChild(circle);

  // Icon text
  const icon = document.createElementNS('http://www.w3.org/2000/svg','text');
  icon.setAttribute('text-anchor','middle');
  icon.setAttribute('dominant-baseline','central');
  icon.setAttribute('font-size','13');
  icon.setAttribute('class','s-icon');
  icon.textContent = s.status==='done' ? '✓' : s.status==='active' ? '▶' : String(s.id);
  g.appendChild(icon);

  // Label below
  const labelY = y > CY ? -32 : 32;
  const lbl = document.createElementNS('http://www.w3.org/2000/svg','text');
  lbl.setAttribute('y', labelY);
  lbl.setAttribute('class','s-label');
  lbl.textContent = s.skill.length > 12 ? s.skill.slice(0,11)+'…' : s.skill;
  g.appendChild(lbl);

  const wk = document.createElementNS('http://www.w3.org/2000/svg','text');
  wk.setAttribute('y', labelY + 14);
  wk.setAttribute('class','s-weeks');
  wk.textContent = s.weeks;
  g.appendChild(wk);

  g.addEventListener('click', () => openDetail(i));
  svg.appendChild(g);
}});

// Goal flag at the end of the track
const lastX = pts[N-1].x + 40;
const lastY = pts[N-1].y;
const flagG = document.createElementNS('http://www.w3.org/2000/svg','g');
flagG.setAttribute('transform', `translate(${{lastX}},${{lastY}})`);

const flagPole = document.createElementNS('http://www.w3.org/2000/svg','line');
flagPole.setAttribute('x1','0'); flagPole.setAttribute('y1','-30');
flagPole.setAttribute('x2','0'); flagPole.setAttribute('y2','20');
flagPole.setAttribute('stroke','#fbbf24'); flagPole.setAttribute('stroke-width','2.5');
flagG.appendChild(flagPole);

const flagRect = document.createElementNS('http://www.w3.org/2000/svg','rect');
flagRect.setAttribute('x','0'); flagRect.setAttribute('y','-30');
flagRect.setAttribute('width','22'); flagRect.setAttribute('height','14');
flagRect.setAttribute('fill','#10b981'); flagRect.setAttribute('rx','2');
flagG.appendChild(flagRect);

const goalLbl = document.createElementNS('http://www.w3.org/2000/svg','text');
goalLbl.setAttribute('y','34'); goalLbl.setAttribute('text-anchor','middle');
goalLbl.setAttribute('font-size','10'); goalLbl.setAttribute('fill','#10b981');
goalLbl.setAttribute('font-weight','700');
goalLbl.textContent = '{"🎉 Reached!" if pct == 100 else "Goal Reached"}';
flagG.appendChild(goalLbl);

svg.appendChild(flagG);

// Train dot
const trainGroup = document.createElementNS('http://www.w3.org/2000/svg','g');
trainGroup.setAttribute('id','train');

const trainGlow = document.createElementNS('http://www.w3.org/2000/svg','circle');
trainGlow.setAttribute('r','14');
trainGlow.setAttribute('fill','rgba(167,139,250,0.2)');
trainGroup.appendChild(trainGlow);

const trainBody = document.createElementNS('http://www.w3.org/2000/svg','circle');
trainBody.setAttribute('r','9');
trainBody.setAttribute('fill','url(#trainGrad)');
trainBody.setAttribute('filter','url(#glow)');
trainGroup.appendChild(trainBody);

const trainDot = document.createElementNS('http://www.w3.org/2000/svg','circle');
trainDot.setAttribute('r','4');
trainDot.setAttribute('fill','#fff');
trainGroup.appendChild(trainDot);

svg.appendChild(trainGroup);

// Position train on path
function positionTrain() {{
  const measurePath = document.createElementNS('http://www.w3.org/2000/svg','path');
  measurePath.setAttribute('d', pathD);
  document.body.appendChild(measurePath);
  const len = measurePath.getTotalLength();
  const pt  = measurePath.getPointAtLength(len * Math.min(TRAIN_POS, 0.9999));
  document.body.removeChild(measurePath);
  trainGroup.setAttribute('transform', `translate(${{pt.x}},${{pt.y}})`);
}}
positionTrain();

// Pulse ring animation via style tag
const style = document.createElement('style');
style.textContent = `
  @keyframes pulse-ring {{
    0%,100% {{ r:28; opacity:0.4; }}
    50%      {{ r:34; opacity:0.1; }}
  }}
  @keyframes train-bob {{
    0%,100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-3px); }}
  }}
  #train {{ animation: train-bob 1.8s ease-in-out infinite; }}
`;
document.head.appendChild(style);

// Detail panel
function openDetail(i) {{
  const s = STATIONS[i];
  document.getElementById('d-title').textContent = '🚉 ' + s.skill;
  const badge = document.getElementById('d-badge');
  badge.textContent = s.status === 'done' ? '✅ Completed' : s.status === 'active' ? '🚂 In Progress' : '⏳ Upcoming';
  badge.className = 'd-badge badge-' + s.status;
  document.getElementById('d-meta').textContent = s.weeks + '  ·  ' + s.hours + 'h total';
  document.getElementById('d-phases').innerHTML = s.phases_html;
  document.getElementById('d-resources').innerHTML = '<ul>' + s.resources_html + '</ul>';
  const proj = document.getElementById('d-project');
  proj.innerHTML = s.project ? `<div class="d-project">🛠️ <strong>Mini Project:</strong> ${{s.project}}</div>` : '';
  document.getElementById('detail').classList.add('open');
  document.getElementById('overlay').classList.add('open');
}}

function closeDetail() {{
  document.getElementById('detail').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}}
</script>
</body>
</html>
"""

components.html(html, height=420, scrolling=False)

# ── Tips ──────────────────────────────────────────────────────────────────────
with st.expander("💡 Tips for your journey", expanded=False):
    for tip in rm["tips"]:
        st.info(tip)

# ── Weekly Checklist ──────────────────────────────────────────────────────────
render_checklist()

# Completion
if pct == 100:
    st.balloons()
    st.success(f"🎉 Roadmap Complete! You've mastered all skills for **{role}**. Time to apply!")

# Achievements
st.markdown("---")

badge_cards = ""
for icon, title, desc, unlocked in [
    ("👣", "First Step",   "Any progress",        pct >= 1),
    ("🔥", "On Fire",      "Week 1 done",          done_weeks >= 1),
    ("⚡", "Quarter Way",  "25% complete",         pct >= 25),
    ("🌟", "Halfway",      "50% complete",         pct >= 50),
    ("📅", "Consistent",   "4+ weeks done",        done_weeks >= 4),
    ("💪", "Dedicated",    "10+ weeks done",       done_weeks >= 10),
    ("🚀", "Almost There", "75% complete",         pct >= 75),
    ("🧠", "Skill Master", f"100% for {role}",     pct == 100),
]:
    badge_cards += (
        f'<div class="ba-card {"ba-on" if unlocked else "ba-off"}">' 
        f'<div class="ba-icon">{icon}</div>'
        f'<div class="ba-title">{title}</div>'
        f'<div class="ba-desc">{desc}</div>'
        f'<div class="ba-status">{"✓ Unlocked" if unlocked else "🔒"}</div>'
        f'</div>'
    )

components.html(f"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',system-ui,sans-serif;}}
body{{background:#fff;color:#333;padding:1rem 0.5rem 2rem;}}
h2{{font-size:1.1rem;font-weight:800;color:#000;margin-bottom:1rem;display:flex;align-items:center;gap:0.5rem;}}
h2 span{{font-size:1.3rem;}}
.ba-grid{{display:flex;flex-wrap:wrap;gap:0.7rem;}}
.ba-card{{
    width:120px;border-radius:16px;padding:1rem 0.6rem;
    display:flex;flex-direction:column;align-items:center;gap:0.3rem;
    transition:transform 0.25s;cursor:default;
    background:#fff;border:1.5px solid #ccccff;box-shadow:0 4px 18px rgba(0,0,0,0.1);
}}
.ba-card:hover{{transform:translateY(-4px);}}
.ba-on{{
    background:#fff;border:1.5px solid #ccccff;box-shadow:0 4px 18px rgba(0,0,0,0.1);
}}
.ba-off{{
    background:#f8f8f8;border:1.5px solid #e0e0e0;opacity:0.6;filter:none;
}}
.ba-icon{{font-size:2rem;}}
.ba-title{{font-size:0.75rem;font-weight:800;text-align:center;color:#000;}}
.ba-on .ba-title{{color:#0000cc;}}
.ba-desc{{font-size:0.63rem;color:#555;text-align:center;line-height:1.4;}}
.ba-status{{font-size:0.63rem;font-weight:700;margin-top:0.2rem;color:#000;}}
.ba-on .ba-status{{color:#34d399;}}
.ba-on .ba-status{{color:#006600;}}
</style>
</head><body>
<h2><span>🏆</span> Achievements</h2>
<div class="ba-grid">{badge_cards}</div>
</body></html>
""", height=220, scrolling=False)

# ── Actions ───────────────────────────────────────────────────────────────────
st.markdown("")
a1, a2 = st.columns(2)
with a1:
    if st.button("🔄 Regenerate Roadmap", use_container_width=True):
        del st.session_state["roadmap_result"]
        st.session_state.checked_weeks = set()
        from utils.auth import update_user
        update_user(st.session_state.email, {"roadmap_result": None, "checked_weeks": []})
        st.rerun()
with a2:
    if st.button("🗑️ Reset Progress", use_container_width=True):
        st.session_state.checked_weeks = set()
        from utils.auth import update_user
        update_user(st.session_state.email, {"checked_weeks": []})
        st.rerun()
