import difflib
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
    'nlp':'Natural Language Processing',
    'cv': 'Computer Vision',
    'ds': "Data Science",
    'dbms': "Database Management System",
    'sql': "SQL",  
    "js": 'Javascript',
    'api': "Application Program Interface",
    'oop': "Object Oriented Programming"
      }
synonyms = {
          "react.js" : "react",
          "Postgresql" : "sql",
          "jira software" : "jira"
}
# # Clean a string into lowercased skills list
def clean_text(raw_string):
    return [skill.strip().lower() for skill in raw_string.split(",") if skill.strip()]

# # Expand abbreviations using dictionary
def expand_skills(skill_list, dictionary):    
    expanded = [] 
    for skill in skill_list:
        full = dictionary.get(skill, skill)
        expanded.append(full.lower())
    return list(expanded) # avoid duplicates

# # Match resume skills to preset jobs list skills
def match_resume_skills(resume_skills, job_skills):
   matched = set()
   for skill in resume_skills:
    if skill in job_skills:
        matched.add(skill)
    else:
        close_match = difflib.get_close_matches(skill,job_skills,n = 3,cutoff = 0.8)
        if close_match:
            matched.add(close_match[0])
   score = round(len(matched)/len(job_skills) *100,2)
   return list(matched), score
def normalize(string):
    s = string.strip().lower()
    for ch in [".", "-", "/"]:
        s = s.replace(ch, " ")
    s = " ".join(s.split())
    return s
def apply_synonym(string):
    string = normalize(string)
    n_string = synonyms.get(string,string)
    return n_string
def run_matching(resume_skills,selected_job):
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
    ]}
    if selected_job in job_skills_raw:
           job_selected = {selected_job: job_skills_raw[selected_job]}
    else:
        return []
     

    # handle input type correctly
    if isinstance(resume_skills, str):
        raw_tokens = clean_text(resume_skills)
    elif isinstance(resume_skills, list):
         raw_tokens = [s.lower().strip() for s in resume_skills if isinstance(s, str)]
    else:
         raw_tokens = []
    # Normalize and expand resume skills
    normalized_resume = [apply_synonym(tok) for tok in raw_tokens]
    resume_skills_expanded = expand_skills(normalized_resume, dictionary)

    result = []
    for job_title, job_tokens in job_selected.items():
        job_normalized = [apply_synonym(tok) for tok in job_tokens]
        job_skills_expanded = expand_skills(job_normalized, dictionary) 
        matched, score = match_resume_skills(resume_skills_expanded, job_skills_expanded)
        not_matched = [skill for skill in job_skills_expanded if skill not in matched]
        missing_skills_links = [
             {"name": skill, "link": skill_links.get(skill.lower())}
             for skill in not_matched
             ]
        result.append({
            "matched_skills": matched,
            "resume_skills": resume_skills_expanded,
            "job_skills": job_skills_expanded,
            "score": score,
            "job_title": job_title,
            "missing_skills" : not_matched,
            "missing_skills_links": missing_skills_links
        })
    print(result)
    return result
