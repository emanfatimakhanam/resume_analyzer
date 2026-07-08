import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

skill_links = {
    "tensorflow": "https://www.tensorflow.org/",
    "pytorch": "https://pytorch.org/",
    "scikit learn": "https://scikit-learn.org/",
    "aws": "https://aws.amazon.com/training/",
    "model deployment": "https://www.coursera.org/learn/mlops",
    "deep learning": "https://www.deeplearning.ai/",
    "feature engineering": "https://www.kaggle.com/learn/feature-engineering",
    "data preprocessing": "https://www.geeksforgeeks.org/data-preprocessing-machine-learning/",
    "python": "https://docs.python.org/3/tutorial/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
}

dictionary = {
    'ml': 'Machine Learning',
    'ai': 'Artificial Intelligence',
    'dl': 'Deep Learning',
    'nlp': 'Natural Language Processing',
    'cv': 'Computer Vision',
    'ds': "Data Science",
    'dbms': "Database Management System",
    'sql': "SQL",
    "js": 'Javascript',
    'api': "Application Program Interface",
    'oop': "Object Oriented Programming"
}

synonyms = {
    # --- fixed: was "Postgresql" (capital P), which never matched since input is always lowercased first
    "postgresql": "sql",
    "postgres": "sql",
    "mysql": "sql",
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "node": "node.js",
    "nodejs": "node.js",
    "jira software": "jira",

    # --- AI / ML / NLP phrasing gaps (based on your resume vs. job_skills_raw keywords)
    "hugging face": "transformers",
    "huggingface": "transformers",
    "hugging face models": "transformers",
    "transformer models": "transformers",
    "large language models": "llms",
    "llm": "llms",
    "generative ai": "llms",
    "gen ai": "llms",
    "genai": "llms",
    "text classification": "nlp",
    "natural language processing": "nlp",
    "cosine similarity": "nlp",
    "tf-idf": "nlp",
    "tf idf": "nlp",
    "tfidf": "nlp",
    "fuzzy matching": "nlp",
    "image classification": "computer vision",
    "object detection": "computer vision",
    "cv": "computer vision",
    "model fine-tuning": "model tuning",
    "fine-tuning": "model tuning",
    "fine tuning": "model tuning",
    "hyperparameter tuning": "model tuning",
    "chatbot": "chatbots",
    "conversational ai": "chatbots",
    "model deployment": "model deployment",
    "mlops": "model deployment",
    "cloud deployment": "model deployment",

    # --- Data / stats phrasing gaps
    "data viz": "data visualization",
    "data visualisation": "data visualization",
    "eda": "data analysis",
    "exploratory data analysis": "data analysis",
    "data cleaning": "data preprocessing",
    "data wrangling": "data preprocessing",
    "feature selection": "feature engineering",

    # --- Web dev phrasing gaps
    "restful apis": "apis",
    "rest api": "apis",
    "rest apis": "apis",
    "api development": "apis",
    "responsive web design": "responsive design",
    "authentication and authorization": "authentication",
    "auth": "authentication",
    "unit tests": "unit testing",
    "testing": "unit testing",

    # --- DevOps / cloud phrasing gaps
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    "ci cd": "ci/cd",
    "amazon web services": "aws",
    "microsoft azure": "azure",
    "shell scripting": "bash scripting",
    "shell script": "bash scripting",
    "containerization": "docker",

    # --- Mobile phrasing gaps
    "react-native": "react native",
    "ui/ux design": "ui design",

    # --- Security phrasing gaps
    "pentesting": "penetration testing",
    "pen testing": "penetration testing",
    "vulnerability assessment": "penetration testing",
    "security information and event management": "siem",
}

# --------------------------
# Utility Functions
# --------------------------
def clean_text(raw_string):
    """Convert comma-separated skills into lowercased list."""
    return [skill.strip().lower() for skill in raw_string.split(",") if skill.strip()]

def expand_skills(skill_list, dictionary):
    """Expand abbreviations using dictionary."""
    expanded = []
    for skill in skill_list:
        full = dictionary.get(skill, skill)
        expanded.append(full.lower())
    return list(expanded)

def normalize(string):
    """Normalize skill names (remove dots, slashes, etc.)."""
    s = string.strip().lower()
    for ch in [".", "-", "/"]:
        s = s.replace(ch, " ")
    return " ".join(s.split())

def apply_synonym(string):
    """Map synonyms to standard terms."""
    string = normalize(string)
    return synonyms.get(string, string)

