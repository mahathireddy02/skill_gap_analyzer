# ── Set your credentials here once ──────────────────────
$env:SMTP_EMAIL    = "your_gmail@gmail.com"
$env:SMTP_PASSWORD = "your_app_password_here"
$env:APP_URL       = "http://10.74.88.186:8501"
# ─────────────────────────────────────────────────────────

py -3.12 -m streamlit run app.py
