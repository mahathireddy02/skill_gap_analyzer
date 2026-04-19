"""
roadmap_generator.py
Generates personalized, week-wise learning roadmaps based on:
- Target role, skill level, time availability, deadline,
  learning style, budget, and missing skills.
"""

import math

# ── Skill Learning Database ───────────────────────────────────────────────────
# Each skill has: hours_to_learn (beginner baseline), phases, resources
SKILL_DB = {
    "python": {
        "hours": 40,
        "phases": {
            "beginner":     "Variables, data types, loops, functions, lists, dicts",
            "intermediate": "OOP, file I/O, error handling, modules, virtual envs",
            "advanced":     "Decorators, generators, async/await, packaging, testing",
        },
        "resources": {
            "free":  ["Python.org tutorial", "freeCodeCamp Python (YouTube)", "Automate the Boring Stuff (book)"],
            "paid":  ["100 Days of Code – Python (Udemy)", "Python Bootcamp – Jose Portilla (Udemy)"],
            "docs":  ["https://docs.python.org/3/tutorial/"],
        },
        "project": "Build a CLI task manager or web scraper",
    },
    "machine learning": {
        "hours": 80,
        "phases": {
            "beginner":     "Supervised vs unsupervised learning, linear/logistic regression, train-test split",
            "intermediate": "Decision trees, random forests, SVM, cross-validation, feature engineering",
            "advanced":     "Ensemble methods, hyperparameter tuning, model deployment, MLOps basics",
        },
        "resources": {
            "free":  ["Andrew Ng ML Course (Coursera – audit)", "StatQuest (YouTube)", "Kaggle Learn"],
            "paid":  ["ML A-Z (Udemy)", "Fast.ai Practical ML"],
            "docs":  ["https://scikit-learn.org/stable/user_guide.html"],
        },
        "project": "Build a house price predictor or spam classifier",
    },
    "deep learning": {
        "hours": 80,
        "phases": {
            "beginner":     "Neural networks, activation functions, backpropagation, gradient descent",
            "intermediate": "CNNs for images, RNNs/LSTMs for sequences, Keras/TensorFlow basics",
            "advanced":     "Transformers, attention mechanism, GANs, model optimization & deployment",
        },
        "resources": {
            "free":  ["3Blue1Brown Neural Networks (YouTube)", "Deep Learning Specialization (Coursera – audit)", "fast.ai"],
            "paid":  ["Deep Learning A-Z (Udemy)", "TensorFlow Developer Certificate prep"],
            "docs":  ["https://www.tensorflow.org/tutorials", "https://pytorch.org/tutorials/"],
        },
        "project": "Build an image classifier or sentiment analysis model",
    },
    "javascript": {
        "hours": 50,
        "phases": {
            "beginner":     "Variables, functions, DOM manipulation, events, ES6 basics",
            "intermediate": "Async/await, fetch API, modules, closures, prototypes",
            "advanced":     "Design patterns, performance optimization, TypeScript migration",
        },
        "resources": {
            "free":  ["javascript.info", "freeCodeCamp JS (YouTube)", "MDN Web Docs"],
            "paid":  ["The Complete JavaScript Course – Jonas (Udemy)", "JavaScript: The Hard Parts (Frontend Masters)"],
            "docs":  ["https://developer.mozilla.org/en-US/docs/Web/JavaScript"],
        },
        "project": "Build a weather app or quiz game with API integration",
    },
    "react": {
        "hours": 50,
        "phases": {
            "beginner":     "Components, JSX, props, state, event handling",
            "intermediate": "Hooks (useState, useEffect, useContext), React Router, forms",
            "advanced":     "Redux/Zustand, performance (memo, lazy), testing with Jest",
        },
        "resources": {
            "free":  ["Official React Docs (react.dev)", "Traversy Media React (YouTube)", "freeCodeCamp React"],
            "paid":  ["React – The Complete Guide (Udemy)", "Epic React (Kent C. Dodds)"],
            "docs":  ["https://react.dev/learn"],
        },
        "project": "Build a task manager or e-commerce product listing app",
    },
    "sql": {
        "hours": 30,
        "phases": {
            "beginner":     "SELECT, WHERE, ORDER BY, INSERT, UPDATE, DELETE, JOINs",
            "intermediate": "Aggregations, GROUP BY, subqueries, window functions, indexes",
            "advanced":     "Query optimization, stored procedures, transactions, normalization",
        },
        "resources": {
            "free":  ["SQLZoo", "Mode Analytics SQL Tutorial", "W3Schools SQL"],
            "paid":  ["The Complete SQL Bootcamp (Udemy)", "SQL for Data Analysis (Udacity)"],
            "docs":  ["https://www.postgresql.org/docs/current/tutorial.html"],
        },
        "project": "Analyze a public dataset (e.g., Netflix, COVID) with SQL queries",
    },
    "docker": {
        "hours": 25,
        "phases": {
            "beginner":     "Containers vs VMs, Docker CLI, Dockerfile, images, containers",
            "intermediate": "Docker Compose, volumes, networking, multi-container apps",
            "advanced":     "Multi-stage builds, Docker Swarm, security scanning, CI/CD integration",
        },
        "resources": {
            "free":  ["Play with Docker (labs.play-with-docker.com)", "TechWorld with Nana Docker (YouTube)", "Docker Docs"],
            "paid":  ["Docker & Kubernetes (Udemy – Bret Fisher)", "Docker Mastery (Udemy)"],
            "docs":  ["https://docs.docker.com/get-started/"],
        },
        "project": "Containerize a Python Flask/FastAPI app with Docker Compose",
    },
    "kubernetes": {
        "hours": 40,
        "phases": {
            "beginner":     "Pods, deployments, services, kubectl basics, Minikube setup",
            "intermediate": "ConfigMaps, secrets, ingress, namespaces, persistent volumes",
            "advanced":     "Helm charts, RBAC, HPA, cluster monitoring, production hardening",
        },
        "resources": {
            "free":  ["Kubernetes.io tutorials", "TechWorld with Nana K8s (YouTube)", "KodeKloud free labs"],
            "paid":  ["CKA Certification prep (Udemy)", "Kubernetes Mastery (Udemy)"],
            "docs":  ["https://kubernetes.io/docs/tutorials/"],
        },
        "project": "Deploy a microservices app on a local Kubernetes cluster",
    },
    "aws": {
        "hours": 60,
        "phases": {
            "beginner":     "IAM, EC2, S3, VPC basics, AWS Free Tier setup",
            "intermediate": "Lambda, RDS, CloudFormation, ECS, Route53, CloudWatch",
            "advanced":     "Well-Architected Framework, cost optimization, security, certifications",
        },
        "resources": {
            "free":  ["AWS Free Tier (aws.amazon.com)", "freeCodeCamp AWS (YouTube)", "AWS Skill Builder"],
            "paid":  ["AWS Certified Solutions Architect (Udemy – Stephane Maarek)", "A Cloud Guru"],
            "docs":  ["https://docs.aws.amazon.com/"],
        },
        "project": "Deploy a serverless REST API with Lambda + API Gateway + DynamoDB",
    },
    "git": {
        "hours": 15,
        "phases": {
            "beginner":     "init, add, commit, push, pull, clone, status",
            "intermediate": "Branching, merging, rebasing, pull requests, resolving conflicts",
            "advanced":     "Git hooks, workflows (GitFlow), CI/CD integration, monorepo strategies",
        },
        "resources": {
            "free":  ["GitHub Hello World guide", "Atlassian Git tutorials", "Learn Git Branching (interactive)"],
            "paid":  ["Git & GitHub Bootcamp (Udemy)"],
            "docs":  ["https://git-scm.com/doc"],
        },
        "project": "Contribute to an open-source project on GitHub",
    },
    "typescript": {
        "hours": 25,
        "phases": {
            "beginner":     "Types, interfaces, enums, type inference, tsconfig basics",
            "intermediate": "Generics, utility types, decorators, strict mode",
            "advanced":     "Advanced generics, conditional types, module augmentation",
        },
        "resources": {
            "free":  ["TypeScript Handbook (typescriptlang.org)", "Matt Pocock TS tutorials (YouTube)"],
            "paid":  ["Understanding TypeScript (Udemy)", "Total TypeScript (Matt Pocock)"],
            "docs":  ["https://www.typescriptlang.org/docs/"],
        },
        "project": "Rewrite a JavaScript project in TypeScript",
    },
    "pandas": {
        "hours": 20,
        "phases": {
            "beginner":     "DataFrames, Series, read_csv, basic operations, filtering",
            "intermediate": "GroupBy, merge/join, pivot tables, handling missing data",
            "advanced":     "Performance optimization, method chaining, custom aggregations",
        },
        "resources": {
            "free":  ["Kaggle Pandas course", "Corey Schafer Pandas (YouTube)", "Pandas docs"],
            "paid":  ["Data Analysis with Pandas (Udemy)"],
            "docs":  ["https://pandas.pydata.org/docs/user_guide/"],
        },
        "project": "Analyze and visualize a real-world dataset (Kaggle)",
    },
    "tensorflow": {
        "hours": 50,
        "phases": {
            "beginner":     "Tensors, Keras Sequential API, training a simple neural network",
            "intermediate": "Custom layers, callbacks, data pipelines with tf.data",
            "advanced":     "Custom training loops, TF Serving, TFLite, distributed training",
        },
        "resources": {
            "free":  ["TensorFlow official tutorials", "DeepLearning.AI TF Developer (Coursera – audit)"],
            "paid":  ["TensorFlow Developer Certificate prep (Udemy)", "Hands-On ML (book)"],
            "docs":  ["https://www.tensorflow.org/tutorials"],
        },
        "project": "Build and deploy an image classification model",
    },
    "pytorch": {
        "hours": 50,
        "phases": {
            "beginner":     "Tensors, autograd, simple neural network with nn.Module",
            "intermediate": "CNNs, RNNs, DataLoader, training loops, GPU usage",
            "advanced":     "Custom loss functions, model optimization, ONNX export, deployment",
        },
        "resources": {
            "free":  ["PyTorch official tutorials", "fast.ai Practical DL", "Andrej Karpathy (YouTube)"],
            "paid":  ["PyTorch for Deep Learning (Udemy)", "Zero to Mastery PyTorch"],
            "docs":  ["https://pytorch.org/tutorials/"],
        },
        "project": "Build a text classifier or object detection model",
    },
    "flutter": {
        "hours": 50,
        "phases": {
            "beginner":     "Dart basics, widgets (Stateless/Stateful), layouts, navigation",
            "intermediate": "State management (Provider/Riverpod/Bloc), REST API integration",
            "advanced":     "Custom animations, platform channels, CI/CD, app store deployment",
        },
        "resources": {
            "free":  ["Flutter official docs", "Vandad Nahavandipoor (YouTube)", "freeCodeCamp Flutter"],
            "paid":  ["Flutter & Dart – The Complete Guide (Udemy)", "Flutter Apprentice (book)"],
            "docs":  ["https://docs.flutter.dev/"],
        },
        "project": "Build a cross-platform todo or weather app",
    },
    "postgresql": {
        "hours": 25,
        "phases": {
            "beginner":     "Setup, psql CLI, basic CRUD, data types",
            "intermediate": "Indexes, foreign keys, transactions, views, functions",
            "advanced":     "Query optimization, EXPLAIN ANALYZE, partitioning, replication",
        },
        "resources": {
            "free":  ["PostgreSQL official tutorial", "Hussein Nasser DB (YouTube)"],
            "paid":  ["SQL and PostgreSQL (Udemy – Stephen Grider)"],
            "docs":  ["https://www.postgresql.org/docs/"],
        },
        "project": "Design and query a relational database for a real app",
    },
    "node": {
        "hours": 40,
        "phases": {
            "beginner":     "Node.js basics, npm, modules, file system, HTTP module",
            "intermediate": "Express.js, middleware, routing, REST APIs, authentication",
            "advanced":     "Streams, clustering, performance, microservices, WebSockets",
        },
        "resources": {
            "free":  ["Node.js official docs", "Traversy Media Node (YouTube)", "The Odin Project"],
            "paid":  ["Node.js – The Complete Guide (Udemy)", "Node.js Design Patterns (book)"],
            "docs":  ["https://nodejs.org/en/docs/"],
        },
        "project": "Build a REST API with Express + JWT authentication",
    },
    "terraform": {
        "hours": 30,
        "phases": {
            "beginner":     "HCL syntax, providers, resources, state files, plan/apply",
            "intermediate": "Modules, variables, outputs, remote state, workspaces",
            "advanced":     "Custom providers, Terragrunt, policy as code, CI/CD integration",
        },
        "resources": {
            "free":  ["HashiCorp Learn (developer.hashicorp.com)", "TechWorld with Nana Terraform (YouTube)"],
            "paid":  ["Terraform on AWS (Udemy)", "HashiCorp Terraform Associate cert prep"],
            "docs":  ["https://developer.hashicorp.com/terraform/docs"],
        },
        "project": "Provision a full AWS VPC + EC2 + RDS with Terraform",
    },
    "power bi": {
        "hours": 25,
        "phases": {
            "beginner":     "Connecting data sources, basic visuals, filters, slicers",
            "intermediate": "DAX formulas, calculated columns, measures, relationships",
            "advanced":     "Row-level security, performance optimization, embedding, Power BI Service",
        },
        "resources": {
            "free":  ["Microsoft Learn Power BI", "Guy in a Cube (YouTube)", "SQLBI"],
            "paid":  ["Microsoft Power BI Desktop (Udemy)", "Power BI A-Z (Udemy)"],
            "docs":  ["https://learn.microsoft.com/en-us/power-bi/"],
        },
        "project": "Build a sales analytics dashboard from a CSV dataset",
    },
    "kotlin": {
        "hours": 40,
        "phases": {
            "beginner":     "Kotlin syntax, null safety, data classes, collections",
            "intermediate": "Coroutines, Android basics, Jetpack components, MVVM",
            "advanced":     "Jetpack Compose, Hilt DI, Flow, testing, app architecture",
        },
        "resources": {
            "free":  ["Kotlin official docs", "Philipp Lackner Android (YouTube)", "Google Codelabs"],
            "paid":  ["Android Kotlin Development (Udemy)", "Kotlin Bootcamp (Udacity)"],
            "docs":  ["https://kotlinlang.org/docs/home.html"],
        },
        "project": "Build a notes or weather Android app with MVVM",
    },
    "ci/cd": {
        "hours": 20,
        "phases": {
            "beginner":     "CI/CD concepts, GitHub Actions basics, automated testing",
            "intermediate": "Multi-stage pipelines, Docker integration, deployment automation",
            "advanced":     "GitOps, ArgoCD, advanced workflows, secrets management",
        },
        "resources": {
            "free":  ["GitHub Actions docs", "TechWorld with Nana CI/CD (YouTube)", "GitLab CI docs"],
            "paid":  ["GitHub Actions – The Complete Guide (Udemy)"],
            "docs":  ["https://docs.github.com/en/actions"],
        },
        "project": "Set up a full CI/CD pipeline for a web app on GitHub Actions",
    },
}