# --------------------------
# Core Matching Function
# --------------------------
def match_resume_skills(resume_skills, job_skills):
    matched = set()

    # Step 1: Exact + close matches
    for skill in resume_skills:
        if skill in job_skills:
            matched.add(skill)
        else:
            close_match = difflib.get_close_matches(skill, job_skills, n=3, cutoff=0.8)
            if close_match:
                matched.add(close_match[0])

    # Step 2: TF-IDF similarity
    # Guard against empty skill lists — TF-IDF crashes if there's nothing to compare
    if not resume_skills or not job_skills:
        similarity = 0
    else:
        vectorizer = TfidfVectorizer()
        documents = [" ".join(resume_skills), " ".join(job_skills)]
        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except ValueError:
            similarity = 0

    # Step 3: Scores
    match_percentage = round((len(matched) / len(job_skills)) * 100, 2) if job_skills else 0
    similarity_score = round(similarity * 100, 2)

    return {
        "matched_skills": list(matched),
        "missing_skills": list(set(job_skills) - matched),
        "match_percentage": match_percentage,   # exact skill match %
        "similarity_score": similarity_score    # TF-IDF similarity %
    }

# --------------------------
# Run Matching Against Job
# --------------------------
def run_matching(resume_skills, selected_job):
    job_skills_raw = {
        "Data Scientist": [
            "python", "machine learning", "deep learning", "data analysis",
            "pandas", "numpy", "matplotlib", "sql", "statistics",
            "scikit-learn", "tensorflow", "nlp", "data visualization"
        ],
        "Machine Learning Engineer": [
            "python", "tensorflow", "pytorch", "scikit-learn", "ml", "dl",
            "model deployment", "aws", "data preprocessing", "feature engineering"
        ],
        "Backend Developer": [
            "python", "django", "flask", "node.js", "sql", "postgresql",
            "apis", "jwt", "docker", "redis", "unit testing"
        ],
        "Frontend Developer": [
            "html", "css", "javascript", "react", "vue", "bootstrap",
            "responsive design", "webpack", "ui/ux", "tailwind css"
        ],
        "Full Stack Developer": [
            "html", "css", "javascript", "react", "node.js", "express",
            "sql", "mongodb", "git", "docker", "rest apis", "authentication"
        ],
        "DevOps Engineer": [
            "linux", "aws", "azure", "docker", "kubernetes", "jenkins",
            "terraform", "ci/cd", "monitoring", "bash scripting"
        ],
        "Mobile App Developer": [
            "flutter", "dart", "react native", "android", "ios",
            "firebase", "api integration", "ui design", "state management"
        ],
        "Database Administrator": [
            "sql", "mysql", "postgresql", "oracle", "database tuning",
            "indexing", "backup and recovery", "normalization", "query optimization"
        ],
        "Cybersecurity Analyst": [
            "network security", "ethical hacking", "penetration testing",
            "firewalls", "siem", "nmap", "wireshark", "incident response", "encryption"
        ],
        "AI Engineer": [
            "python", "pytorch", "tensorflow", "computer vision",
            "nlp", "chatbots", "transformers", "llms", "model tuning"
        ]
    }

    if selected_job not in job_skills_raw:
        return []

    job_selected = {selected_job: job_skills_raw[selected_job]}

    # Handle input type
    if isinstance(resume_skills, str):
        raw_tokens = clean_text(resume_skills)
    elif isinstance(resume_skills, list):
        raw_tokens = [s.lower().strip() for s in resume_skills if isinstance(s, str)]
    else:
        raw_tokens = []

    # Normalize + expand resume skills
    normalized_resume = [apply_synonym(tok) for tok in raw_tokens]
    resume_skills_expanded = expand_skills(normalized_resume, dictionary)

    result = []
    for job_title, job_tokens in job_selected.items():
        job_normalized = [apply_synonym(tok) for tok in job_tokens]
        job_skills_expanded = expand_skills(job_normalized, dictionary)

        # Use dict result
        match_result = match_resume_skills(resume_skills_expanded, job_skills_expanded)

        # Missing skill links
        missing_skills_links = [
            {"name": skill, "link": skill_links.get(skill.lower())}
            for skill in match_result["missing_skills"]
        ]

        # Final weighted score
        final_score = round((match_result["match_percentage"] * 0.6) + (match_result["similarity_score"] * 0.4), 2)

        result.append({
            "job_title": job_title,
            "resume_skills": resume_skills_expanded,
            "job_skills": job_skills_expanded,
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
            "missing_skills_links": missing_skills_links,
            "match_percentage": match_result["match_percentage"],
            "similarity_score": match_result["similarity_score"],
            "final_score": final_score
        })

    return result