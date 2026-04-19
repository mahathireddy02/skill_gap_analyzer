import streamlit as st
import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from components.navbar import show_navbar

st.set_page_config(page_title="Chatbot · SkillGap", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
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
.user-msg{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;
    border-radius:16px 16px 4px 16px;padding:0.7rem 1rem;margin:0.5rem 0 0.5rem auto;
    max-width:70%;font-size:0.9rem;line-height:1.5;width:fit-content;}
.bot-msg{background:#f3f0ff;color:#1a1a2e;
    border-radius:16px 16px 16px 4px;padding:0.7rem 1rem;margin:0.5rem auto 0.5rem 0;
    max-width:75%;font-size:0.9rem;line-height:1.6;width:fit-content;}
</style>
""", unsafe_allow_html=True)

show_navbar("Chatbot")

# ── User profile ──────────────────────────────────────────────────────────────
db_user      = get_user(st.session_state.email)
user_skills  = db_user.get("skills", [])
missing      = db_user.get("missing_skills", [])
target_role  = db_user.get("target_role", "")
resume_score = db_user.get("resume_score", 0)
name         = st.session_state.user.get("name", "there").split()[0]

# ── Skill tips knowledge base ─────────────────────────────────────────────────
SKILL_TIPS = {
    "python":            "Start with python.org tutorial. Build small scripts, then move to Flask/FastAPI. Practice on HackerRank.",
    "javascript":        "Use javascript.info — best free resource. Build DOM projects, then learn ES6+, then React.",
    "typescript":        "Learn after JavaScript. Start with the official TypeScript Handbook at typescriptlang.org.",
    "java":              "Start with Java Brains on YouTube. Learn OOP, then Spring Boot for backend APIs.",
    "kotlin":            "Use official Kotlin docs + Philipp Lackner on YouTube for Android development.",
    "swift":             "Use Apple's official Swift tutorials at developer.apple.com. Build iOS apps with SwiftUI.",
    "dart":              "Start at dartpad.dev. Learn syntax, then move to Flutter.",
    "html":              "Use MDN Web Docs. Build 5 static pages. Focus on semantic HTML.",
    "css":               "Practice Flexbox Froggy and Grid Garden. Then build real layouts.",
    "react":             "Use react.dev (official docs). Build a todo app, then a weather app with API.",
    "vue":               "Use vuejs.org official guide. Build a simple CRUD app.",
    "angular":           "Use angular.io tour of heroes tutorial. Learn components, services, and routing.",
    "node":              "Use Traversy Media Node.js crash course. Build a REST API with Express.",
    "django":            "Use official Django tutorial (djangoproject.com). Build a blog app.",
    "flask":             "Use official Flask docs. Build a simple REST API.",
    "fastapi":           "Use fastapi.tiangolo.com docs. Build a CRUD API with Pydantic models.",
    "sql":               "Practice on SQLZoo and Mode Analytics. Focus on JOINs, GROUP BY, window functions.",
    "postgresql":        "Use official PostgreSQL tutorial. Learn indexing and EXPLAIN ANALYZE.",
    "mongodb":           "Use MongoDB University free courses. Learn aggregation pipeline.",
    "mysql":             "Use W3Schools SQL + practice on db-fiddle.com.",
    "redis":             "Use redis.io docs. Learn caching, pub/sub, and session storage patterns.",
    "docker":            "Use TechWorld with Nana on YouTube. Containerize a Python app first.",
    "kubernetes":        "Learn Docker first, then use kubernetes.io tutorials. Use Minikube locally.",
    "aws":               "Start with AWS Free Tier. Learn EC2, S3, Lambda. Use AWS Skill Builder.",
    "azure":             "Use Microsoft Learn (learn.microsoft.com). Start with AZ-900 fundamentals.",
    "gcp":               "Use Google Cloud Skills Boost. Start with Associate Cloud Engineer path.",
    "terraform":         "Use HashiCorp Learn at developer.hashicorp.com. Provision AWS resources.",
    "git":               "Use learngitbranching.js.org (interactive). Practice branching and PRs daily.",
    "linux":             "Use linuxcommand.org. Learn file system, permissions, bash scripting.",
    "machine learning":  "Start with Andrew Ng's ML course on Coursera (audit free). Practice on Kaggle.",
    "deep learning":     "Use fast.ai or DeepLearning.AI specialization. Build image classifiers first.",
    "tensorflow":        "Use tensorflow.org tutorials. Start with Keras Sequential API.",
    "pytorch":           "Use pytorch.org tutorials + Andrej Karpathy on YouTube.",
    "scikit-learn":      "Use scikit-learn.org user guide. Build classification and regression models.",
    "pandas":            "Use Kaggle's free Pandas course. Analyze a real dataset from Kaggle.",
    "numpy":             "Use numpy.org quickstart. Practice array operations and broadcasting.",
    "power bi":          "Use Microsoft Learn Power BI path. Build a dashboard from a CSV file.",
    "tableau":           "Use Tableau Public (free). Follow official training videos.",
    "spark":             "Use Databricks Community Edition (free). Learn PySpark DataFrames.",
    "kafka":             "Use Confluent's free Kafka tutorials. Run Kafka locally with Docker.",
    "airflow":           "Use official Airflow docs. Build a simple DAG with Python operators.",
    "flutter":           "Use flutter.dev official docs + Vandad Nahavandipoor on YouTube.",
    "firebase":          "Use Firebase docs. Learn Firestore, Auth, and Cloud Functions.",
    "rest api":          "Learn HTTP methods, status codes, JSON. Test APIs with Postman.",
    "graphql":           "Use howtographql.com. Build a GraphQL API with Apollo Server.",
    "ci/cd":             "Use GitHub Actions docs. Set up a pipeline that tests and deploys your app.",
    "microservices":     "Read 'Building Microservices' by Sam Newman. Start with 2 services communicating via REST.",
    "mlops":             "Use MLflow for experiment tracking. Learn model serving with FastAPI.",
    "selenium":          "Use Selenium official docs. Automate a login flow as your first project.",
    "testing":           "Learn pytest for Python. Write unit tests for a small project you've built.",
    "figma":             "Use Figma's official YouTube channel. Design a mobile app screen.",
    "statistics":        "Use Khan Academy Statistics. Learn distributions, hypothesis testing, regression.",
    "excel":             "Use ExcelJet.net. Learn VLOOKUP, pivot tables, and basic formulas.",
    "networking":        "Use Professor Messer's CompTIA Network+ course (free on YouTube).",
    "cryptography":      "Use Christof Paar's lectures on YouTube. Learn AES, RSA, and hashing.",
    "ansible":           "Use Red Hat's Ansible getting started guide. Automate server setup.",
    "monitoring":        "Learn Prometheus + Grafana. Use Docker Compose to run both locally.",
    "data pipelines":    "Learn ETL concepts. Build a pipeline with Python + Airflow or Prefect.",
}

# ── Intent patterns — strict keyword sets ─────────────────────────────────────
INTENTS = {
    "greeting":       ["hi", "hello", "hey", "hii", "howdy", "good morning", "good evening", "what's up", "sup"],
    "my_skills":      ["my skills", "what skills do i have", "skills i have", "show my skills", "list my skills", "what are my skills"],
    "missing_skills": ["missing skills", "skill gap", "what skills do i need", "what am i missing", "skills to learn", "gap analysis"],
    "resume_score":   ["resume score", "my ats score", "ats score", "how is my resume", "resume rating", "resume feedback"],
    "target_role":    ["my target role", "what is my role", "which role am i targeting", "my goal role"],
    "roadmap":        ["my roadmap", "learning plan", "study plan", "how to prepare for", "what should i learn first", "learning path"],
    "career_tips":    ["career tips", "how to get a job", "job search", "how to get hired", "interview tips", "placement tips", "internship tips", "how to crack interview"],
    "resources":      ["free resources", "best resources", "where to learn", "learning websites", "best courses", "free courses", "youtube channels"],
    "projects":       ["project ideas", "what projects to build", "portfolio projects", "project suggestions"],
    "salary":         ["salary", "how much does", "pay", "compensation", "package", "ctc"],
    "compare_roles":  ["difference between", "vs", "compare", "which is better", "data scientist vs", "frontend vs backend"],
    "help":           ["help", "what can you do", "commands", "options", "how to use"],
}

def match_intent(q: str) -> str:
    """Return the best matching intent for a query."""
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if p in q:
                return intent
    return "unknown"

def match_skill(q: str) -> str:
    """Return skill name if user is asking about a specific skill."""
    # Sort by length descending to match longer phrases first
    for skill in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        if skill in q:
            return skill
    return ""

# ── Response builder ──────────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    q = user_input.strip().lower()
    q = re.sub(r"[^\w\s/]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()

    intent = match_intent(q)
    skill  = match_skill(q)

    # ── Greeting ──────────────────────────────────────────────────────────────
    if intent == "greeting":
        role_line = f"Your target role is **{target_role}**." if target_role else "You haven't set a target role yet."
        return (
            f"Hey {name}! 👋 I'm your SkillGap assistant.\n\n"
            f"{role_line}\n\n"
            f"You can ask me:\n"
            f"- **my skills** — see what skills were detected\n"
            f"- **missing skills** — see your skill gap\n"
            f"- **how to learn python** — tips for any skill\n"
            f"- **career tips** — job search advice\n"
            f"- **my roadmap** — your learning plan"
        )

    # ── My skills ─────────────────────────────────────────────────────────────
    if intent == "my_skills":
        if not user_skills:
            return "No skills detected yet. Upload your resume on the **Resume Score** page first."
        return f"You have **{len(user_skills)} skills** detected from your resume:\n\n" + \
               "\n".join(f"• {s.title()}" for s in user_skills)

    # ── Missing skills ────────────────────────────────────────────────────────
    if intent == "missing_skills":
        if not target_role:
            return "You haven't selected a target role yet. Go to the **Skill Gap** page and pick a role first."
        if not missing:
            return f"Great news! You have all required skills for **{target_role}**. 🎉"
        skills_list = "\n".join(f"• {s.title()}" for s in missing)
        return (
            f"For **{target_role}**, you're missing **{len(missing)} skills**:\n\n"
            f"{skills_list}\n\n"
            f"Go to the **Roadmap** page to get a week-by-week learning plan."
        )

    # ── Resume score ──────────────────────────────────────────────────────────
    if intent == "resume_score":
        if resume_score == 0:
            return "You haven't uploaded a resume yet. Go to the **Resume Score** page to upload your PDF."
        if resume_score >= 70:
            tip = "Excellent resume! Make sure to tailor it for each job application."
        elif resume_score >= 40:
            tip = "Good start. Add more technical skills, quantify achievements (e.g. 'improved speed by 30%'), and use action verbs."
        else:
            tip = "Needs improvement. Add sections for Experience, Projects, Skills, and Education. Include your email and phone."
        return f"Your ATS resume score is **{resume_score}%**.\n\n💡 {tip}"

    # ── Target role ───────────────────────────────────────────────────────────
    if intent == "target_role":
        if not target_role:
            return "No target role set. Go to the **Skill Gap** page and select a role."
        total   = len(user_skills) + len(missing)
        pct     = int(len(user_skills) / total * 100) if total else 0
        return (
            f"Your target role is **{target_role}**.\n\n"
            f"You match **{pct}%** of the required skills "
            f"({len(user_skills)} matched, {len(missing)} missing)."
        )

    # ── Roadmap ───────────────────────────────────────────────────────────────
    if intent == "roadmap":
        if not target_role:
            return "Set a target role first on the **Skill Gap** page, then generate your roadmap."
        if not missing:
            return f"You already have all skills for **{target_role}**! Check the **Roadmap** page for advanced tips."
        top = missing[:3]
        lines = "\n\n".join(
            f"**{s.title()}** — {SKILL_TIPS.get(s.lower(), 'Search for beginner tutorials on YouTube.')}"
            for s in top
        )
        suffix = f"\n\n...plus {len(missing)-3} more. Go to the **Roadmap** page for the full plan." if len(missing) > 3 else ""
        return f"Start with these top priorities for **{target_role}**:\n\n{lines}{suffix}"

    # ── Specific skill question ───────────────────────────────────────────────
    if skill:
        tip = SKILL_TIPS[skill]
        has_it   = skill in [s.lower() for s in user_skills]
        needs_it = skill in [s.lower() for s in missing]
        if has_it:
            status = f"✅ You already have **{skill.title()}** in your profile."
        elif needs_it:
            status = f"❌ **{skill.title()}** is a missing skill for **{target_role}**. Here's how to learn it:"
        else:
            status = f"Here's how to learn **{skill.title()}**:"
        return f"{status}\n\n{tip}"

    # ── Career tips ───────────────────────────────────────────────────────────
    if intent == "career_tips":
        return (
            "**Job Search Tips:**\n\n"
            "1. Build 2–3 projects and push them to GitHub\n"
            "2. Optimize your LinkedIn — add skills, summary, and projects\n"
            "3. Practice DSA on LeetCode (start with Easy, then Medium)\n"
            "4. Apply on LinkedIn, Naukri, Internshala, and AngelList\n"
            "5. Prepare a 2-minute self-introduction\n"
            "6. Research the company before every interview\n\n"
            "Ask me about a specific role for more targeted advice."
        )

    # ── Resources ─────────────────────────────────────────────────────────────
    if intent == "resources":
        return (
            "**Best Free Learning Resources:**\n\n"
            "• **YouTube** — Traversy Media, Fireship, TechWorld with Nana, Corey Schafer\n"
            "• **freeCodeCamp** — Web Dev, Python, Data Analysis (free certificates)\n"
            "• **Kaggle** — Data Science & ML with real datasets\n"
            "• **Coursera** — Audit courses for free (Andrew Ng ML, Google courses)\n"
            "• **LeetCode** — DSA practice for interviews\n"
            "• **roadmap.sh** — Visual learning paths for every role\n\n"
            "Tell me a specific skill and I'll give you the exact resource."
        )

    # ── Project ideas ─────────────────────────────────────────────────────────
    if intent == "projects":
        role_projects = {
            "data scientist":       ["House price predictor", "Sentiment analysis on tweets", "Customer churn prediction"],
            "frontend developer":   ["Portfolio website", "Weather app with API", "E-commerce product page"],
            "backend developer":    ["REST API with auth", "URL shortener", "Task management API"],
            "full stack developer": ["Blog platform", "Chat app", "Job board website"],
            "devops engineer":      ["CI/CD pipeline on GitHub Actions", "Dockerized microservice", "Terraform AWS setup"],
            "ml engineer":          ["Model serving API with FastAPI", "MLflow experiment tracker", "Image classifier deployment"],
            "flutter developer":    ["Todo app", "Weather app", "Expense tracker"],
            "data analyst":         ["Sales dashboard in Power BI", "COVID data analysis", "Excel automation script"],
        }
        role_key = target_role.lower() if target_role else ""
        projects = role_projects.get(role_key, ["Build a CRUD app", "Create a REST API", "Build a data dashboard"])
        lines = "\n".join(f"• {p}" for p in projects)
        return f"**Project ideas for {target_role or 'your role'}:**\n\n{lines}\n\nEach project should go on GitHub with a README."

    # ── Salary ────────────────────────────────────────────────────────────────
    if intent == "salary":
        return (
            "**Approximate salary ranges (India, entry level):**\n\n"
            "• Frontend / Backend Developer — ₹4–8 LPA\n"
            "• Full Stack Developer — ₹5–10 LPA\n"
            "• Data Analyst — ₹4–7 LPA\n"
            "• Data Scientist — ₹6–12 LPA\n"
            "• DevOps Engineer — ₹6–12 LPA\n"
            "• ML Engineer — ₹8–15 LPA\n\n"
            "Salaries vary by company, city, and skills. Building strong projects increases your value significantly."
        )

    # ── Role comparison ───────────────────────────────────────────────────────
    if intent == "compare_roles":
        if "data scientist" in q and "data analyst" in q:
            return (
                "**Data Analyst vs Data Scientist:**\n\n"
                "• **Data Analyst** — focuses on reporting, dashboards, SQL, Excel, Power BI. Less coding.\n"
                "• **Data Scientist** — builds ML models, needs Python, statistics, and ML frameworks.\n\n"
                "Start as a Data Analyst if you're new to data. Move to Data Scientist after learning ML."
            )
        if "frontend" in q and "backend" in q:
            return (
                "**Frontend vs Backend:**\n\n"
                "• **Frontend** — builds what users see. HTML, CSS, JavaScript, React.\n"
                "• **Backend** — builds server logic, APIs, databases. Python, Node, SQL, Docker.\n\n"
                "Full Stack = both. Start with Frontend if you like visual work, Backend if you prefer logic."
            )
        if "ml engineer" in q and "data scientist" in q:
            return (
                "**Data Scientist vs ML Engineer:**\n\n"
                "• **Data Scientist** — explores data, builds models, focuses on insights.\n"
                "• **ML Engineer** — deploys and scales models in production. More software engineering.\n\n"
                "Data Scientist = more research. ML Engineer = more engineering."
            )
        return "Ask me to compare two specific roles, e.g. 'data scientist vs data analyst'."

    # ── Help ──────────────────────────────────────────────────────────────────
    if intent == "help":
        return (
            "Here's what you can ask me:\n\n"
            "• **my skills** — skills detected from your resume\n"
            "• **missing skills** — your skill gap for the target role\n"
            "• **my resume score** — ATS score and tips\n"
            "• **my roadmap** — top skills to learn next\n"
            "• **how to learn python** — tips for any specific skill\n"
            "• **career tips** — job search and interview advice\n"
            "• **project ideas** — what to build for your portfolio\n"
            "• **free resources** — best websites to learn from\n"
            "• **salary** — expected pay ranges\n"
            "• **data scientist vs data analyst** — role comparisons"
        )

    # ── Unknown ───────────────────────────────────────────────────────────────
    # Try one more time — check if any skill word is in the query
    for skill_key in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        words = skill_key.split()
        if all(w in q for w in words):
            tip = SKILL_TIPS[skill_key]
            return f"**{skill_key.title()}:**\n\n{tip}"

    return (
        f"I didn't quite understand that. Here are things I can help with:\n\n"
        f"• Type **my skills** to see your detected skills\n"
        f"• Type **missing skills** to see your gap\n"
        f"• Type **how to learn docker** for any skill tips\n"
        f"• Type **career tips** for job search advice\n"
        f"• Type **help** to see all options"
    )


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("## 🤖 SkillGap Chatbot")
st.caption("Ask me about your skills, learning path, career tips, or any tech skill.")
st.markdown("")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "bot",
        "text": (
            f"Hey {name}! 👋 I'm your SkillGap assistant.\n\n"
            f"{'Your target role is **' + target_role + '**. ' if target_role else ''}"
            f"{'You have **' + str(len(user_skills)) + '** skills and are missing **' + str(len(missing)) + '**.' if user_skills else 'Upload your resume to get started.'}\n\n"
            f"Ask me anything — type **help** to see what I can do."
        )
    }]

# Quick buttons
q1, q2, q3, q4, q5 = st.columns(5)
quick_prompts = [
    (q1, "📋 My Skills",      "my skills"),
    (q2, "❌ Missing Skills", "missing skills"),
    (q3, "📄 Resume Score",   "my resume score"),
    (q4, "🛤️ My Roadmap",     "my roadmap"),
    (q5, "💼 Career Tips",    "career tips"),
]
for col, label, prompt in quick_prompts:
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            st.session_state.chat_history.append({"role": "bot",  "text": get_response(prompt)})
            st.rerun()

st.markdown("---")

# Chat history
for msg in st.session_state.chat_history:
    css = "user-msg" if msg["role"] == "user" else "bot-msg"
    prefix = "🧑" if msg["role"] == "user" else "🤖"
    # Render newlines as <br>
    text = msg["text"].replace("\n", "<br>")
    st.markdown(f'<div class="{css}">{prefix} {text}</div>', unsafe_allow_html=True)

st.markdown("")

# Input form
with st.form("chat_form", clear_on_submit=True):
    c1, c2 = st.columns([6, 1])
    with c1:
        user_input = st.text_input("", placeholder="e.g. how to learn docker, missing skills, career tips...",
                                   label_visibility="collapsed")
    with c2:
        sent = st.form_submit_button("Send", use_container_width=True, type="primary")

if sent and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
    st.session_state.chat_history.append({"role": "bot",  "text": get_response(user_input.strip())})
    st.rerun()

if len(st.session_state.chat_history) > 3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [{
            "role": "bot",
            "text": f"Chat cleared. How can I help you, {name}?"
        }]
        st.rerun()