# Default for skills not in DB
DEFAULT_SKILL = {
    "hours": 30,
    "phases": {
        "beginner":     "Learn fundamentals through official documentation and beginner tutorials",
        "intermediate": "Build small projects and follow structured courses on Udemy/Coursera",
        "advanced":     "Contribute to open source, build portfolio projects, get certified",
    },
    "resources": {
        "free":  ["Official documentation", "YouTube tutorials", "freeCodeCamp"],
        "paid":  ["Udemy courses (search skill name)", "Coursera specializations"],
        "docs":  ["Search 'skill_name official docs'"],
    },
    "project": "Build a small project applying this skill end-to-end",
}

# Learning style → resource type preference
STYLE_RESOURCE_MAP = {
    "videos":   "free",   # YouTube-heavy
    "projects": "free",   # project-based
    "docs":     "docs",   # documentation-first
    "courses":  "paid",   # structured paid courses
    "mixed":    "free",   # balanced
}


# ── Timeline Calculator ───────────────────────────────────────────────────────

def calculate_timeline(
    missing_skills: list[str],
    hours_per_week: float,
    skill_level: str,
) -> dict:
    """
    Calculate realistic week-by-week timeline for learning missing skills.
    Adjusts hours based on current skill level.
    """
    level_multiplier = {"beginner": 1.0, "intermediate": 0.7, "advanced": 0.5}
    multiplier = level_multiplier.get(skill_level.lower(), 1.0)

    total_hours = sum(
        SKILL_DB.get(s.lower(), DEFAULT_SKILL)["hours"] * multiplier
        for s in missing_skills
    )
    total_weeks = math.ceil(total_hours / hours_per_week) if hours_per_week > 0 else 0

    return {
        "total_hours":  round(total_hours),
        "total_weeks":  total_weeks,
        "total_months": round(total_weeks / 4.3, 1),
        "hours_per_week": hours_per_week,
    }


