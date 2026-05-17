"""Rule-based chatbot for SkillGap Analyzer — broad app topics, off-topic guard."""

import re
from typing import Any

SKILL_TIPS: dict[str, str] = {
    "python": "Start with python.org tutorial. Build small scripts, then move to Flask/FastAPI. Practice on HackerRank.",
    "javascript": "Use javascript.info — best free resource. Build DOM projects, then learn ES6+, then React.",
    "typescript": "Learn after JavaScript. Start with the official TypeScript Handbook at typescriptlang.org.",
    "java": "Start with Java Brains on YouTube. Learn OOP, then Spring Boot for backend APIs.",
    "kotlin": "Use official Kotlin docs + Philipp Lackner on YouTube for Android development.",
    "swift": "Use Apple's official Swift tutorials at developer.apple.com. Build iOS apps with SwiftUI.",
    "dart": "Start at dartpad.dev. Learn syntax, then move to Flutter.",
    "html": "Use MDN Web Docs. Build 5 static pages. Focus on semantic HTML.",
    "css": "Practice Flexbox Froggy and Grid Garden. Then build real layouts.",
    "react": "Use react.dev (official docs). Build a todo app, then a weather app with API.",
    "vue": "Use vuejs.org official guide. Build a simple CRUD app.",
    "angular": "Use angular.io tour of heroes tutorial. Learn components, services, and routing.",
    "node": "Use Traversy Media Node.js crash course. Build a REST API with Express.",
    "django": "Use official Django tutorial (djangoproject.com). Build a blog app.",
    "flask": "Use official Flask docs. Build a simple REST API.",
    "fastapi": "Use fastapi.tiangolo.com docs. Build a CRUD API with Pydantic models.",
    "sql": "Practice on SQLZoo and Mode Analytics. Focus on JOINs, GROUP BY, window functions.",
    "postgresql": "Use official PostgreSQL tutorial. Learn indexing and EXPLAIN ANALYZE.",
    "mongodb": "Use MongoDB University free courses. Learn aggregation pipeline.",
    "mysql": "Use W3Schools SQL + practice on db-fiddle.com.",
    "redis": "Use redis.io docs. Learn caching, pub/sub, and session storage patterns.",
    "docker": "Use TechWorld with Nana on YouTube. Containerize a Python app first.",
    "kubernetes": "Learn Docker first, then use kubernetes.io tutorials. Use Minikube locally.",
    "aws": "Start with AWS Free Tier. Learn EC2, S3, Lambda. Use AWS Skill Builder.",
    "azure": "Use Microsoft Learn (learn.microsoft.com). Start with AZ-900 fundamentals.",
    "gcp": "Use Google Cloud Skills Boost. Start with Associate Cloud Engineer path.",
    "terraform": "Use HashiCorp Learn at developer.hashicorp.com. Provision AWS resources.",
    "git": "Use learngitbranching.js.org (interactive). Practice branching and PRs daily.",
    "linux": "Use linuxcommand.org. Learn file system, permissions, bash scripting.",
    "machine learning": "Start with Andrew Ng's ML course on Coursera (audit free). Practice on Kaggle.",
    "deep learning": "Use fast.ai or DeepLearning.AI specialization. Build image classifiers first.",
    "tensorflow": "Use tensorflow.org tutorials. Start with Keras Sequential API.",
    "pytorch": "Use pytorch.org tutorials + Andrej Karpathy on YouTube.",
    "scikit-learn": "Use scikit-learn.org user guide. Build classification and regression models.",
    "pandas": "Use Kaggle's free Pandas course. Analyze a real dataset from Kaggle.",
    "numpy": "Use numpy.org quickstart. Practice array operations and broadcasting.",
    "power bi": "Use Microsoft Learn Power BI path. Build a dashboard from a CSV file.",
    "tableau": "Use Tableau Public (free). Follow official training videos.",
    "spark": "Use Databricks Community Edition (free). Learn PySpark DataFrames.",
    "kafka": "Use Confluent's free Kafka tutorials. Run Kafka locally with Docker.",
    "airflow": "Use official Airflow docs. Build a simple DAG with Python operators.",
    "flutter": "Use flutter.dev official docs + Vandad Nahavandipoor on YouTube.",
    "firebase": "Use Firebase docs. Learn Firestore, Auth, and Cloud Functions.",
    "rest api": "Learn HTTP methods, status codes, JSON. Test APIs with Postman.",
    "graphql": "Use howtographql.com. Build a GraphQL API with Apollo Server.",
    "ci/cd": "Use GitHub Actions docs. Set up a pipeline that tests and deploys your app.",
    "microservices": "Read 'Building Microservices' by Sam Newman. Start with 2 services communicating via REST.",
    "mlops": "Use MLflow for experiment tracking. Learn model serving with FastAPI.",
    "selenium": "Use Selenium official docs. Automate a login flow as your first project.",
    "testing": "Learn pytest for Python. Write unit tests for a small project you've built.",
    "figma": "Use Figma's official YouTube channel. Design a mobile app screen.",
    "statistics": "Use Khan Academy Statistics. Learn distributions, hypothesis testing, regression.",
    "excel": "Use ExcelJet.net. Learn VLOOKUP, pivot tables, and basic formulas.",
    "networking": "Use Professor Messer's CompTIA Network+ course (free on YouTube).",
    "cryptography": "Use Christof Paar's lectures on YouTube. Learn AES, RSA, and hashing.",
    "ansible": "Use Red Hat's Ansible getting started guide. Automate server setup.",
    "monitoring": "Learn Prometheus + Grafana. Use Docker Compose to run both locally.",
    "data pipelines": "Learn ETL concepts. Build a pipeline with Python + Airflow or Prefect.",
    "c++": "Use learncpp.com. Build small console programs, then learn STL and pointers.",
    "c#": "Use Microsoft's C# docs. Build a console app, then try ASP.NET Core.",
    "go": "Use go.dev tour and official docs. Build a CLI tool and a simple HTTP server.",
    "rust": "Use the Rust Book (doc.rust-lang.org/book). Build small CLI tools first.",
    "ruby": "Use ruby-lang.org docs. Try Rails with the official Getting Started guide.",
    "php": "Use php.net manual. Build a simple CRUD app with Laravel or plain PHP.",
    "spring": "Learn Java first, then Spring Boot docs. Build a REST API with JPA.",
    "next.js": "Learn React first, then nextjs.org docs. Build a blog or portfolio site.",
    "tailwind": "Use tailwindcss.com docs. Rebuild a landing page with utility classes.",
    "blockchain": "Learn basics on ethereum.org. Try a simple smart contract tutorial on Remix.",
    "cybersecurity": "Try TryHackMe and OWASP Top 10. Learn networking and Linux basics first.",
}

