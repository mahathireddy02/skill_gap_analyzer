import json, hashlib, os, secrets, time, smtplib, streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

# ── Configure these with your Gmail credentials ───────────────────────────────
SMTP_EMAIL    = os.environ.get("SMTP_EMAIL", "")       # your Gmail address
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")    # Gmail App Password
APP_URL       = os.environ.get("APP_URL", "http://localhost:8501")

def _load():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def signup(name, email, password, security_q=None, security_a=None):
    users = _load()
    if email in users:
        return False, "Email already registered."
    users[email] = {
        "name": name,
        "password": _hash(password),
        "skills": [],
        "resume_score": 0,
        "security_q": security_q or "",
        "security_a": _hash(security_a.lower().strip()) if security_a else "",
    }
    _save(users)
    return True, "Account created!"

def login(email, password):
    users = _load()
    if email not in users:
        return False, "Email not found."
    if users[email]["password"] != _hash(password):
        return False, "Incorrect password."
    return True, users[email]

def get_security_question(email):
    users = _load()
    if email not in users:
        return None
    return users[email].get("security_q", "")

def reset_password(email, security_answer, new_password):
    users = _load()
    if email not in users:
        return False, "Email not found."
    stored = users[email].get("security_a", "")
    if not stored:
        return False, "No security question set for this account."
    if _hash(security_answer.lower().strip()) != stored:
        return False, "Incorrect answer."
    users[email]["password"] = _hash(new_password)
    _save(users)
    return True, "Password reset successfully!"

def generate_reset_token(email):
    """Generate a 1-hour reset token, store it, and return the reset URL."""
    users = _load()
    if email not in users:
        return False, "No account found with that email."
    token = secrets.token_urlsafe(32)
    users[email]["reset_token"]  = token
    users[email]["reset_expiry"] = time.time() + 3600  # 1 hour
    _save(users)
    reset_url = f"{APP_URL}/1_Login?token={token}&email={email}"
    return True, reset_url

def send_reset_email(email):
    """Send password reset email. Returns (ok, message)."""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        # Dev fallback: return the link directly
        ok, reset_url = generate_reset_token(email)
        if not ok:
            return False, reset_url
        return True, f"DEV_LINK:{reset_url}"

    ok, reset_url = generate_reset_token(email)
    if not ok:
        return False, reset_url

    users = _load()
    name  = users[email].get("name", "Student")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset your SkillGap password"
    msg["From"]    = SMTP_EMAIL
    msg["To"]      = email

    html = f"""
    <div style="font-family:Inter,sans-serif;max-width:480px;margin:0 auto;">
      <h2 style="color:#7c3aed;">🎓 SkillGap — Password Reset</h2>
      <p>Hi <strong>{name}</strong>,</p>
      <p>Click the button below to reset your password. This link expires in <strong>1 hour</strong>.</p>
      <a href="{reset_url}" style="display:inline-block;background:linear-gradient(135deg,#7c3aed,#4f46e5);
         color:#fff;padding:12px 28px;border-radius:10px;text-decoration:none;font-weight:700;margin:16px 0;">
        🔑 Reset My Password
      </a>
      <p style="color:#999;font-size:0.85rem;">If you didn't request this, ignore this email.</p>
    </div>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, email, msg.as_string())
        return True, "Email sent!"
    except Exception as e:
        return False, f"Failed to send email: {e}"

def verify_reset_token(email, token):
    """Check token validity. Returns (ok, message)."""
    users = _load()
    if email not in users:
        return False, "Invalid link."
    stored_token  = users[email].get("reset_token", "")
    stored_expiry = users[email].get("reset_expiry", 0)
    if not stored_token or stored_token != token:
        return False, "Invalid or already used reset link."
    if time.time() > stored_expiry:
        return False, "Reset link has expired. Please request a new one."
    return True, "Valid"

def reset_password_with_token(email, token, new_password):
    """Reset password after token verification."""
    ok, msg = verify_reset_token(email, token)
    if not ok:
        return False, msg
    users = _load()
    users[email]["password"]     = _hash(new_password)
    users[email]["reset_token"]  = ""
    users[email]["reset_expiry"] = 0
    _save(users)
    return True, "Password reset successfully!"


def delete_account(email):
    users = _load()
    if email not in users:
        return False, "Account not found."
    del users[email]
    _save(users)
    return True, "Account deleted."

def get_user(email):
    return _load().get(email)

def update_user(email, data):
    users = _load()
    users[email].update(data)
    _save(users)

def require_login():
    import streamlit as st
    # Restore session from query param on refresh
    if not st.session_state.get("user"):
        email = st.query_params.get("session", "")
        if email:
            users = _load()
            if email in users:
                st.session_state.user  = users[email]
                st.session_state.email = email
    if not st.session_state.get("user") or not st.session_state.get("email"):
        st.switch_page("pages/1_Login.py")
        st.stop()
    # Keep session param in URL so refresh works
    st.query_params["session"] = st.session_state.email
