import streamlit as st
import streamlit.components.v1 as components
import json

def role_autocomplete(roles: list[str], default: str = "", key: str = "role_ac",
                      dark: bool = True) -> str:
    """
    Proper autocomplete text input with a styled dropdown.
    Filters roles as the user types. Clicking a suggestion fills the input.
    Returns the current selected/typed value.
    """
    val_key = f"{key}_value"
    if val_key not in st.session_state:
        st.session_state[val_key] = default

    # Check if a suggestion was clicked (passed via query param)
    qp_key = f"{key}_pick"
    picked = st.query_params.get(qp_key, "")
    if picked:
        st.session_state[val_key] = picked
        del st.query_params[qp_key]
        st.rerun()

    roles_json = json.dumps(roles)
    current    = st.session_state[val_key]

    bg_input  = "rgba(255,255,255,0.07)" if dark else "#fff"
    border    = "rgba(255,255,255,0.12)" if dark else "#d1d5db"
    text_col  = "#fff"                   if dark else "#1a1a2e"
    dd_bg     = "#1a1a2e"                if dark else "#fff"
    dd_border = "rgba(255,255,255,0.12)" if dark else "#e5e7eb"
    dd_hover  = "rgba(124,58,237,0.2)"   if dark else "#f3f0ff"
    dd_text   = "rgba(255,255,255,0.9)"  if dark else "#1a1a2e"

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0;
       font-family: 'Inter', sans-serif; }}
  body {{ background: transparent; overflow: visible; }}

  .ac-wrap {{
    position: relative;
    width: 100%;
  }}

  #ac-input {{
    width: 100%;
    padding: 0.55rem 0.85rem;
    background: {bg_input};
    border: 1px solid {border};
    border-radius: 10px;
    color: {text_col};
    font-size: 0.92rem;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }}
  #ac-input:focus {{
    border-color: rgba(167,139,250,0.6);
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15);
  }}
  #ac-input::placeholder {{ color: rgba(255,255,255,0.3); }}

  #ac-dropdown {{
    display: none;
    position: absolute;
    top: calc(100% + 4px);
    left: 0; right: 0;
    background: {dd_bg};
    border: 1px solid {dd_border};
    border-radius: 10px;
    max-height: 220px;
    overflow-y: auto;
    z-index: 9999;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  }}
  #ac-dropdown.open {{ display: block; }}

  .ac-item {{
    padding: 0.55rem 0.9rem;
    font-size: 0.88rem;
    color: {dd_text};
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    transition: background 0.12s;
  }}
  .ac-item:last-child {{ border-bottom: none; }}
  .ac-item:hover, .ac-item.active {{ background: {dd_hover}; color: #a78bfa; }}

  .ac-empty {{
    padding: 0.6rem 0.9rem;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.3);
    font-style: italic;
  }}
</style>
</head>
<body>
<div class="ac-wrap">
  <input id="ac-input" type="text"
         placeholder="Type to search roles…"
         value="{current}"
         autocomplete="off" />
  <div id="ac-dropdown"></div>
</div>

<script>
  const roles     = {roles_json};
  const input     = document.getElementById('ac-input');
  const dropdown  = document.getElementById('ac-dropdown');
  const QP_KEY    = '{qp_key}';
  let activeIdx   = -1;

  function filter(q) {{
    if (!q) return roles.slice(0, 8);
    const lq = q.toLowerCase();
    return roles.filter(r => r.toLowerCase().includes(lq)).slice(0, 8);
  }}

  function render(items) {{
    dropdown.innerHTML = '';
    activeIdx = -1;
    if (!items.length) {{
      dropdown.innerHTML = '<div class="ac-empty">No matching roles — your custom role will be used</div>';
      dropdown.classList.add('open');
      return;
    }}
    items.forEach((r, i) => {{
      const div = document.createElement('div');
      div.className = 'ac-item';
      div.textContent = r;
      div.addEventListener('mousedown', (e) => {{
        e.preventDefault();
        selectRole(r);
      }});
      dropdown.appendChild(div);
    }});
    dropdown.classList.add('open');
  }}

  function selectRole(r) {{
    input.value = r;
    dropdown.classList.remove('open');
    // Send to Streamlit via query param + form submit trick
    const url = new URL(window.parent.location.href);
    url.searchParams.set(QP_KEY, r);
    window.parent.history.replaceState(null, '', url.toString());
    // Trigger Streamlit rerun by dispatching a custom event
    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: r}}, '*');
    // Fallback: navigate to trigger rerun
    setTimeout(() => {{ window.parent.location.href = url.toString(); }}, 80);
  }}

  input.addEventListener('input', () => {{
    const q = input.value.trim();
    render(filter(q));
  }});

  input.addEventListener('focus', () => {{
    render(filter(input.value.trim()));
  }});

  input.addEventListener('blur', () => {{
    setTimeout(() => dropdown.classList.remove('open'), 150);
    // Save typed value even if not from list
    const val = input.value.trim();
    if (val) {{
      const url = new URL(window.parent.location.href);
      url.searchParams.set(QP_KEY, val);
      window.parent.history.replaceState(null, '', url.toString());
      setTimeout(() => {{ window.parent.location.href = url.toString(); }}, 80);
    }}
  }});

  input.addEventListener('keydown', (e) => {{
    const items = dropdown.querySelectorAll('.ac-item');
    if (e.key === 'ArrowDown') {{
      e.preventDefault();
      activeIdx = Math.min(activeIdx + 1, items.length - 1);
      items.forEach((el, i) => el.classList.toggle('active', i === activeIdx));
    }} else if (e.key === 'ArrowUp') {{
      e.preventDefault();
      activeIdx = Math.max(activeIdx - 1, 0);
      items.forEach((el, i) => el.classList.toggle('active', i === activeIdx));
    }} else if (e.key === 'Enter' && activeIdx >= 0) {{
      e.preventDefault();
      selectRole(items[activeIdx].textContent);
    }} else if (e.key === 'Escape') {{
      dropdown.classList.remove('open');
    }}
  }});
</script>
</body>
</html>
"""

    components.html(html, height=58, scrolling=False)

    # Also show a plain hidden text_input so Streamlit can read the value
    # The value is synced via query param → session state above
    return st.session_state[val_key]