INTENTS: dict[str, list[str]] = {
    "greeting": [
        "hi", "hello", "hey", "hii", "howdy", "good morning", "good evening",
        "what's up", "sup",
    ],
    "my_skills": [
        "my skills", "what skills do i have", "skills i have", "show my skills",
        "list my skills", "what are my skills", "skills on my resume",
    ],
    "missing_skills": [
        "missing skills", "skill gap", "what skills do i need", "what am i missing",
        "skills to learn", "gap analysis", "skills i lack", "what should i learn",
    ],
    "resume_score": [
        "resume score", "my ats score", "ats score", "how is my resume",
        "resume rating", "resume feedback", "ats friendly", "parse my resume",
    ],
    "target_role": [
        "my target role", "what is my role", "which role am i targeting",
        "my goal role", "career goal", "role am i aiming",
    ],
    "roadmap": [
        "my roadmap", "learning plan", "study plan", "how to prepare for",
        "what should i learn first", "learning path", "week by week",
    ],
    "career_tips": [
        "career tips", "how to get a job", "job search", "how to get hired",
        "interview tips", "placement tips", "internship tips", "how to crack interview",
        "fresher job", "campus placement", "how to apply",
    ],
    "resources": [
        "free resources", "best resources", "where to learn", "learning websites",
        "best courses", "free courses", "youtube channels", "recommend a course",
    ],
    "projects": [
        "project ideas", "what projects to build", "portfolio projects",
        "project suggestions", "github projects", "what to build",
    ],
    "salary": [
        "salary", "how much does", "pay", "compensation", "package", "ctc", "lpa",
    ],
    "compare_roles": [
        "difference between", " vs ", "compare", "which is better",
        "data scientist vs", "frontend vs backend", "better role",
    ],
    "improve_resume": [
        "improve resume", "better resume", "resume tips", "fix my resume",
        "resume format", "resume section", "make resume stronger",
    ],
    "interview_prep": [
        "interview question", "prepare for interview", "technical interview",
        "hr interview", "mock interview", "coding interview", "system design",
    ],
    "linkedin": [
        "linkedin", "linkedin profile", "optimize linkedin", "linkedin headline",
    ],
    "certification": [
        "certification", "certificate", "certified", "which cert", "aws cert",
    ],
    "what_next": [
        "what should i do", "what next", "next steps", "where do i start",
        "how do i start", "getting started", "am i ready", "readiness",
    ],
    "app_help": [
        "how to use", "how does this app", "skillgap", "skill gap analyzer",
        "upload resume", "resume builder", "dashboard", "analytics page",
        "profile page", "sign up", "change role", "theme",
    ],
    "help": ["help", "what can you do", "commands", "options", "topics"],
}

