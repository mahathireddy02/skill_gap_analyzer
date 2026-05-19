"""Rule-based chatbot for SkillGap Analyzer — broad app topics, off-topic guard."""

import re
from difflib import SequenceMatcher
from typing import Any

from utils.readiness import calculate_readiness

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
    "change_target_role": [
        "change target role", "change my target role", "change role",
        "edit target role", "edit my role", "update target role",
        "update my role", "set target role", "set my role",
        "where can i change target role", "where to change target role",
        "where can i change my role", "how to change target role",
        "how can i change my role", "how do i change my role",
        "chnaeg taget role", "change taget role", "chnaeg target role",
    ],
    "roadmap": [
        "my roadmap", "learning plan", "study plan", "how to prepare for",
        "what should i learn first", "learning path", "week by week",
        "roadmap", "study schedule", "learning schedule", "plan for",
        "prepare for", "make me a study plan",
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
        "projects should i build", "suggest projects", "build for",
    ],
    "salary": [
        "salary", "how much does", "pay", "compensation", "package", "ctc", "lpa",
    ],
    "compare_roles": [
        "difference between", " vs ", "compare", "which is better",
        "data scientist vs", "frontend vs backend", "better role",
        "frontend or backend", "backend or frontend",
    ],
    "improve_resume": [
        "improve resume", "better resume", "resume tips", "fix my resume",
        "resume format", "resume section", "make resume stronger",
        "improve my cv", "fix my cv", "better cv", "cv tips",
    ],
    "template_suggestion": [
        "best template", "which template", "template is best", "best resume template",
        "suggest template", "recommend template", "choose template", "template out of four",
        "best template out of four", "which resume template should i use",
        "whihc is the best template", "which is the best template",
        "template for my target role", "template for target role", "template for my role",
        "best template our of four", "best template out of 4", "template out of 4",
    ],
    "interview_prep": [
        "interview question", "prepare for interview", "technical interview",
        "hr interview", "mock interview", "coding interview", "system design",
        "interview preparation", "prep for interview", "crack interview",
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
    "theme_change": [
        "change to light theme", "switch to light theme", "make it light",
        "light theme", "light mode", "change to dark theme", "switch to dark theme",
        "make it dark", "dark theme", "dark mode", "change theme", "switch theme",
        "lighth", "lite theme", "lite mode", "darkh", "drak theme", "drak mode",
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
    "I don't answer such questions that are irrelevant. "
    "Ask me something relevant to **SkillGap Analyzer**."
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

APP_GUIDES: dict[str, dict[str, Any]] = {
    "resume_score": {
        "keywords": [
            "resume score", "ats", "upload resume", "upload my resume",
            "score resume", "score my resume", "check resume", "check my resume", "parse resume",
        ],
        "answer": (
            "Use **Resume Score** to upload your resume and get an ATS score.\n\n"
            "Steps:\n"
            "1. Open **Resume Score** from the top navigation.\n"
            "2. Upload your PDF resume.\n"
            "3. Review the ATS score, detected skills, and suggestions.\n"
            "4. Use **Skill Gap** after that to compare your skills with your target role."
        ),
    },
    "skill_gap": {
        "keywords": ["skill gap", "missing skills", "analyze gap", "check gap", "find gap"],
        "answer": (
            "Use **Skill Gap** to compare your skills with your target role.\n\n"
            "Steps:\n"
            "1. Make sure your **Target Role** is saved in **Profile**.\n"
            "2. Open **Skill Gap** from the top navigation.\n"
            "3. Click **Analyze Gap**.\n"
            "4. Review matched and missing skills, then open **Roadmap** for a learning plan."
        ),
    },
    "roadmap": {
        "keywords": ["roadmap", "learning plan", "study plan", "weekly plan", "week by week"],
        "answer": (
            "Use **Roadmap** to see your learning plan.\n\n"
            "Steps:\n"
            "1. Save a target role in **Profile**.\n"
            "2. Run **Skill Gap** so the app knows your missing skills.\n"
            "3. Open **Roadmap** from the top navigation.\n"
            "4. Follow the weekly tasks and mark progress as you complete them."
        ),
    },
    "resume_builder": {
        "keywords": ["resume builder", "build resume", "create resume", "download resume", "make resume"],
        "answer": (
            "Use **Resume Builder** to create and download a resume.\n\n"
            "Steps:\n"
            "1. Open **Resume Builder** from the top navigation.\n"
            "2. Fill in your personal details, education, skills, projects, and experience.\n"
            "3. Choose a template.\n"
            "4. Download the finished resume."
        ),
    },
    "analytics": {
        "keywords": ["analytics", "progress", "track progress", "stats", "dashboard chart"],
        "answer": (
            "Use **Analytics** to track your progress.\n\n"
            "It shows your resume score, target role, skills found, missing skills, and roadmap progress."
        ),
    },
    "profile": {
        "keywords": ["profile", "edit profile", "change name", "bio", "career preferences", "preferences"],
        "answer": (
            "Use **Profile** to update your account and career details.\n\n"
            "You can edit your name, target role, bio, and career preferences, then click **Save Profile**."
        ),
    },
    "dashboard": {
        "keywords": ["dashboard", "home page", "main page", "overview"],
        "answer": (
            "Use **Dashboard** for a quick overview of your SkillGap account.\n\n"
            "It summarizes your target role, readiness, resume score, skills, and quick links to the main tools."
        ),
    },
}

PAGE_TARGETS: list[tuple[str, str, list[str]]] = [
    ("Dashboard", "pages/3_Dashboard.py", ["dashboard", "home", "home page", "main page", "overview"]),
    ("Resume Score", "pages/4_Resume_Score.py", ["resume score", "resume page", "ats", "resume upload", "upload resume", "score page"]),
    ("Skill Gap", "pages/5_Skill_Gap.py", ["skill gap", "gap analyzer", "skill analyzer", "missing skills"]),
    ("Roadmap", "pages/6_Roadmap.py", ["roadmap", "learning plan", "study plan"]),
    ("Analytics", "pages/7_Analytics.py", ["analytics", "stats", "progress page", "progress"]),
    ("Profile", "pages/8_Profile.py", ["profile", "account", "settings", "career preferences"]),
    ("Chatbot", "pages/9_Chatbot.py", ["chatbot", "chat bot", "assistant"]),
    ("Resume Builder", "pages/10_Resume_Builder.py", ["resume builder", "builder", "create resume", "make resume"]),
]


def normalize_query(text: str) -> str:
    q = text.strip().lower()
    q = re.sub(r"[^\w\s/]", " ", q)
    return re.sub(r"\s+", " ", q).strip()


def similar_text(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def fuzzy_contains(q: str, phrase: str, threshold: float = 0.82) -> bool:
    q = q.lower().strip()
    phrase = phrase.lower().strip()
    if not q or not phrase:
        return False
    if phrase in q:
        return True

    q_words = q.split()
    p_words = phrase.split()
    if not q_words or not p_words:
        return False

    if len(p_words) == 1:
        return any(similar_text(word, phrase) >= threshold for word in q_words)

    window = len(p_words)
    for i in range(0, len(q_words) - window + 1):
        chunk = " ".join(q_words[i:i + window])
        if similar_text(chunk, phrase) >= threshold:
            return True
    return False


def fuzzy_any(q: str, phrases: list[str], threshold: float = 0.82) -> bool:
    return any(fuzzy_contains(q, phrase, threshold) for phrase in phrases)


def match_intent(q: str) -> str:
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if len(p) <= 3:
                if re.search(rf"\b{re.escape(p)}\b", q):
                    return intent
            elif fuzzy_contains(q, p):
                return intent
    return "unknown"


def match_skill(q: str) -> str:
    for skill in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        if fuzzy_contains(q, skill):
            return skill
    for skill_key in sorted(SKILL_TIPS.keys(), key=len, reverse=True):
        words = skill_key.split()
        if all(fuzzy_contains(q, w, 0.82) for w in words):
            return skill_key
    return ""


def detect_page_navigation(q: str) -> tuple[str, str]:
    wants_navigation = fuzzy_any(q, ["go", "open", "take", "navigate", "visit", "move", "switch", "show", "view", "page"], 0.70) or re.search(
        r"\b(go|open|take|navigate|visit|move|switch|show|view)\b", q
    ) is not None
    if not wants_navigation:
        return "", ""

    for label, path, aliases in PAGE_TARGETS:
        if fuzzy_any(q, aliases, 0.78):
            return label, path
    return "", ""


def is_target_role_change_question(q: str) -> bool:
    has_role = fuzzy_any(q, ["role", "target", "taget", "goal"], 0.75)
    has_change_word = fuzzy_any(q, ["change", "chnaeg", "chnage", "edit", "update", "set", "choose", "select", "where", "how"], 0.75)
    return has_role and has_change_word


def app_guide_response(q: str) -> str:
    for guide in APP_GUIDES.values():
        if fuzzy_any(q, guide["keywords"]):
            return guide["answer"]
    return ""


def is_app_navigation_question(q: str) -> bool:
    return fuzzy_any(q, ["where", "how", "what is", "open", "go", "find", "use", "upload", "download", "check", "see", "view"], 0.78)


def is_template_question(q: str) -> bool:
    has_template = fuzzy_any(q, ["template", "templates"], 0.78)
    wants_advice = fuzzy_any(q, ["best", "which", "suggest", "recommend", "choose", "select", "better", "role", "target"], 0.78)
    return has_template and wants_advice


def is_theme_question(q: str) -> bool:
    if detect_theme_request(q):
        return True
    return fuzzy_any(q, ["theme", "mode", "appearance", "color"], 0.78) and fuzzy_any(
        q, ["light", "lite", "lighth", "dark", "drak", "darkh", "change", "switch", "make", "set"], 0.75
    )


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
    if app_guide_response(q):
        return True
    if match_skill(q):
        return True
    if extract_learning_subject(q):
        return True
    return fuzzy_any(q, APP_RELATED_KEYWORDS, 0.82)


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


def skill_roadmap_response(skill: str, ctx: dict[str, Any]) -> str:
    tip = SKILL_TIPS.get(skill, f"Start with beginner tutorials and official docs for {skill}.")
    return (
        f"Here's a practical study plan for **{skill.title()}**:\n\n"
        f"1. **Days 1-2:** Learn the basics and key terms. {tip}\n"
        "2. **Days 3-5:** Follow one hands-on tutorial and take notes in your own words.\n"
        "3. **Days 6-10:** Build a small project that uses the skill in a real workflow.\n"
        "4. **Days 11-14:** Add tests, polish the README, and put the project on GitHub.\n\n"
        "After that, add the project to your resume and re-check your SkillGap progress."
    )


def next_step_response(skill: str, ctx: dict[str, Any]) -> str:
    missing = ctx.get("missing") or []
    target_role = ctx.get("target_role") or "your target role"
    next_gap = next((s for s in missing if s.lower() != skill.lower()), "")
    if next_gap:
        return (
            f"After **{skill.title()}**, move to **{next_gap.title()}** because it is still a gap "
            f"for **{target_role}**.\n\n"
            f"Use this order: revise **{skill.title()}** with one project, learn **{next_gap.title()}**, "
            "then update your resume and run the Skill Gap check again."
        )
    return (
        f"After **{skill.title()}**, build one portfolio project, write a clear GitHub README, "
        "and practice explaining the project for interviews."
    )


def awaiting_target_role(ctx: dict[str, Any]) -> bool:
    history = ctx.get("chat_history") or []
    for msg in reversed(history[-4:]):
        if msg.get("role") == "bot":
            return "Which role should I set" in msg.get("text", "")
    return False


def recent_target_role_context(ctx: dict[str, Any]) -> bool:
    history = ctx.get("chat_history") or []
    for msg in reversed(history[-6:]):
        text = msg.get("text", "").lower()
        if "target role" in text or "role should i set" in text:
            return True
    return False


def extract_target_role_from_query(q: str) -> str:
    patterns = [
        r"\b(?:change|chnage|chnaeg|set|update|make|switch)\b.*?\b(?:target role|taget role|role|goal)\b\s+(?:to|as|into)\s+(.+)$",
        r"\b(?:target role|role|goal)\b\s+(?:to|as|into)\s+(.+)$",
        r"\b(?:set|make|change|chnage|chnaeg|update)\s+(?:it|this)\s+(?:to|as|into)\s+(.+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, q)
        if match:
            return clean_role_name(match.group(1))
    return ""


def clean_role_name(role: str) -> str:
    role = re.sub(r"\b(in the app|in app|please|pls|for me|now)\b", "", role).strip()
    role = re.sub(r"[^a-zA-Z\s\-+/]", " ", role)
    role = re.sub(r"\s+", " ", role).strip(" -/")
    if len(role) < 3:
        return ""
    return format_role_name(role)


def supported_roles() -> list[str]:
    try:
        from utils.skill_analyzer import get_roles

        return get_roles()
    except Exception:
        return []


def canonical_supported_role(role: str) -> str:
    for known in supported_roles():
        if known.lower() == role.lower():
            return known
    return role


def suggest_role_correction(role: str) -> str:
    roles = supported_roles()
    if not roles:
        return ""
    role_l = role.lower()
    best = ""
    best_score = 0.0
    for known in roles:
        known_l = known.lower()
        score = SequenceMatcher(None, role_l, known_l).ratio()
        if role_l in known_l or known_l in role_l:
            score = max(score, 0.9)
        if score > best_score:
            best = known
            best_score = score
    return best if best_score >= 0.72 and best.lower() != role_l else ""


def pending_role_confirmation(ctx: dict[str, Any]) -> tuple[str, str]:
    history = ctx.get("chat_history") or []
    pattern = r"Type \*\*yes\*\* to change it to \*\*(.+?)\*\*, or \*\*no\*\* to keep \*\*(.+?)\*\*"
    for msg in reversed(history[-6:]):
        if msg.get("role") != "bot":
            continue
        match = re.search(pattern, msg.get("text", ""))
        if match:
            return match.group(1), match.group(2)
    return "", ""


def save_target_role(role: str, ctx: dict[str, Any]) -> str:
    email = ctx.get("email")
    if not email:
        return "I can guide you, but I could not change the target role because your session email was not available."

    from utils.auth import update_user

    update_user(email, {
        "target_role": role,
        "missing_skills": [],
        "checked_weeks": [],
    })
    ctx["target_role"] = role
    ctx["missing"] = []
    return (
        f"Changed your target role to **{role}** for the whole app.\n\n"
        "I cleared the old gap/roadmap progress because it belonged to the previous role. "
        "Open **Skill Gap** and run the analysis again to get missing skills for this new role."
    )


def target_role_change_response(q: str, ctx: dict[str, Any]) -> str:
    corrected_role, original_role = pending_role_confirmation(ctx)
    if corrected_role and q in ("yes", "y", "yeah", "yep", "correct"):
        return save_target_role(corrected_role, ctx)
    if corrected_role and q in ("no", "n", "nope"):
        return save_target_role(original_role, ctx)

    requested_role = extract_target_role_from_query(q)
    if not requested_role and awaiting_target_role(ctx):
        requested_role = clean_role_name(q)

    current_role = ctx.get("target_role") or ""
    if not requested_role:
        current = f" Your current target role is **{current_role}**." if current_role else ""
        return (
            f"Sure, I can change it for the whole app.{current}\n\n"
            "Which role should I set as your target role? For example: **Data Analyst**, "
            "**Backend Developer**, or **UI UX Designer**."
        )

    requested_role = canonical_supported_role(requested_role)
    correction = suggest_role_correction(requested_role)
    if correction:
        return (
            f"Did you mean **{correction}**?\n\n"
            f"Type **yes** to change it to **{correction}**, or **no** to keep **{requested_role}**."
        )

    return save_target_role(requested_role, ctx)


def theme_change_response(q: str, ctx: dict[str, Any]) -> str:
    requested = detect_theme_request(q)

    current = (ctx.get("theme") or "dark").lower()
    if not requested:
        return (
            f"Your current theme is **{current.title()}**.\n\n"
            "Ask **change to light theme** or **change to dark theme** and I will switch it for you."
        )

    if requested == current:
        return f"The app is already using **{requested.title()}** theme."

    email = ctx.get("email")
    if not email:
        return "I can guide you, but I could not change the theme because your session email was not available."

    from utils.auth import update_user

    update_user(email, {"theme": requested})
    ctx["theme"] = requested
    return f"Changed the app to **{requested.title()}** theme."


def detect_theme_request(q: str) -> str:
    if fuzzy_any(q, ["light", "lighth", "lite", "white", "bright"], 0.72):
        return "light"
    if fuzzy_any(q, ["dark", "darkh", "drak", "black", "night"], 0.72):
        return "dark"
    return ""


def extract_template_role(q: str, ctx: dict[str, Any]) -> str:
    saved_role = (ctx.get("target_role") or "").strip()
    role_patterns = [
        r"\bfor (?:a |an |the )?(.+?)(?: role| profile| resume)?$",
        r"\bas (?:a |an )?(.+?)(?: role| profile)?$",
    ]
    for pattern in role_patterns:
        match = re.search(pattern, q)
        if not match:
            continue
        role = match.group(1).strip()
        role = re.sub(r"\b(in the app|in app|out of four|out of 4|our of four)\b", "", role).strip()
        if role in {"my target", "my target role", "target role", "my role", "role"}:
            return saved_role
        if role and not any(word in role for word in ["template", "templates"]):
            return format_role_name(role)
    return saved_role


def format_role_name(role: str) -> str:
    formatted = role.title()
    replacements = {
        "Ui": "UI",
        "Ux": "UX",
        "Ml": "ML",
        "Ai": "AI",
        "Hr": "HR",
        "Qa": "QA",
    }
    for old, new in replacements.items():
        formatted = re.sub(rf"\b{old}\b", new, formatted)
    return formatted


def correct_common_role_words(role: str) -> str:
    terms = [
        "doctor", "nurse", "medical", "teacher", "professor", "lawyer", "legal",
        "government", "bank", "admin", "marketing", "designer", "developer",
        "engineer", "analyst", "scientist", "frontend", "backend", "data",
        "software", "manager", "accountant", "finance", "research",
    ]
    corrected = []
    for word in role.split():
        replacement = ""
        for term in terms:
            if similar_text(word, term) >= 0.80:
                replacement = term
                break
        corrected.append(replacement or word)
    return format_role_name(" ".join(corrected))


def template_choice_for_role(role: str) -> tuple[str, str]:
    r = role.lower()
    if fuzzy_any(r, ["designer", "ui", "ux", "creative", "graphics", "graphic", "artist", "content", "marketing"], 0.78):
        return "Creative", "that role benefits from a resume that looks more visual and distinctive"
    if fuzzy_any(r, ["data analyst", "analyst", "data scientist", "business analyst", "finance", "accountant", "research"], 0.78):
        return "Minimal", "it keeps data, tools, metrics, and achievements easy to scan"
    if fuzzy_any(r, ["developer", "engineer", "full stack", "frontend", "backend", "devops", "ml engineer", "software", "programmer"], 0.78):
        return "Modern", "it looks professional for tech roles and gives enough structure for skills, projects, and experience"
    if fuzzy_any(r, ["doctor", "nurse", "medical", "teacher", "professor", "lawyer", "legal", "government", "bank", "hr", "admin"], 0.78):
        return "Classic", "it is formal, simple, and safest for conservative or ATS-heavy applications"
    return "Modern", "it is the safest all-round choice when you want a professional resume with a little visual polish"


def template_suggestion_response(q: str, ctx: dict[str, Any]) -> str:
    requested_role = extract_template_role(q, ctx)
    if requested_role:
        requested_role = correct_common_role_words(requested_role)

    if any(word in q for word in ["ats", "traditional", "simple company", "government"]):
        pick = "**Classic** is the best template for that."
        reason = "It is black-and-white, traditional, and the safest option for ATS-heavy applications."
    elif requested_role:
        template, role_reason = template_choice_for_role(requested_role)
        pick = f"For **{requested_role}**, **{template}** is the best template."
        reason = role_reason.capitalize().replace("ats", "ATS") + "."
    elif any(word in q for word in ["creative", "design", "designer", "bold", "stand out"]):
        pick = "**Creative** is the best template for that."
        reason = "It has a bold purple header and stronger visual styling, so it works better for creative or design-leaning roles."
    elif any(word in q for word in ["minimal", "clean", "simple", "elegant"]):
        pick = "**Minimal** is the best template for that."
        reason = "It uses whitespace and light green accents, so it feels clean without looking plain."
    else:
        pick = "**Modern** is the best template."
        reason = "It is the best all-round option in this app: professional, clean, and especially good for tech roles."

    return (
        f"{pick} {reason}\n\n"
        "Quick guide:\n"
        "1. **Modern** — best overall for most students, freshers, developers, and tech roles.\n"
        "2. **Classic** — best when you want maximum ATS safety and a formal look.\n"
        "3. **Minimal** — best for a clean, elegant resume with less visual weight.\n"
        "4. **Creative** — best when you want to stand out, especially for design or creative profiles.\n\n"
        "If you are unsure, use **Modern**."
    )


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

    role_change_followup = extract_target_role_from_query(q) and recent_target_role_context(ctx)
    role_confirmation_reply = pending_role_confirmation(ctx)[0] and q in (
        "yes", "y", "yeah", "yep", "correct", "no", "n", "nope"
    )
    if intent == "change_target_role" or is_target_role_change_question(q) or awaiting_target_role(ctx) or role_change_followup or role_confirmation_reply:
        return target_role_change_response(q, ctx)

    if intent == "theme_change" or is_theme_question(q):
        return theme_change_response(q, ctx)

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

    if intent == "template_suggestion" or is_template_question(q):
        return template_suggestion_response(q, ctx)

    guide = app_guide_response(q)
    if guide and is_app_navigation_question(q):
        return guide

    if intent == "my_skills":
        if not user_skills:
            return "No skills detected yet. Upload your resume on **Resume Score** first."
        return f"You have **{len(user_skills)} skills** from your resume:\n\n" + \
               "\n".join(f"• {s.title()}" for s in user_skills)

    if intent == "missing_skills":
        if not target_role:
            return "Select a target role on **Skill Gap** first."
        if not ctx.get("gap_analyzed"):
            return "Run **Skill Gap** first so I can compare your skills with the target role."
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
        if not ctx.get("gap_analyzed"):
            return (
                f"Target role: **{target_role}**. Readiness is not calculated yet. "
                "Open **Skill Gap** and run the analysis."
            )
        pct = calculate_readiness(user_skills, missing, True, ctx.get("gap_result", {}))
        matched_count = len((ctx.get("gap_result") or {}).get("matched_skills") or user_skills)
        return (
            f"Target role: **{target_role}** — **{pct}%** skill match "
            f"({matched_count} matched, {len(missing)} missing)."
        )

    if intent == "roadmap":
        if skill:
            return skill_roadmap_response(skill, ctx)
        if not target_role:
            return "Set a target role on **Skill Gap**, then open **Roadmap**."
        if not ctx.get("gap_analyzed"):
            return "Run **Skill Gap** first, then I can build a roadmap from the missing skills."
        if not missing:
            return f"You're well covered for **{target_role}**. Use **Roadmap** for advanced topics."
        top = missing[:3]
        lines = "\n\n".join(
            f"**{s.title()}** — {SKILL_TIPS.get(s.lower(), 'Find a beginner tutorial on YouTube.')}"
            for s in top
        )
        extra = f"\n\n+{len(missing) - 3} more on **Roadmap**." if len(missing) > 3 else ""
        return f"Top priorities for **{target_role}**:\n\n{lines}{extra}"

    learn_subject = extract_learning_subject(q)
    if learn_subject:
        sk = match_skill(learn_subject) or learn_subject
        return skill_response(sk.lower(), ctx)

    if intent == "what_next":
        if skill:
            return next_step_response(skill, ctx)
        return generic_app_response(q, ctx)

    if skill:
        return skill_response(skill, ctx)

    guide = app_guide_response(q)
    if guide:
        return guide

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
