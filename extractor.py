import re

def phone_extract(full_text):
    return re.findall(r"(\+?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,})", full_text)

def extract_email(full_text):
    return re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", full_text)

def extract_name(full_text):
    # Resumes almost always put the name on the first non-empty line
    lines = [line.strip() for line in full_text.strip().split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        word_count = len(first_line.split())
        if 1 <= word_count <= 4 and "@" not in first_line and not any(ch.isdigit() for ch in first_line):
            return first_line
    return ""

skill_keywords = [
    "Python", "Java", "SQL", "Excel", "Power BI", "Tableau", "React", "Django", "MySQL", "Oracle",
    "Machine Learning", "Deep Learning", "NLP", "Data Analysis", "Docker", "Kubernetes",
    "pandas", "numpy", "matplotlib", "statistics", "scikit-learn", "tensorflow", "data visualization",
    "pytorch", "ml", "dl", "model deployment", "aws", "data preprocessing", "feature engineering",
    "flask", "node.js", "postgresql", "apis", "jwt", "redis", "unit testing", "html", "css",
    "javascript", "vue", "bootstrap", "responsive design", "webpack", "ui/ux", "tailwind css",
    "flutter", "dart", "react native", "android", "ios", "firebase", "api integration", "ui design",
    "state management", "linux", "azure", "jenkins", "terraform", "ci/cd", "monitoring",
    "bash scripting", "network security", "ethical hacking", "penetration testing", "firewalls",
    "siem", "nmap", "wireshark", "incident response", "encryption", "computer vision", "chatbots",
    "transformers", "llms", "model tuning"
]

def extract_skills(full_text):
    text_lower = full_text.lower()
    found = []
    for skill in skill_keywords:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(set(found))

def extract_experience(full_text):
    experience = []
    date_range_pattern = r"(?:[A-Za-z]{3,9}\.?\s)?\d{4}\s*[-–—to]+\s*(?:[A-Za-z]{3,9}\.?\s)?(?:\d{4}|Present|present|Current|current)"
    date_ranges = re.findall(date_range_pattern, full_text)
    experience.extend(date_ranges)

    year_exp_pattern = r"\d+(?:\.\d+)?\+?\s*years?\s*(?:of\s*)?experience"
    year_matches = re.findall(year_exp_pattern, full_text, re.IGNORECASE)
    experience.extend(year_matches)

    return experience

def extract_fields(full_text):
    return {
        "Name": extract_name(full_text),
        "Email": extract_email(full_text),
        "Phone": phone_extract(full_text),
        "Skills": extract_skills(full_text),
        "Experience": extract_experience(full_text)
    }