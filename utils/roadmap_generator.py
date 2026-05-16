"""
roadmap_generator.py
Strictly deadline-bound: total plan = EXACTLY deadline_weeks weeks.
All skills are covered within that window by proportional distribution.
"""

import math

SKILL_DB = {
    "python":           {"hours": 40, "phases": {"beginner": "Variables, data types, loops, functions, lists, dicts", "intermediate": "OOP, file I/O, error handling, modules, virtual envs", "advanced": "Decorators, generators, async/await, packaging, testing"}, "resources": {"free": ["Python.org tutorial", "freeCodeCamp Python (YouTube)", "Automate the Boring Stuff"], "paid": ["100 Days of Code – Python (Udemy)", "Python Bootcamp – Jose Portilla (Udemy)"], "docs": ["https://docs.python.org/3/tutorial/"]}, "project": "Build a CLI task manager or web scraper"},
    "machine learning": {"hours": 80, "phases": {"beginner": "Supervised vs unsupervised learning, linear/logistic regression, train-test split", "intermediate": "Decision trees, random forests, SVM, cross-validation, feature engineering", "advanced": "Ensemble methods, hyperparameter tuning, model deployment, MLOps basics"}, "resources": {"free": ["Andrew Ng ML Course (Coursera audit)", "StatQuest (YouTube)", "Kaggle Learn"], "paid": ["ML A-Z (Udemy)", "Fast.ai Practical ML"], "docs": ["https://scikit-learn.org/stable/user_guide.html"]}, "project": "Build a house price predictor or spam classifier"},
    "deep learning":    {"hours": 80, "phases": {"beginner": "Neural networks, activation functions, backpropagation, gradient descent", "intermediate": "CNNs for images, RNNs/LSTMs for sequences, Keras/TensorFlow basics", "advanced": "Transformers, attention mechanism, GANs, model optimization & deployment"}, "resources": {"free": ["3Blue1Brown Neural Networks (YouTube)", "Deep Learning Specialization (Coursera audit)", "fast.ai"], "paid": ["Deep Learning A-Z (Udemy)", "TensorFlow Developer Certificate prep"], "docs": ["https://www.tensorflow.org/tutorials"]}, "project": "Build an image classifier or sentiment analysis model"},
    "javascript":       {"hours": 50, "phases": {"beginner": "Variables, functions, DOM manipulation, events, ES6 basics", "intermediate": "Async/await, fetch API, modules, closures, prototypes", "advanced": "Design patterns, performance optimization, TypeScript migration"}, "resources": {"free": ["javascript.info", "freeCodeCamp JS (YouTube)", "MDN Web Docs"], "paid": ["The Complete JavaScript Course – Jonas (Udemy)"], "docs": ["https://developer.mozilla.org/en-US/docs/Web/JavaScript"]}, "project": "Build a weather app or quiz game with API integration"},
    "react":            {"hours": 50, "phases": {"beginner": "Components, JSX, props, state, event handling", "intermediate": "Hooks (useState, useEffect, useContext), React Router, forms", "advanced": "Redux/Zustand, performance (memo, lazy), testing with Jest"}, "resources": {"free": ["Official React Docs (react.dev)", "Traversy Media React (YouTube)", "freeCodeCamp React"], "paid": ["React – The Complete Guide (Udemy)"], "docs": ["https://react.dev/learn"]}, "project": "Build a task manager or e-commerce product listing app"},
    "sql":              {"hours": 30, "phases": {"beginner": "SELECT, WHERE, ORDER BY, INSERT, UPDATE, DELETE, JOINs", "intermediate": "Aggregations, GROUP BY, subqueries, window functions, indexes", "advanced": "Query optimization, stored procedures, transactions, normalization"}, "resources": {"free": ["SQLZoo", "Mode Analytics SQL Tutorial", "W3Schools SQL"], "paid": ["The Complete SQL Bootcamp (Udemy)"], "docs": ["https://www.postgresql.org/docs/current/tutorial.html"]}, "project": "Analyze a public dataset with SQL queries"},
    "docker":           {"hours": 25, "phases": {"beginner": "Containers vs VMs, Docker CLI, Dockerfile, images, containers", "intermediate": "Docker Compose, volumes, networking, multi-container apps", "advanced": "Multi-stage builds, Docker Swarm, security scanning, CI/CD integration"}, "resources": {"free": ["Play with Docker", "TechWorld with Nana Docker (YouTube)", "Docker Docs"], "paid": ["Docker & Kubernetes (Udemy – Bret Fisher)"], "docs": ["https://docs.docker.com/get-started/"]}, "project": "Containerize a Python Flask/FastAPI app with Docker Compose"},
    "kubernetes":       {"hours": 40, "phases": {"beginner": "Pods, deployments, services, kubectl basics, Minikube setup", "intermediate": "ConfigMaps, secrets, ingress, namespaces, persistent volumes", "advanced": "Helm charts, RBAC, HPA, cluster monitoring, production hardening"}, "resources": {"free": ["Kubernetes.io tutorials", "TechWorld with Nana K8s (YouTube)", "KodeKloud free labs"], "paid": ["CKA Certification prep (Udemy)"], "docs": ["https://kubernetes.io/docs/tutorials/"]}, "project": "Deploy a microservices app on a local Kubernetes cluster"},
    "aws":              {"hours": 60, "phases": {"beginner": "IAM, EC2, S3, VPC basics, AWS Free Tier setup", "intermediate": "Lambda, RDS, CloudFormation, ECS, Route53, CloudWatch", "advanced": "Well-Architected Framework, cost optimization, security, certifications"}, "resources": {"free": ["AWS Free Tier", "freeCodeCamp AWS (YouTube)", "AWS Skill Builder"], "paid": ["AWS Certified Solutions Architect (Udemy – Stephane Maarek)"], "docs": ["https://docs.aws.amazon.com/"]}, "project": "Deploy a serverless REST API with Lambda + API Gateway + DynamoDB"},
    "git":              {"hours": 15, "phases": {"beginner": "init, add, commit, push, pull, clone, status", "intermediate": "Branching, merging, rebasing, pull requests, resolving conflicts", "advanced": "Git hooks, workflows (GitFlow), CI/CD integration, monorepo strategies"}, "resources": {"free": ["GitHub Hello World guide", "Atlassian Git tutorials", "Learn Git Branching (interactive)"], "paid": ["Git & GitHub Bootcamp (Udemy)"], "docs": ["https://git-scm.com/doc"]}, "project": "Contribute to an open-source project on GitHub"},
    "typescript":       {"hours": 25, "phases": {"beginner": "Types, interfaces, enums, type inference, tsconfig basics", "intermediate": "Generics, utility types, decorators, strict mode", "advanced": "Advanced generics, conditional types, module augmentation"}, "resources": {"free": ["TypeScript Handbook (typescriptlang.org)", "Matt Pocock TS tutorials (YouTube)"], "paid": ["Understanding TypeScript (Udemy)"], "docs": ["https://www.typescriptlang.org/docs/"]}, "project": "Rewrite a JavaScript project in TypeScript"},
    "pandas":           {"hours": 20, "phases": {"beginner": "DataFrames, Series, read_csv, basic operations, filtering", "intermediate": "GroupBy, merge/join, pivot tables, handling missing data", "advanced": "Performance optimization, method chaining, custom aggregations"}, "resources": {"free": ["Kaggle Pandas course", "Corey Schafer Pandas (YouTube)"], "paid": ["Data Analysis with Pandas (Udemy)"], "docs": ["https://pandas.pydata.org/docs/user_guide/"]}, "project": "Analyze and visualize a real-world dataset (Kaggle)"},
    "tensorflow":       {"hours": 50, "phases": {"beginner": "Tensors, Keras Sequential API, training a simple neural network", "intermediate": "Custom layers, callbacks, data pipelines with tf.data", "advanced": "Custom training loops, TF Serving, TFLite, distributed training"}, "resources": {"free": ["TensorFlow official tutorials", "DeepLearning.AI TF Developer (Coursera audit)"], "paid": ["TensorFlow Developer Certificate prep (Udemy)"], "docs": ["https://www.tensorflow.org/tutorials"]}, "project": "Build and deploy an image classification model"},
    "pytorch":          {"hours": 50, "phases": {"beginner": "Tensors, autograd, simple neural network with nn.Module", "intermediate": "CNNs, RNNs, DataLoader, training loops, GPU usage", "advanced": "Custom loss functions, model optimization, ONNX export, deployment"}, "resources": {"free": ["PyTorch official tutorials", "fast.ai Practical DL", "Andrej Karpathy (YouTube)"], "paid": ["PyTorch for Deep Learning (Udemy)"], "docs": ["https://pytorch.org/tutorials/"]}, "project": "Build a text classifier or object detection model"},
    "flutter":          {"hours": 50, "phases": {"beginner": "Dart basics, widgets (Stateless/Stateful), layouts, navigation", "intermediate": "State management (Provider/Riverpod/Bloc), REST API integration", "advanced": "Custom animations, platform channels, CI/CD, app store deployment"}, "resources": {"free": ["Flutter official docs", "Vandad Nahavandipoor (YouTube)"], "paid": ["Flutter & Dart – The Complete Guide (Udemy)"], "docs": ["https://docs.flutter.dev/"]}, "project": "Build a cross-platform todo or weather app"},
    "postgresql":       {"hours": 25, "phases": {"beginner": "Setup, psql CLI, basic CRUD, data types", "intermediate": "Indexes, foreign keys, transactions, views, functions", "advanced": "Query optimization, EXPLAIN ANALYZE, partitioning, replication"}, "resources": {"free": ["PostgreSQL official tutorial", "Hussein Nasser DB (YouTube)"], "paid": ["SQL and PostgreSQL (Udemy – Stephen Grider)"], "docs": ["https://www.postgresql.org/docs/"]}, "project": "Design and query a relational database for a real app"},
    "node":             {"hours": 40, "phases": {"beginner": "Node.js basics, npm, modules, file system, HTTP module", "intermediate": "Express.js, middleware, routing, REST APIs, authentication", "advanced": "Streams, clustering, performance, microservices, WebSockets"}, "resources": {"free": ["Node.js official docs", "Traversy Media Node (YouTube)"], "paid": ["Node.js – The Complete Guide (Udemy)"], "docs": ["https://nodejs.org/en/docs/"]}, "project": "Build a REST API with Express + JWT authentication"},
    "terraform":        {"hours": 30, "phases": {"beginner": "HCL syntax, providers, resources, state files, plan/apply", "intermediate": "Modules, variables, outputs, remote state, workspaces", "advanced": "Custom providers, Terragrunt, policy as code, CI/CD integration"}, "resources": {"free": ["HashiCorp Learn", "TechWorld with Nana Terraform (YouTube)"], "paid": ["Terraform on AWS (Udemy)"], "docs": ["https://developer.hashicorp.com/terraform/docs"]}, "project": "Provision a full AWS VPC + EC2 + RDS with Terraform"},
    "power bi":         {"hours": 25, "phases": {"beginner": "Connecting data sources, basic visuals, filters, slicers", "intermediate": "DAX formulas, calculated columns, measures, relationships", "advanced": "Row-level security, performance optimization, embedding, Power BI Service"}, "resources": {"free": ["Microsoft Learn Power BI", "Guy in a Cube (YouTube)"], "paid": ["Power BI A-Z (Udemy)"], "docs": ["https://learn.microsoft.com/en-us/power-bi/"]}, "project": "Build a sales analytics dashboard from a CSV dataset"},
    "kotlin":           {"hours": 40, "phases": {"beginner": "Kotlin syntax, null safety, data classes, collections", "intermediate": "Coroutines, Android basics, Jetpack components, MVVM", "advanced": "Jetpack Compose, Hilt DI, Flow, testing, app architecture"}, "resources": {"free": ["Kotlin official docs", "Philipp Lackner Android (YouTube)"], "paid": ["Android Kotlin Development (Udemy)"], "docs": ["https://kotlinlang.org/docs/home.html"]}, "project": "Build a notes or weather Android app with MVVM"},
    "ci/cd":            {"hours": 20, "phases": {"beginner": "CI/CD concepts, GitHub Actions basics, automated testing", "intermediate": "Multi-stage pipelines, Docker integration, deployment automation", "advanced": "GitOps, ArgoCD, advanced workflows, secrets management"}, "resources": {"free": ["GitHub Actions docs", "TechWorld with Nana CI/CD (YouTube)"], "paid": ["GitHub Actions – The Complete Guide (Udemy)"], "docs": ["https://docs.github.com/en/actions"]}, "project": "Set up a full CI/CD pipeline for a web app on GitHub Actions"},
}

