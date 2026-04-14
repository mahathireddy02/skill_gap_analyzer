# 🎓 Student Skill Gap Analyzer

A complete Streamlit web app that helps students upload resumes, analyze skill gaps, get personalized roadmaps, and track progress.

---

## 📁 Project Structure

```
skill_gap_analyzer/
├── app.py                  # Landing page
├── pages/
│   ├── 1_Login.py
│   ├── 2_Signup.py
│   ├── 3_Dashboard.py
│   ├── 4_Resume_Score.py
│   ├── 5_Skill_Gap.py
│   ├── 6_Roadmap.py
│   ├── 7_Analytics.py
│   └── 8_Profile.py
├── components/
│   └── navbar.py           # Reusable top navbar
├── utils/
│   ├── auth.py             # Signup / Login / Session
│   ├── scorer.py           # Resume ATS scoring
│   ├── analyzer.py         # Skill gap logic
│   └── roadmap.py          # Learning roadmap generator
├── data/
│   └── users.json          # User storage (auto-managed)
└── requirements.txt
```

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
```
http://localhost:8501
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Auth | Signup/Login with hashed passwords stored in JSON |
| 📄 Resume Score | Upload PDF or paste text → ATS-style score + suggestions |
| 🧠 Skill Gap | Select target role → see matched vs missing skills |
| 🛤️ Roadmap | Beginner → Intermediate → Advanced plan per missing skill |
| 📊 Analytics | Charts for skill match, resume score, weekly progress |
| 👤 Profile | View/edit profile, reset data |

---

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit (Python)
- **PDF Parsing**: pdfplumber
- **Storage**: JSON file (`data/users.json`)
- **Charts**: Streamlit native charts + pandas
