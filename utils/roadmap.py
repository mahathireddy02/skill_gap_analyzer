SKILL_ROADMAP = {
    "python": {
        "beginner": "Learn Python basics: variables, loops, functions (freeCodeCamp / Python.org)",
        "intermediate": "OOP, file handling, libraries (Automate the Boring Stuff)",
        "advanced": "Async programming, packaging, testing (Real Python)",
    },
    "machine learning": {
        "beginner": "ML concepts: supervised/unsupervised learning (Coursera - Andrew Ng)",
        "intermediate": "Scikit-learn, model evaluation, feature engineering",
        "advanced": "Ensemble methods, hyperparameter tuning, MLOps",
    },
    "deep learning": {
        "beginner": "Neural networks basics, backpropagation (3Blue1Brown series)",
        "intermediate": "CNNs, RNNs with TensorFlow/Keras",
        "advanced": "Transformers, GANs, model deployment",
    },
    "sql": {
        "beginner": "SELECT, WHERE, JOIN basics (SQLZoo / W3Schools)",
        "intermediate": "Aggregations, subqueries, window functions",
        "advanced": "Query optimization, indexing, stored procedures",
    },
    "javascript": {
        "beginner": "JS fundamentals: DOM, events, ES6 (javascript.info)",
        "intermediate": "Async/await, fetch API, modules",
        "advanced": "Design patterns, performance, TypeScript",
    },
    "react": {
        "beginner": "Components, props, state (official React docs)",
        "intermediate": "Hooks, context API, React Router",
        "advanced": "Redux, performance optimization, testing",
    },
    "docker": {
        "beginner": "Containers vs VMs, Dockerfile basics (Play with Docker)",
        "intermediate": "Docker Compose, volumes, networking",
        "advanced": "Multi-stage builds, Docker Swarm, security",
    },
    "aws": {
        "beginner": "AWS core services: EC2, S3, IAM (AWS Free Tier)",
        "intermediate": "Lambda, RDS, VPC, CloudFormation",
        "advanced": "Well-Architected Framework, cost optimization, certifications",
    },
    "git": {
        "beginner": "Init, commit, push, pull (GitHub Hello World guide)",
        "intermediate": "Branching, merging, rebasing",
        "advanced": "Git workflows, hooks, CI/CD integration",
    },
    "kubernetes": {
        "beginner": "Pods, deployments, services (Kubernetes.io tutorials)",
        "intermediate": "ConfigMaps, secrets, ingress, namespaces",
        "advanced": "Helm, RBAC, cluster autoscaling, monitoring",
    },
}

DEFAULT_ROADMAP = {
    "beginner": "Search official documentation and beginner tutorials on YouTube",
    "intermediate": "Build small projects and follow structured courses on Udemy/Coursera",
    "advanced": "Contribute to open source, build portfolio projects, get certified",
}

def get_roadmap(missing_skills):
    roadmap = {}
    for skill in missing_skills:
        roadmap[skill] = SKILL_ROADMAP.get(skill.lower(), DEFAULT_ROADMAP)
    return roadmap