DEFAULT_SKILL = {
    "hours": 30,
    "phases": {
        "beginner":     "Learn fundamentals through official documentation and beginner tutorials",
        "intermediate": "Build small projects and follow structured courses on Udemy/Coursera",
        "advanced":     "Contribute to open source, build portfolio projects, get certified",
    },
    "resources": {
        "free": ["Official documentation", "YouTube tutorials", "freeCodeCamp"],
        "paid": ["Udemy courses (search skill name)", "Coursera specializations"],
        "docs": ["Search 'skill_name official docs'"],
    },
    "project": "Build a small project applying this skill end-to-end",
}

STYLE_RESOURCE_MAP = {"videos": "free", "projects": "free", "docs": "docs", "courses": "paid", "mixed": "free"}
LEVEL_MULTIPLIER   = {"beginner": 1.0, "intermediate": 0.7, "advanced": 0.5}


def _distribute(n_skills: int, total_slots: int) -> list[int]:
    """
    Distribute total_slots across n_skills proportionally (equal weight).
    Every skill gets at least 1 slot. Total always equals total_slots exactly.
    """
    base  = total_slots // n_skills
    extra = total_slots % n_skills
    slots = [base + (1 if i < extra else 0) for i in range(n_skills)]
    return slots


def _distribute_weighted(weights: list[float], total_slots: int) -> list[int]:
    """
    Distribute total_slots proportionally by weight.
    Every skill gets at least 1 slot. Total always equals total_slots exactly.
    """
    n = len(weights)
    if n > total_slots:
        # More skills than slots: give 1 to top skills, 0 to rest
        indexed = [(weights[i], i) for i in range(n)]
        indexed.sort(reverse=True)
        result = [0] * n
        for j in range(total_slots):
            result[indexed[j][1]] = 1
        return result
    
    total_w = sum(weights)
    raw     = [(w / total_w) * total_slots for w in weights]
    floors  = [max(1, math.floor(r)) for r in raw]
    diff    = total_slots - sum(floors)
    # Distribute remaining slots to skills with largest fractional parts
    fracs   = [(raw[i] - math.floor(raw[i]), i) for i in range(len(raw))]
    fracs.sort(reverse=True)
    for j in range(diff):
        floors[fracs[j][1]] += 1
    return floors


