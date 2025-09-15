import re
import difflib
def phone_extract(full_text):
                    return re.findall(r"(\+?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,})", full_text)

def extract_email(full_text):
                    return re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-\s]+(?:\.[A-Za-z]{2,})+", full_text)
def extract_name(full_text):
                    match = re.search(r"Name[:\s]+(?:Dr\.\s*)?([A-Z][a-z]+(?:\s[A-Z][a-z]+){1})", full_text.strip())
                    return match.group(1) if match else ""        #group 0 means no capturing group whole and if 1 it means capturing group 1.

def extract_skills(full_text):
    skill_keywords = [
        "Python", "Java", "SQL", "Excel", "Power BI", "Tableau", "React", "Django", "mysql",  "oracle", "database tuning",
        "indexing", "backup and recovery", "normalization", "query optimization","network security", "ethical hacking", "penetration testing",
        "firewalls", "siem", "nmap", "wireshark", "incident response", "encryption","nlp", "chatbots", "transformers", "llms", "model tuning"
        "Machine Learning", "Data Analysis", "Agile", "Spring Boot", "PostgreSQL", "flutter", "dart", "react native", "android", "ios",
        "firebase", "api integration", "ui design", "state management",  "linux", "aws", "azure", "docker", "kubernetes", "jenkins",
        "terraform", "ci/cd", "monitoring", "bash scripting","html", "css", "javascript", "react", "vue", "bootstrap",
        "responsive design", "webpack", "ui/ux", "tailwind css", "apis", "jwt", "docker", "redis", "unit testing", "ml", "dl",
        "model deployment", "aws", "data preprocessing", "feature engineering", "machine learning", "deep learning", "data analysis",
        "pandas", "numpy", "matplotlib", "sql", "statistics", "scikit-learn", "tensorflow", "nlp", "data visualization"
        "Jira", "Team Leadership", "Research", "NLP", "Data Mining", "JavaScript","pytorch", "tensorflow", "computer vision"
    ]
    words = full_text.split()
    found = []

    for word in words:
        matches = difflib.get_close_matches(word, skill_keywords, n=1, cutoff=0.8)
        if matches:
            found.append(matches[0])  # matches is a list, take the first element
    # Extra check for multi-word skills
    lower_text = full_text.lower()
    for skill in skill_keywords:
        if skill.lower() in lower_text:
            found.append(skill)

    return list(set(found))  # remove duplicates

def extract_experience(full_text):
                    experience = re.findall(r"Experience[:\s]*\d+(?:\.\d+)?\s+years\s+(?:as|in)\s+(?:[A-Z][a-z]+\s?){1,3}",full_text)
                    return [e.replace('Experience: ', "").strip() for e in experience]#strip remove whitespace character before and after  
def extract_fields(full_text):
       return  {
                'Name': extract_name(full_text),
                "Email" : extract_email(full_text),
                "Phone" : phone_extract(full_text),
                "Skills" : extract_skills(full_text),
                "Experience" : extract_experience(full_text)
        }