# ── Phase Selector ────────────────────────────────────────────────────────────

def get_starting_phase(skill_level: str) -> list[str]:
    """Return which phases to include based on current level."""
    level = skill_level.lower()
    if level == "beginner":
        return ["beginner", "intermediate", "advanced"]
    elif level == "intermediate":
        return ["intermediate", "advanced"]
    else:
        return ["advanced"]


# ── Roadmap Generator ─────────────────────────────────────────────────────────

def generate_roadmap(
    role: str,
    missing_skills: list[str],
    skill_level: str       = "beginner",
    hours_per_week: float  = 10.0,
    deadline_months: int   = 3,
    learning_style: str    = "mixed",
    budget: str            = "free",
    interests: str         = "",
) -> dict:
    """
    Generate a complete personalized roadmap.

    Returns:
    {
        role, summary, timeline,
        phases: [ { phase_num, title, weeks, skills: [...] } ],
        weekly_plan: [ { week, focus, tasks, hours } ],
        tips
    }
    """
    if not missing_skills:
        return {
            "role": role,
            "summary": "🎉 You already have all required skills for this role!",
            "phases": [],
            "weekly_plan": [],
            "timeline": {},
            "tips": [],
        }

    # Normalize
    skill_level    = skill_level.lower()
    budget         = budget.lower()
    learning_style = learning_style.lower()
    resource_key   = STYLE_RESOURCE_MAP.get(learning_style, "free")
    if budget == "paid":
        resource_key = "paid"
    elif budget == "free":
        resource_key = "free" if resource_key != "docs" else "docs"

    phases_to_include = get_starting_phase(skill_level)
    timeline = calculate_timeline(missing_skills, hours_per_week, skill_level)

    # Warn if deadline is too tight
    deadline_weeks = deadline_months * 4.3
    is_tight = timeline["total_weeks"] > deadline_weeks
    tight_warning = (
        f"⚠️ Your deadline ({deadline_months} months) may be tight. "
        f"Estimated time needed: {timeline['total_months']} months. "
        f"Consider increasing study hours or reducing scope."
    ) if is_tight else ""

    # Build per-skill entries
    skill_entries = []
    level_multiplier = {"beginner": 1.0, "intermediate": 0.7, "advanced": 0.5}
    multiplier = level_multiplier.get(skill_level, 1.0)

    for skill in missing_skills:
        skill_lower = skill.lower()
        db_entry = SKILL_DB.get(skill_lower, DEFAULT_SKILL)
        adjusted_hours = round(db_entry["hours"] * multiplier)
        weeks_needed   = math.ceil(adjusted_hours / hours_per_week) if hours_per_week > 0 else 1

        # Pick resources based on style/budget
        resources = db_entry["resources"].get(resource_key, db_entry["resources"]["free"])
        # Always include docs if style is docs
        if learning_style == "docs":
            resources = db_entry["resources"].get("docs", resources)

        phases_content = {
            phase: db_entry["phases"].get(phase, "")
            for phase in phases_to_include
            if db_entry["phases"].get(phase)
        }

        skill_entries.append({
            "skill":         skill,
            "hours_needed":  adjusted_hours,
            "weeks_needed":  weeks_needed,
            "phases":        phases_content,
            "resources":     resources,
            "project":       db_entry.get("project", "Build a small project using this skill"),
        })

    # Build phase-wise plan (group skills into phases)
    phase_plan = []
    week_cursor = 1

    for i, entry in enumerate(skill_entries):
        phase_plan.append({
            "phase_num":   i + 1,
            "skill":       entry["skill"],
            "start_week":  week_cursor,
            "end_week":    week_cursor + entry["weeks_needed"] - 1,
            "hours":       entry["hours_needed"],
            "phases":      entry["phases"],
            "resources":   entry["resources"],
            "project":     entry["project"],
        })
        week_cursor += entry["weeks_needed"]

    # Build weekly plan (first 12 weeks detailed, rest summarized)
    weekly_plan = []
    for phase in phase_plan:
        for week in range(phase["start_week"], phase["end_week"] + 1):
            if week > 52:
                break
            week_in_skill = week - phase["start_week"] + 1
            total_skill_weeks = phase["end_week"] - phase["start_week"] + 1

            # Determine which phase content to show this week
            phase_keys = list(phase["phases"].keys())
            phase_idx  = min(
                int((week_in_skill - 1) / total_skill_weeks * len(phase_keys)),
                len(phase_keys) - 1
            )
            current_phase_key = phase_keys[phase_idx] if phase_keys else "beginner"
            phase_content = phase["phases"].get(current_phase_key, "Continue learning")

            weekly_plan.append({
                "week":    week,
                "skill":   phase["skill"],
                "focus":   f"{current_phase_key.title()} - {phase['skill'].title()}",
                "tasks":   phase_content,
                "hours":   hours_per_week,
                "project": phase["project"] if week == phase["end_week"] else "",
            })

    # Personalized tips
    tips = [
        f"📅 Study {hours_per_week} hours/week consistently — daily practice beats weekend cramming.",
        f"🎯 Focus on one skill at a time. Complete each phase before moving on.",
        f"🛠️ Build the mini-project at the end of each skill — it cements your learning.",
        f"📊 Track your progress weekly and adjust your plan if needed.",
    ]
    if interests:
        tips.append(f"💡 Since you're interested in {interests}, look for projects that combine it with {role} skills.")
    if is_tight:
        tips.append(tight_warning)
    if budget == "free":
        tips.append("💰 All recommended resources are free. Kaggle, freeCodeCamp, and YouTube are your best friends.")
    if learning_style == "projects":
        tips.append("🔨 Project-based learner? Skip theory-heavy sections and jump straight to building.")

    return {
        "role":        role,
        "skill_level": skill_level,
        "summary": (
            f"Personalized roadmap for **{role}** | "
            f"Level: {skill_level.title()} | "
            f"{len(missing_skills)} skills to learn | "
            f"~{timeline['total_months']} months at {hours_per_week}h/week"
        ),
        "timeline":    timeline,
        "phase_plan":  phase_plan,
        "weekly_plan": weekly_plan,
        "tips":        tips,
        "tight_deadline": is_tight,
    }
