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
html,body,.stApp{margin:0!important;padding:0!important;background:#0f0c29!important;}
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
missing = db_user.get("missing_skills", [])
role    = db_user.get("target_role", "")

if not missing or not role:
    st.info("No skill gap data found. Run the Skill Gap Analyzer first.")
    if st.button("Go to Skill Gap Analyzer", type="primary"):
        st.switch_page("pages/5_Skill_Gap.py")
    st.stop()

if "checked_weeks" not in st.session_state:
    st.session_state.checked_weeks = set()

st.markdown("## 🛤️ Learning Roadmap")
st.caption(f"Target Role: **{role}** · {len(missing)} skills to learn")

# ── Settings Form ─────────────────────────────────────────────────────────────
with st.expander("⚙️ Customize Roadmap", expanded="roadmap_result" not in st.session_state):
    c1, c2, c3 = st.columns(3)
    with c1:
        skill_level   = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"])
        hours_per_day = st.slider("Hours/day", 0.5, 8.0, 1.5, 0.5)
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
        with st.spinner("Building your roadmap..."):
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
        st.rerun()

if "roadmap_result" not in st.session_state:
    st.stop()

rm          = st.session_state["roadmap_result"]
tl          = rm["timeline"]
phases      = rm["phase_plan"]
weekly      = rm["weekly_plan"]
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
  body{{background:#0f0c29;font-family:'Inter',system-ui,sans-serif;color:#fff;overflow-x:hidden;}}

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
  .station-active .s-icon{{fill:#fff;font-size:14px;}}
  .station-upcoming .s-icon{{fill:#6366f1;font-size:14px;}}

  .s-label{{font-size:12px;font-weight:700;fill:#e2e8f0;text-anchor:middle;}}
  .s-weeks{{font-size:10px;fill:#94a3b8;text-anchor:middle;}}

  .station-group{{cursor:pointer;transition:transform .2s;}}
  .station-group:hover .s-circle{{stroke-width:3;}}

  /* Track */
  .track-bg{{stroke:#1e1b4b;stroke-width:8;fill:none;stroke-linecap:round;}}
  .track-done{{stroke:url(#trackGrad);stroke-width:8;fill:none;stroke-linecap:round;stroke-dasharray:var(--dash);stroke-dashoffset:0;transition:stroke-dasharray 1s ease;}}
  .track-rail{{stroke:rgba(255,255,255,0.06);stroke-width:2;fill:none;stroke-dasharray:12 18;}}

  /* Train */
  #train{{transition:all 1.2s cubic-bezier(.4,0,.2,1);}}
  #train-glow{{filter:drop-shadow(0 0 12px #a78bfa);}}

  /* Detail panel */
  #detail{{
    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.92);
    background:linear-gradient(135deg,#1e1b4b,#0f0c29);
    border:1px solid rgba(167,139,250,0.3);
    border-radius:20px;padding:28px 32px;width:min(520px,90vw);
    box-shadow:0 24px 80px rgba(0,0,0,0.7);
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
  .d-close{{background:rgba(255,255,255,0.08);border:none;color:#fff;width:32px;height:32px;
    border-radius:50%;cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;}}
  .d-close:hover{{background:rgba(255,255,255,0.15);}}
  .d-badge{{display:inline-block;padding:3px 12px;border-radius:999px;font-size:0.75rem;font-weight:700;margin-bottom:14px;}}
  .badge-done{{background:#10b98122;color:#34d399;border:1px solid #10b98144;}}
  .badge-active{{background:#7c3aed22;color:#a78bfa;border:1px solid #7c3aed44;}}
  .badge-upcoming{{background:#1e1b4b;color:#6366f1;border:1px solid #4338ca44;}}
  .d-meta{{color:#94a3b8;font-size:0.85rem;margin-bottom:16px;}}
  .ph-row{{display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;font-size:0.83rem;line-height:1.5;color:#cbd5e1;}}
  .ph-badge{{flex-shrink:0;padding:2px 8px;border-radius:6px;font-size:0.72rem;font-weight:700;margin-top:1px;}}
  .ph-beginner{{background:#10b98122;color:#34d399;}}
  .ph-intermediate{{background:#f59e0b22;color:#fbbf24;}}
  .ph-advanced{{background:#ef444422;color:#f87171;}}
  .d-section{{font-size:0.78rem;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.08em;margin:14px 0 8px;}}
  .d-resources ul{{padding-left:16px;}}
  .d-resources li{{font-size:0.83rem;color:#94a3b8;margin-bottom:4px;}}
  .d-project{{background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);
    border-radius:10px;padding:10px 14px;font-size:0.83rem;color:#c4b5fd;margin-top:12px;}}

  /* Progress bar */
  #prog-wrap{{padding:0 24px 16px;}}
  .prog-label{{display:flex;justify-content:space-between;font-size:0.8rem;color:#94a3b8;margin-bottom:6px;}}
  .prog-bar{{height:6px;background:rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;}}
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

components.html(html, height=340, scrolling=False)

# ── Tips ──────────────────────────────────────────────────────────────────────
with st.expander("💡 Tips for your journey", expanded=False):
    for tip in rm["tips"]:
        st.info(tip)

# ── Weekly Checklist ──────────────────────────────────────────────────────────
render_checklist()

# ── Completion ────────────────────────────────────────────────────────────────
if pct == 100:
    st.balloons()
    st.success(f"🎉 Roadmap Complete! You've mastered all skills for **{role}**. Time to apply!")

# ── Actions ───────────────────────────────────────────────────────────────────
st.markdown("")
a1, a2 = st.columns(2)
with a1:
    if st.button("🔄 Regenerate Roadmap", use_container_width=True):
        del st.session_state["roadmap_result"]
        st.session_state.checked_weeks = set()
        st.rerun()
with a2:
    if st.button("🗑️ Reset Progress", use_container_width=True):
        st.session_state.checked_weeks = set()
        st.rerun()