# Off-topic unless paired with app-related keywords
OFF_TOPIC_WORDS = [
    "weather", "joke", "recipe", "pizza", "football", "cricket", "movie",
    "netflix", "horoscope", "bitcoin", "crypto", "president", "politics",
    "symptoms", "diagnose", "dating", "breakup", "fortnite", "minecraft",
]

OFF_TOPIC_PHRASES = [
    "weather forecast", "what's the weather", "what is the weather", "temperature today",
    "football score", "cricket match", "who won the game",
    "recipe for", "cook pasta", "pizza recipe",
    "movie review", "watch netflix", "song lyrics", "sing a song",
    "tell me a joke", "write a poem", "write a story about",
    "horoscope", "astrology", "zodiac sign",
    "bitcoin price", "stock price today", "crypto trading tip",
    "who is the president", "politics", "election result",
    "medical advice", "doctor diagnose", "symptoms of disease",
    "legal advice", "lawyer", "sue someone",
    "dating advice", "relationship problem", "break up with",
    "homework help math", "solve this equation", "algebra problem",
    "translate this paragraph to french", "translate to spanish",
    "play a game", "chess move", "fortnite",
    "capital of france", "trivia about animals",
    "buy iphone", "best phone to buy", "shopping deal",
]

APP_RELATED_KEYWORDS = [
    "skill", "resume", "cv", "ats", "job", "career", "interview", "internship",
    "roadmap", "learn", "study", "course", "certification", "portfolio", "github",
    "leetcode", "hackerrank", "salary", "role", "developer", "engineer", "analyst",
    "scientist", "gap", "upload", "score", "profile", "target", "missing", "project",
    "placement", "hire", "apply", "linkedin", "skillgap", "python", "java", "react",
    "docker", "aws", "sql", "data", "frontend", "backend", "full stack", "devops",
    "machine learning", "ml", "ai", "coding", "programming", "tech", "software",
    "fresher", "experienced", "resume builder", "skill gap", "analytics",
]

LEARNING_PATTERNS = [
    r"how (?:do i |to |can i )?learn (.+)",
    r"how (?:do i |to )?get started (?:with )?(.+)",
    r"tips (?:for|on) (.+)",
    r"best way to learn (.+)",
    r"resources (?:for|on) (.+)",
    r"(?:want|need) to learn (.+)",
    r"should i learn (.+)",
    r"teach me (.+)",
    r"explain (.+)",
    r"what is (.+)",
    r"what are (.+)",
]

OFF_TOPIC_REPLY = (
    "I can only help with topics related to **SkillGap Analyzer** — skills, resumes, "
    "skill gaps, roadmaps, interviews, career growth, and learning tech.\n\n"
    "Please ask a question related to the app. Type **help** to see examples."
)

ROLE_PROJECTS = {
    "data scientist": ["House price predictor", "Sentiment analysis on tweets", "Customer churn prediction"],
    "frontend developer": ["Portfolio website", "Weather app with API", "E-commerce product page"],
    "backend developer": ["REST API with auth", "URL shortener", "Task management API"],
    "full stack developer": ["Blog platform", "Chat app", "Job board website"],
    "devops engineer": ["CI/CD pipeline on GitHub Actions", "Dockerized microservice", "Terraform AWS setup"],
    "ml engineer": ["Model serving API with FastAPI", "MLflow experiment tracker", "Image classifier deployment"],
    "flutter developer": ["Todo app", "Weather app", "Expense tracker"],
    "data analyst": ["Sales dashboard in Power BI", "COVID data analysis", "Excel automation script"],
}