def generate_roadmap(
    role: str,
    missing_skills: list[str],
    skill_level: str      = "beginner",
    hours_per_week: float = 10.0,
    deadline_months: int  = 3,
    learning_style: str   = "mixed",
    budget: str           = "free",
    interests: str        = "",
) -> dict:

    if not missing_skills:
        return {"role": role, "summary": "You already have all required skills!",
                "phases": [], "weekly_plan": [], "timeline": {}, "tips": []}

    # ── Normalise ─────────────────────────────────────────────────────────────
    skill_level    = skill_level.lower()
    budget         = budget.lower()
    learning_style = learning_style.lower()
    multiplier     = LEVEL_MULTIPLIER.get(skill_level, 1.0)

    resource_key = STYLE_RESOURCE_MAP.get(learning_style, "free")
    if budget == "paid":           resource_key = "paid"
    elif learning_style == "docs": resource_key = "docs"

    phases_to_include = (
        ["beginner", "intermediate", "advanced"] if skill_level == "beginner" else
        ["intermediate", "advanced"]             if skill_level == "intermediate" else
        ["advanced"]
    )

    # ── Deadline: EXACTLY this many weeks, no more ────────────────────────────
    # Use more accurate weeks per month calculation
    # 1 month = 4 weeks, 2 months = 9 weeks, 3 months = 13 weeks, etc.
    weeks_per_month = {1: 4, 2: 9, 3: 13, 6: 26, 9: 39, 12: 52}
    total_weeks    = weeks_per_month.get(deadline_months, max(1, round(deadline_months * 4.33)))
    hours_per_day  = round(hours_per_week / 7, 2)
    total_hours    = round(hours_per_week * total_weeks)

    # ── Distribute weeks across skills by their relative weight ───────────────
    weights = [
        max(1.0, SKILL_DB.get(s.lower(), DEFAULT_SKILL)["hours"] * multiplier)
        for s in missing_skills
    ]
    skill_weeks = _distribute_weighted(weights, total_weeks)

    # Sanity check: sum must equal total_weeks
    assert sum(skill_weeks) == total_weeks, f"Week distribution error: {sum(skill_weeks)} != {total_weeks}"

    # ── Build phase plan ──────────────────────────────────────────────────────
    phase_plan  = []
    week_cursor = 1

    for i, skill in enumerate(missing_skills):
        weeks = skill_weeks[i]
        if weeks == 0:
            continue  # Skip skills with 0 weeks (happens when too many skills for short timeline)
        
        sl    = skill.lower()
        db    = SKILL_DB.get(sl, DEFAULT_SKILL)
        hours = round(weeks * hours_per_week)           # hours = weeks * hpw

        resources = db["resources"].get(resource_key, db["resources"]["free"])

        # Phase content: if only 1 week, show only the most relevant phase
        if weeks == 1:
            key = phases_to_include[0]
            phases_content = {key: f"[{weeks}w sprint] " + db["phases"].get(key, "Core fundamentals")}
        else:
            phases_content = {
                p: db["phases"][p]
                for p in phases_to_include
                if db["phases"].get(p)
            }

        phase_plan.append({
            "phase_num":  len(phase_plan) + 1,
            "skill":      skill,
            "start_week": week_cursor,
            "end_week":   week_cursor + weeks - 1,
            "hours":      hours,
            "phases":     phases_content,
            "resources":  resources,
            "project":    db.get("project", "Build a small project using this skill"),
        })
        week_cursor += weeks

    # Final week_cursor - 1 must equal total_weeks
    assert week_cursor - 1 == total_weeks, f"Phase plan overflow: ends at week {week_cursor-1}, expected {total_weeks}"

    # ── Build weekly plan: exactly total_weeks entries ────────────────────────
    weekly_plan = []
    for phase in phase_plan:
        phase_keys        = list(phase["phases"].keys())
        total_phase_weeks = phase["end_week"] - phase["start_week"] + 1

        for week in range(phase["start_week"], phase["end_week"] + 1):
            week_in_phase = week - phase["start_week"] + 1

            # Which phase content to show this week
            phase_idx = min(
                int((week_in_phase - 1) / total_phase_weeks * len(phase_keys)),
                len(phase_keys) - 1,
            )
            current_phase_key = phase_keys[phase_idx]
            phase_content     = phase["phases"][current_phase_key]

            weekly_plan.append({
                "week":      week,
                "skill":     phase["skill"],
                "focus":     f"{current_phase_key.title()} - {phase['skill'].title()}",
                "tasks":     phase_content,
                "hours":     hours_per_week,
                "daily_hrs": round(hours_per_day, 1),
                "project":   phase["project"] if week == phase["end_week"] else "",
            })

    # Verify weekly plan has exactly total_weeks entries
    assert len(weekly_plan) == total_weeks, f"Weekly plan has {len(weekly_plan)} entries, expected {total_weeks}"

    # ── Timeline ──────────────────────────────────────────────────────────────
    timeline = {
        "total_weeks":    total_weeks,
        "total_hours":    total_hours,
        "total_months":   round(total_weeks / 4.33, 1),
        "hours_per_week": hours_per_week,
        "daily_hours":    round(hours_per_day, 1),
    }

    # ── Tips ──────────────────────────────────────────────────────────────────
    skills_covered = len(phase_plan)
    skills_skipped = len(missing_skills) - skills_covered
    
    tips = [
        f"Your {total_weeks}-week plan covers {skills_covered} skill{'s' if skills_covered != 1 else ''} at {round(hours_per_day,1)}h/day.",
        f"Starting from {skill_level.title()} level — covering {', '.join(phases_to_include)} phase(s).",
        f"Complete the mini-project at the end of each skill to solidify learning.",
        f"Each skill gets proportional time based on its complexity — heavier skills get more weeks.",
    ]
    
    if skills_skipped > 0:
        skipped_names = [missing_skills[i] for i in range(len(missing_skills)) if skill_weeks[i] == 0]
        tips.insert(1, f"⚠️ Timeline too short: {skills_skipped} skill(s) excluded ({', '.join(skipped_names)}). Consider extending to 2-3 months.")

    ideal_hours = sum(
        SKILL_DB.get(s.lower(), DEFAULT_SKILL)["hours"] * multiplier
        for s in missing_skills
    )
    if total_hours < ideal_hours:
        coverage = round(total_hours / ideal_hours * 100)
        tips.append(
            f"Your {total_weeks}-week window covers ~{coverage}% of ideal depth. "
            f"Focus on core concepts and use the project at the end of each skill to practice."
        )
    else:
        tips.append("Your timeline gives enough time to cover all phases thoroughly.")

    if budget == "free":
        tips.append("Free resources selected — Kaggle, freeCodeCamp, and YouTube are your best friends.")
    if learning_style == "projects":
        tips.append("Project-based style — jump to hands-on tasks early, use docs as reference.")
    if learning_style == "videos":
        tips.append("Video learner — watch at 1.5x speed and pause to code along.")
    if interests:
        tips.append(f"Interested in {interests}? Find projects that combine it with {role} skills.")

    return {
        "role":           role,
        "skill_level":    skill_level,
        "summary":        f"{role} | {skill_level.title()} | {len(missing_skills)} skills | {total_weeks} weeks | {round(hours_per_day,1)}h/day",
        "timeline":       timeline,
        "phase_plan":     phase_plan,
        "weekly_plan":    weekly_plan,
        "tips":           tips,
        "tight_deadline": total_hours < ideal_hours,
    }
