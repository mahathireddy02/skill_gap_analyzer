import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.resume_builder import build_resume_pdf, validate_resume_data
from components.navbar import show_navbar

st.set_page_config(page_title="Resume Builder", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
require_login()

db_user = get_user(st.session_state.email)
theme = db_user.get("theme", "dark")

bg_color = "#ffffff" if theme == "light" else "#0a0e17"
text_color = "#000000" if theme == "light" else "#ffffff"
border_color = "#e5e7eb" if theme == "light" else "rgba(255,255,255,0.1)"
secondary_text = "#4b5563" if theme == "light" else "rgba(255,255,255,0.5)"

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body,.stApp{margin:0!important;padding:0!important;background:""" + bg_color + """!important;color:""" + text_color + """!important;}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div > div {
    background-color: """ + bg_color + """!important;
    color: """ + text_color + """!important;
    border: 1px solid """ + border_color + """!important;
}
.block-container{padding:1.5rem 2.5rem 2rem!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;border:none!important;}
div[data-testid="stButton"] button[kind="secondary"]{
    background-color: """ + bg_color + """!important;
    color: """ + text_color + """!important;
    border: 1px solid """ + border_color + """!important;
}
h1, h2, h3, h4, p, label, .stMarkdown {color: """ + text_color + """!important;}
small, .stCaptionContainer p {color: """ + secondary_text + """!important;}
hr {border-color: """ + border_color + """!important;}
div[data-testid="stAlert"] {
    background-color: """ + bg_color + """!important;
    border: 1px solid """ + border_color + """!important;
}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

st.markdown("## 📝 Resume Builder")
st.caption("Pick a template, fill in your details, and download a professional PDF resume.")
st.markdown("")

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_template" not in st.session_state:
    st.session_state.selected_template = None
if "template_chosen" not in st.session_state:
    st.session_state.template_chosen = False
if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

# ── Template metadata for preview cards ──────────────────────────────────────
TEMPLATE_META = {
    "Classic": {
        "icon": "📄", "accent": "#000000", "header_bg": "#ffffff",
        "header_text": "#000000", "sec_color": "#000000", "hr": "#000000",
        "desc": "Black & white, centered name. Traditional and ATS-safe.",
        "tags": ["Traditional", "ATS-Safe", "B&W"],
    },
    "Modern": {
        "icon": "✨", "accent": "#4f46e5", "header_bg": "#4f46e5",
        "header_text": "#ffffff", "sec_color": "#4f46e5", "hr": "#4f46e5",
        "desc": "Indigo header band, colored section titles. Clean and professional.",
        "tags": ["Popular", "Colorful", "Tech"],
    },
    "Minimal": {
        "icon": "🎯", "accent": "#059669", "header_bg": "#ffffff",
        "header_text": "#111827", "sec_color": "#059669", "hr": "#059669",
        "desc": "Green accents, lots of whitespace. Simple and elegant.",
        "tags": ["Clean", "Minimal", "Green"],
    },
    "Creative": {
        "icon": "🎨", "accent": "#7c3aed", "header_bg": "#7c3aed",
        "header_text": "#ffffff", "sec_color": "#7c3aed", "hr": "#7c3aed",
        "desc": "Purple header, bold section labels. Stands out from the crowd.",
        "tags": ["Bold", "Creative", "Purple"],
    },
}

# ── Template preview cards ────────────────────────────────────────────────────
st.markdown("### 🎨 Choose a Template")
st.caption("Each card shows a live preview of the template style. Click **Select** to choose one.")
st.markdown("")

def _preview_classic(border, shadow):
    return f"""
<div style="border:{border};border-radius:14px;overflow:hidden;box-shadow:{shadow};margin-bottom:6px;background:#fff;height:100%;display:flex;flex-direction:column;">
  <div style="background:#fff;padding:10px 12px 6px;flex:1;overflow:hidden;">
    <div style="border-top:2.5px solid #000;padding-top:5px;">
      <div style="font-size:0.9rem;font-weight:900;color:#000;text-align:center;font-family:Georgia,serif;">John Smith</div>
      <div style="font-size:0.55rem;color:#555;text-align:center;margin-top:2px;font-family:Georgia,serif;">john@email.com &nbsp;·&nbsp; +91 9876543210 &nbsp;·&nbsp; Mumbai</div>
    </div>
    <div style="border-top:2.5px solid #000;border-bottom:0.5px solid #000;margin:5px 0 3px;"></div>
  </div>
  <div style="background:#fff;padding:0 12px 8px;">
    <div style="border-top:0.5px solid #000;text-align:center;padding:2px 0 1px;">
      <span style="font-size:0.58rem;font-weight:900;color:#000;font-family:Georgia,serif;letter-spacing:0.08em;">WORK EXPERIENCE</span>
    </div>
    <div style="border-top:1.5px solid #000;margin-bottom:4px;"></div>
    <div style="display:flex;justify-content:space-between;">
      <span style="font-size:0.6rem;font-weight:700;color:#000;font-family:Georgia,serif;">Software Engineer</span>
      <span style="font-size:0.52rem;color:#666;font-style:italic;font-family:Georgia,serif;">2022–Present</span>
    </div>
    <div style="font-size:0.55rem;color:#444;font-style:italic;font-family:Georgia,serif;margin-bottom:2px;">Google</div>
    <div style="font-size:0.52rem;color:#222;font-family:Georgia,serif;">• Built scalable REST APIs</div>
    <div style="font-size:0.52rem;color:#222;font-family:Georgia,serif;">• Reduced latency by 30%</div>
    <div style="border-top:0.5px solid #000;text-align:center;padding:2px 0 1px;margin-top:5px;">
      <span style="font-size:0.58rem;font-weight:900;color:#000;font-family:Georgia,serif;letter-spacing:0.08em;">SKILLS</span>
    </div>
    <div style="border-top:1.5px solid #000;margin-bottom:3px;"></div>
    <div style="font-size:0.52rem;color:#222;font-family:Georgia,serif;"><b>Languages:</b> Python, Java, SQL</div>
    <div style="font-size:0.52rem;color:#222;font-family:Georgia,serif;"><b>Tools:</b> Docker, Git, AWS</div>
  </div>
  <div style="background:#f5f5f5;padding:5px 12px;display:flex;justify-content:space-between;align-items:center;margin-top:auto;">
    <div style="color:#000;font-size:0.62rem;font-weight:800;">
      Traditional | ATS-Safe | B&W
    </div>
    <div style="font-size:0.65rem;font-weight:800;color:#000;">📄 Classic</div>
  </div>
</div>"""

def _preview_modern(border, shadow):
    return f"""
<div style="border:{border};border-radius:14px;overflow:hidden;box-shadow:{shadow};margin-bottom:6px;height:100%;display:flex;flex-direction:column;">
  <div style="background:#1e1b4b;padding:9px 12px;">
    <div style="font-size:0.88rem;font-weight:800;color:#fff;">John Smith</div>
    <div style="font-size:0.58rem;color:#818cf8;margin-top:1px;">Results-driven Software Engineer</div>
  </div>
  <div style="display:flex;">
    <div style="background:#312e81;padding:7px 8px;width:38%;flex-shrink:0;">
      <div style="border-top:0.5px solid #4338ca;margin-bottom:3px;"></div>
      <div style="font-size:0.55rem;font-weight:700;color:#818cf8;letter-spacing:0.06em;margin-bottom:2px;">CONTACT</div>
      <div style="font-size:0.5rem;font-weight:700;color:#fff;">Email</div>
      <div style="font-size:0.5rem;color:#c7d2fe;margin-bottom:2px;">john@email.com</div>
      <div style="font-size:0.5rem;font-weight:700;color:#fff;">Phone</div>
      <div style="font-size:0.5rem;color:#c7d2fe;margin-bottom:3px;">+91 9876543210</div>
      <div style="border-top:0.5px solid #4338ca;margin-bottom:3px;"></div>
      <div style="font-size:0.55rem;font-weight:700;color:#818cf8;letter-spacing:0.06em;margin-bottom:2px;">SKILLS</div>
      <div style="font-size:0.5rem;font-weight:700;color:#fff;">Languages</div>
      <div style="font-size:0.5rem;color:#c7d2fe;margin-bottom:2px;">Python, Java, SQL</div>
      <div style="font-size:0.5rem;font-weight:700;color:#fff;">Tools</div>
      <div style="font-size:0.5rem;color:#c7d2fe;">Docker, Git, AWS</div>
    </div>
    <div style="background:#f8f9ff;padding:7px 9px;flex:1;">
      <div style="font-size:0.58rem;font-weight:800;color:#4f46e5;letter-spacing:0.06em;">EXPERIENCE</div>
      <div style="border-bottom:1.5px solid #4f46e5;margin-bottom:3px;"></div>
      <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.58rem;font-weight:700;color:#1f2937;">Software Engineer</span>
        <span style="font-size:0.5rem;color:#6b7280;font-style:italic;">2022–Now</span>
      </div>
      <div style="font-size:0.52rem;color:#4f46e5;margin-bottom:2px;">Google</div>
      <div style="font-size:0.5rem;color:#374151;">• Built scalable REST APIs</div>
      <div style="font-size:0.5rem;color:#374151;">• Reduced latency by 30%</div>
    </div>
  </div>
  <div style="background:#f0f0ff;padding:5px 12px;display:flex;justify-content:space-between;align-items:center;margin-top:auto;">
    <div style="color:#000;font-size:0.62rem;font-weight:800;">
      Popular | Tech | Clean
    </div>
    <div style="font-size:0.65rem;font-weight:800;color:#4f46e5;">✨ Modern</div>
  </div>
</div>"""

def _preview_minimal(border, shadow):
    return f"""
<div style="border:{border};border-radius:14px;overflow:hidden;box-shadow:{shadow};margin-bottom:6px;background:#fff;height:100%;display:flex;flex-direction:column;">
  <div style="background:#fff;padding:10px 12px 5px;">
    <div style="font-size:1rem;font-weight:900;color:#111827;">John Smith</div>
    <div style="border-top:1.5px solid #059669;margin:4px 0 3px;"></div>
    <div style="font-size:0.52rem;color:#6b7280;">john@email.com &nbsp;·&nbsp; +91 9876543210 &nbsp;·&nbsp; Mumbai</div>
  </div>
  <div style="background:#fff;padding:4px 12px 8px;">
    <div style="font-size:0.6rem;font-weight:800;color:#059669;margin-top:5px;">Experience</div>
    <div style="border-top:0.6px solid #059669;margin-bottom:4px;"></div>
    <div style="border-left:3px solid #059669;padding-left:7px;margin-bottom:4px;">
      <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.58rem;font-weight:700;color:#111827;">Software Engineer</span>
        <span style="font-size:0.5rem;color:#9ca3af;font-style:italic;">2022–Present</span>
      </div>
      <div style="font-size:0.52rem;color:#059669;margin-bottom:2px;">Google</div>
      <div style="font-size:0.5rem;color:#374151;">• Built scalable REST APIs</div>
    </div>
    <div style="font-size:0.6rem;font-weight:800;color:#059669;margin-top:4px;">Skills</div>
    <div style="border-top:0.6px solid #059669;margin-bottom:4px;"></div>
    <div style="display:flex;">
      <span style="font-size:0.52rem;font-weight:700;color:#111827;width:38%;">Languages</span>
      <span style="font-size:0.52rem;color:#374151;">Python, Java, SQL</span>
    </div>
    <div style="display:flex;">
      <span style="font-size:0.52rem;font-weight:700;color:#111827;width:38%;">Tools</span>
      <span style="font-size:0.52rem;color:#374151;">Docker, Git, AWS</span>
    </div>
  </div>
  <div style="background:#f9fafb;padding:5px 12px;display:flex;justify-content:space-between;align-items:center;margin-top:auto;">
    <div style="color:#000;font-size:0.62rem;font-weight:800;">
      Clean | Simple | Green
    </div>
    <div style="font-size:0.65rem;font-weight:800;color:#059669;">🎯 Minimal</div>
  </div>
</div>"""

def _preview_creative(border, shadow):
    return f"""
<div style="border:{border};border-radius:14px;overflow:hidden;box-shadow:{shadow};margin-bottom:6px;height:100%;display:flex;flex-direction:column;">
  <div style="background:#7c3aed;padding:10px 12px;">
    <div style="font-size:0.9rem;font-weight:900;color:#fff;">John Smith</div>
    <div style="font-size:0.58rem;color:#ddd6fe;margin-top:1px;">Results-driven Software Engineer</div>
    <div style="font-size:0.5rem;color:#c4b5fd;margin-top:3px;">john@email.com &nbsp;|&nbsp; +91 9876543210 &nbsp;|&nbsp; Mumbai</div>
  </div>
  <div style="background:#fff;padding:6px 12px 8px;">
    <div style="background:#7c3aed;border-left:4px solid #6d28d9;padding:3px 8px;margin-bottom:5px;">
      <span style="font-size:0.58rem;font-weight:800;color:#fff;letter-spacing:0.07em;">SKILLS</span>
    </div>
    <div style="margin-bottom:4px;">
      <span style="font-size:0.5rem;font-weight:700;color:#7c3aed;">Languages &nbsp;</span>
      <span style="background:#ede9fe;color:#5b21b6;font-size:0.5rem;font-weight:700;padding:1px 6px;border-radius:999px;margin:1px;display:inline-block;">Python</span>
      <span style="background:#ede9fe;color:#5b21b6;font-size:0.5rem;font-weight:700;padding:1px 6px;border-radius:999px;margin:1px;display:inline-block;">Java</span>
      <span style="background:#ede9fe;color:#5b21b6;font-size:0.5rem;font-weight:700;padding:1px 6px;border-radius:999px;margin:1px;display:inline-block;">SQL</span>
    </div>
    <div style="background:#7c3aed;border-left:4px solid #6d28d9;padding:3px 8px;margin-bottom:5px;">
      <span style="font-size:0.58rem;font-weight:800;color:#fff;letter-spacing:0.07em;">EXPERIENCE</span>
    </div>
    <div style="background:#f5f3ff;border-left:4px solid #7c3aed;padding:4px 7px;">
      <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.58rem;font-weight:700;color:#1e1b4b;">Software Engineer</span>
        <span style="font-size:0.5rem;color:#6b7280;font-style:italic;">2022–Now</span>
      </div>
      <div style="font-size:0.52rem;color:#7c3aed;margin-bottom:2px;">Google</div>
      <div style="font-size:0.5rem;color:#374151;">• Built scalable REST APIs</div>
    </div>
  </div>
  <div style="background:#f5f3ff;padding:5px 12px;display:flex;justify-content:space-between;align-items:center;margin-top:auto;">
    <div style="color:#000;font-size:0.62rem;font-weight:800;">
      Bold | Creative | Purple
    </div>
    <div style="font-size:0.65rem;font-weight:800;color:#7c3aed;">🎨 Creative</div>
  </div>
</div>"""

_PREVIEW_FN = {
    "Classic":  _preview_classic,
    "Modern":   _preview_modern,
    "Minimal":  _preview_minimal,
    "Creative": _preview_creative,
}

cols = st.columns(4, gap="small")
for col, (tmpl, meta) in zip(cols, TEMPLATE_META.items()):
    with col:
        is_sel = st.session_state.selected_template == tmpl
        border = f"3px solid {meta['accent']}" if is_sel else "2px solid #e5e7eb"
        shadow = f"0 6px 24px {meta['accent']}44" if is_sel else "0 2px 8px rgba(0,0,0,0.06)"
        st.markdown(
            f'<div style="height:340px;display:flex;flex-direction:column;">'
            + _PREVIEW_FN[tmpl](border, shadow)
            + '</div>',
            unsafe_allow_html=True
        )
        btn_label = "✅ Selected" if is_sel else f"Select {tmpl}"
        btn_type  = "primary" if is_sel else "secondary"
        if st.button(btn_label, key=f"tmpl_{tmpl}", use_container_width=True, type=btn_type):
            st.session_state.selected_template = tmpl
            st.session_state.template_chosen   = True
            st.switch_page("pages/11_Resume_Details.py")

st.markdown("")
if not st.session_state.template_chosen:
    st.info("👆 Select a template above to continue filling in your resume details.")
else:
    st.success(f"✅ {st.session_state.selected_template} template selected.")
    if st.button("Continue to Resume Details", type="primary", use_container_width=True):
        st.switch_page("pages/11_Resume_Details.py")