def normalize_query(text: str) -> str:
    q = text.strip().lower()
    q = re.sub(r"[^\w\s/]", " ", q)
    return re.sub(r"\s+", " ", q).strip()


def match_intent(q: str) -> str:
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if p in q:
                return intent
    return "unknown"


def match_skill(q: str) -> str:
    for skill in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        if skill in q:
            return skill
    for skill_key in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        words = skill_key.split()
        if all(w in q for w in words):
            return skill_key
    return ""


def _subject_is_off_topic(subject: str) -> bool:
    s = subject.lower()
    return any(w in s for w in OFF_TOPIC_WORDS)


def extract_learning_subject(q: str) -> str:
    for pat in LEARNING_PATTERNS:
        m = re.search(pat, q)
        if not m:
            continue
        subject = m.group(1).strip()
        subject = re.sub(r"\b(in|for|as a|as an)\b.*$", "", subject).strip()
        if len(subject) < 2 or _subject_is_off_topic(subject):
            continue
        found = match_skill(subject)
        if found:
            return found
        if _subject_is_off_topic(q):
            continue
        return subject
    return ""


def is_app_related(q: str) -> bool:
    if match_intent(q) not in ("unknown",):
        return True
    if match_skill(q):
        return True
    if extract_learning_subject(q):
        return True
    return any(kw in q for kw in APP_RELATED_KEYWORDS)


def is_off_topic(q: str) -> bool:
    for phrase in OFF_TOPIC_PHRASES:
        if phrase in q:
            return True
    for word in OFF_TOPIC_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", q):
            if not any(kw in q for kw in APP_RELATED_KEYWORDS):
                return True
    if match_intent(q) != "unknown":
        return False
    if match_skill(q):
        return False
    if extract_learning_subject(q):
        return False
    return not any(kw in q for kw in APP_RELATED_KEYWORDS)


def skill_response(skill: str, ctx: dict[str, Any]) -> str:
    tip = SKILL_TIPS.get(skill, (
        f"Search YouTube for '{skill} tutorial for beginners', follow official docs, "
        "and build one small project this week. Add it to your resume when done."
    ))
    user_skills = ctx.get("user_skills") or []
    missing = ctx.get("missing") or []
    target_role = ctx.get("target_role") or ""
    has_it = skill in [s.lower() for s in user_skills]
    needs_it = skill in [s.lower() for s in missing]
    if has_it:
        status = f"You already have **{skill.title()}** on your profile."
    elif needs_it:
        status = f"**{skill.title()}** is a gap skill for **{target_role}**. Here's how to learn it:"
    else:
        status = f"Here's how to learn **{skill.title()}**:"
    return f"{status}\n\n{tip}"


def generic_app_response(q: str, ctx: dict[str, Any]) -> str:
    name = ctx.get("name", "there")
    target_role = ctx.get("target_role") or ""
    missing = ctx.get("missing") or []
    user_skills = ctx.get("user_skills") or []
    resume_score = ctx.get("resume_score", 0)

    hints = []
    if not user_skills:
        hints.append("Upload your resume on **Resume Score** to detect skills.")
    if not target_role:
        hints.append("Pick a target role on **Skill Gap** for personalized advice.")
    elif missing:
        hints.append(f"Focus on **{missing[0].title()}** — it's a top gap for **{target_role}**.")
    if resume_score and resume_score < 60:
        hints.append("Improve your ATS score on **Resume Score** before applying widely.")
    if not hints:
        hints.append("Check **Roadmap** for your week-by-week plan and **Analytics** for progress.")

    return (
        f"Here's guidance based on your SkillGap profile, {name}:\n\n"
        + "\n".join(f"• {h}" for h in hints)
        + "\n\nYou can also ask: **my skills**, **missing skills**, **how to learn python**, "
        "**career tips**, or **project ideas**."
    )


