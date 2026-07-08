
import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

def phone_extract(full_text):
    return re.findall(r"(\+?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,})", full_text)

def extract_email(full_text):
    return re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}", full_text)

def extract_name(full_text):
    doc = nlp(full_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # Fallback: if spaCy can't find a name, assume it's the first line of the resume
    # (this is where names almost always appear)
    lines = [line.strip() for line in full_text.strip().split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        # a real name is usually short (1-4 words) and doesn't contain @ or numbers
        word_count = len(first_line.split())
        if 1 <= word_count <= 4 and "@" not in first_line and not any(ch.isdigit() for ch in first_line):
            return first_line
    return ""

skill_keywords = [
    "Python", "Java", "SQL", "Excel", "Power BI", "Tableau", "React", "Django", "MySQL", "Oracle",
    "Machine Learning", "Deep Learning", "NLP", "Data Analysis", "Docker", "Kubernetes", "data analysis",
    "pandas", "numpy", "matplotlib", "sql", "statistics","scikit-learn", "tensorflow", "nlp", "data visualization","pytorch", "scikit-learn", "ml", "dl",
    "model deployment", "aws", "data preprocessing", "feature engineering","django", "flask", "node.js", "sql", "postgresql",
        "apis", "jwt", "docker", "redis", "unit testing",  "html", "css", "javascript", "react", "vue", "bootstrap",
        "responsive design", "webpack", "ui/ux", "tailwind css", "flutter", "dart", "react native", "android", "ios",
        "firebase", "api integration", "ui design", "state management", "linux", "aws", "azure", "docker", "kubernetes", "jenkins",
        "terraform", "ci/cd", "monitoring", "bash scripting", "network security", "ethical hacking", "penetration testing",
        "firewalls", "siem", "nmap", "wireshark", "incident response", "encryption", "computer vision",
        "nlp", "chatbots", "transformers", "llms", "model tuning"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # make matching case-insensitive
patterns = [nlp.make_doc(skill) for skill in skill_keywords]
matcher.add("Skills", patterns)

def extract_skills(full_text):
    doc = nlp(full_text)
    matches = matcher(doc)
    found = [doc[start:end].text for match_id, start, end in matches]
    return list(set(found))

def extract_experience(full_text):
    experience = []

    # Catch date ranges like "2021 - 2023", "Jan 2021 - Present", "2020-2024"
    date_range_pattern = r"(?:[A-Za-z]{3,9}\.?\s)?\d{4}\s*[-–—to]+\s*(?:[A-Za-z]{3,9}\.?\s)?(?:\d{4}|Present|present|Current|current)"
    date_ranges = re.findall(date_range_pattern, full_text)
    experience.extend(date_ranges)

    # Also keep catching phrases like "5 years of experience"
    doc = nlp(full_text)
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME", "QUANTITY"]:
            if "year" in ent.text.lower():
                experience.append(ent.text)

    return experience

def extract_fields(full_text):
    return {
        "Name": extract_name(full_text),
        "Email": extract_email(full_text),
        "Phone": phone_extract(full_text),
        "Skills": extract_skills(full_text),
        "Experience": extract_experience(full_text)
    }