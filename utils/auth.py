import json, hashlib, os, streamlit as st

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def _load():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def signup(name, email, password, security_q=None, security_a=None,
           target_role="", skill_level="Beginner", skills=None,
           time_availability="5–10 hrs", experience_type="Student"):
    users = _load()
    if email in users:
        return False, "Email already registered."
    users[email] = {
        "name":              name,
        "password":          _hash(password),
        "skills":            skills or [],
        "missing_skills":    [],
        "resume_score":      0,
        "target_role":       target_role,
        "skill_level":       skill_level,
        "time_availability": time_availability,
        "experience_type":   experience_type,
        "security_q":        security_q or "",
        "security_a":        _hash(security_a.lower().strip()) if security_a else "",
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

def verify_security_answer(email, security_answer):
    users = _load()
    if email not in users:
        return False, "Email not found."
    stored = users[email].get("security_a", "")
    if not stored:
        return False, "No security question set for this account."
    if _hash(security_answer.lower().strip()) != stored:
        return False, "Incorrect answer."
    return True, "Answer verified."

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