def get_response(user_input: str, ctx: dict[str, Any]) -> str:
    q = normalize_query(user_input)
    if not q:
        return "Please type a question. Type **help** for ideas."

    intent = match_intent(q)
    skill = match_skill(q)
    name = ctx.get("name", "there")
    user_skills = ctx.get("user_skills") or []
    missing = ctx.get("missing") or []
    target_role = ctx.get("target_role") or ""
    resume_score = ctx.get("resume_score", 0)

    if intent in ("greeting",) or q in ("hi", "hello", "hey"):
        role_line = f"Your target role is **{target_role}**." if target_role else "Set a target role on **Skill Gap** when you're ready."
        return (
            f"Hey {name}! I'm your SkillGap assistant.\n\n"
            f"{role_line}\n\n"
            "Ask me about skills, resumes, roadmaps, interviews, learning any tech skill, "
            "or type **help** for examples."
        )

    if q in ("thanks", "thank you", "thx"):
        return "You're welcome! Ask anytime about your career path or skills."

    if q in ("bye", "goodbye", "see you"):
        return f"Good luck, {name}! Come back when you need career or learning help."

    if intent == "help":
        return (
            "**I can help with anything related to SkillGap Analyzer:**\n\n"
            "• **my skills** / **missing skills** / **resume score** / **my roadmap**\n"
            "• **how to learn docker** (or any tech skill)\n"
            "• **career tips** / **interview prep** / **project ideas** / **salary**\n"
            "• **improve resume** / **linkedin** / **what should I do next**\n"
            "• Role comparisons, certifications, and learning resources\n\n"
            "Off-topic questions (weather, jokes, general trivia) aren't supported — "
            "please keep questions related to careers and this app."
        )

    if intent == "my_skills":
        if not user_skills:
            return "No skills detected yet. Upload your resume on **Resume Score** first."
        return f"You have **{len(user_skills)} skills** from your resume:\n\n" + \
               "\n".join(f"• {s.title()}" for s in user_skills)

    if intent == "missing_skills":
        if not target_role:
            return "Select a target role on **Skill Gap** first."
        if not missing:
            return f"You match all core skills for **{target_role}**."
        return (
            f"For **{target_role}**, you're missing **{len(missing)} skills**:\n\n"
            + "\n".join(f"• {s.title()}" for s in missing)
            + "\n\nSee **Roadmap** for a full learning plan."
        )

    if intent == "resume_score":
        if resume_score == 0:
            return "Upload your resume on **Resume Score** to get an ATS score."
        if resume_score >= 70:
            tip = "Strong resume — tailor keywords per job posting."
        elif resume_score >= 40:
            tip = "Add quantified achievements, more skills, and action verbs."
        else:
            tip = "Add Experience, Projects, Skills, Education, and contact details."
        return f"Your ATS score is **{resume_score}%**.\n\n{tip}"

    if intent == "target_role":
        if not target_role:
            return "No target role set. Choose one on **Skill Gap**."
        total = len(user_skills) + len(missing)
        pct = int(len(user_skills) / total * 100) if total else 0
        return (
            f"Target role: **{target_role}** — **{pct}%** skill match "
            f"({len(user_skills)} matched, {len(missing)} missing)."
        )

    if intent == "roadmap":
        if not target_role:
            return "Set a target role on **Skill Gap**, then open **Roadmap**."
        if not missing:
            return f"You're well covered for **{target_role}**. Use **Roadmap** for advanced topics."
        top = missing[:3]
        lines = "\n\n".join(
            f"**{s.title()}** — {SKILL_TIPS.get(s.lower(), 'Find a beginner tutorial on YouTube.')}"
            for s in top
        )
        extra = f"\n\n+{len(missing) - 3} more on **Roadmap**." if len(missing) > 3 else ""
        return f"Top priorities for **{target_role}**:\n\n{lines}{extra}"

    if skill:
        return skill_response(skill, ctx)

    learn_subject = extract_learning_subject(q)
    if learn_subject:
        sk = match_skill(learn_subject) or learn_subject
        return skill_response(sk.lower(), ctx)

    if is_off_topic(q):
        return OFF_TOPIC_REPLY

    if intent == "career_tips":
        return (
            "**Job search tips:**\n\n"
            "1. Build 2–3 projects on GitHub with READMEs\n"
            "2. Optimize LinkedIn — skills, summary, projects\n"
            "3. Practice DSA (LeetCode Easy → Medium)\n"
            "4. Apply on LinkedIn, Naukri, Internshala\n"
            "5. Prepare a 2-minute intro and STAR stories\n"
            "6. Research each company before interviews"
        )

    if intent == "resources":
        return (
            "**Free learning resources:**\n\n"
            "• YouTube — Traversy Media, Fireship, Corey Schafer\n"
            "• freeCodeCamp, Kaggle, roadmap.sh\n"
            "• Coursera (audit free), LeetCode\n\n"
            "Ask **how to learn [skill]** for specific paths."
        )

    if intent == "projects":
        role_key = target_role.lower() if target_role else ""
        projects = ROLE_PROJECTS.get(role_key, ["CRUD app", "REST API", "Data dashboard"])
        return "**Project ideas:**\n\n" + "\n".join(f"• {p}" for p in projects) + \
               "\n\nHost on GitHub with a clear README."

    if intent == "salary":
        return (
            "**Entry-level ranges (India, approximate):**\n\n"
            "• Frontend/Backend — ₹4–8 LPA\n"
            "• Full Stack — ₹5–10 LPA\n"
            "• Data Analyst — ₹4–7 LPA\n"
            "• Data Scientist — ₹6–12 LPA\n"
            "• DevOps / ML Engineer — ₹6–15 LPA"
        )

    if intent == "compare_roles":
        if "data scientist" in q and "data analyst" in q:
            return "**Data Analyst** — dashboards, SQL, reporting.\n**Data Scientist** — ML models, Python, stats."
        if "frontend" in q and "backend" in q:
            return "**Frontend** — UI (HTML/CSS/JS/React).\n**Backend** — APIs, databases, servers."
        if "ml engineer" in q and "data scientist" in q:
            return "**Data Scientist** — modeling & insights.\n**ML Engineer** — production deployment."
        return "Name two roles to compare, e.g. *data scientist vs data analyst*."

    if intent == "improve_resume":
        return (
            "**Resume tips:**\n\n"
            "• One page for freshers; clear sections\n"
            "• Bullet points with numbers (e.g. 'reduced load time 30%')\n"
            "• Match keywords from job descriptions\n"
            "• List projects with tech stack and links\n"
            "• Use **Resume Builder** and check **Resume Score** in this app"
        )

    if intent == "interview_prep":
        return (
            "**Interview prep:**\n\n"
            "• Revise your top 3 projects deeply\n"
            "• Practice Easy/Medium LeetCode for tech roles\n"
            "• Prepare 'tell me about yourself' and 'why this role'\n"
            "• Review skills from **Skill Gap** for your target role\n"
            "• Do 1–2 mock interviews with a friend"
        )

    if intent == "linkedin":
        return (
            "**LinkedIn tips:**\n\n"
            "• Headline: role + key skills (e.g. 'Aspiring Data Scientist | Python | SQL')\n"
            "• Summary: 3–4 lines on goals and projects\n"
            "• Add skills from your **Skill Gap** profile\n"
            "• Post about projects you build"
        )

    if intent == "certification":
        return (
            "**Useful certs (by path):**\n\n"
            "• Cloud — AWS Cloud Practitioner, Azure AZ-900\n"
            "• Data — Google Data Analytics, IBM Data Science\n"
            "• DevOps — CKA, AWS Solutions Architect (after basics)\n\n"
            "Projects often matter more than certs for freshers."
        )

    if intent == "what_next":
        return generic_app_response(q, ctx)

    if intent == "app_help":
        return (
            "**Using SkillGap Analyzer:**\n\n"
            "1. **Resume Score** — upload PDF, get ATS score\n"
            "2. **Skill Gap** — pick target role, see gaps\n"
            "3. **Roadmap** — weekly learning plan\n"
            "4. **Resume Builder** — create/download resume\n"
            "5. **Analytics** — track progress\n"
            "6. **Chatbot** — ask career & skill questions (here!)"
        )

    if is_app_related(q):
        return generic_app_response(q, ctx)

    return OFF_TOPIC_REPLY
