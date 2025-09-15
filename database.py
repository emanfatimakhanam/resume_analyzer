import sqlite3
import re
# Create connection and cursor
def db_initialize():
    with sqlite3.connect("resumes.db") as conn:
     cursor = conn.cursor()

    # Create table if not exists
     cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            skills TEXT,
            experience INTEGER,
            phone TEXT,
            email TEXT
        )
    ''')
    
     conn.commit()

# Function to clean and format the raw JSON data
def cleaning_format(people):
    cleaned = []
    for item in people:
        if not isinstance(item, dict):
            continue
        name = item.get("Name", "unknown")

        # Clean skills
        skills = item.get("Skills", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        
        # Clean experience
        experience = item.get("Experience", [])
        if isinstance(experience, list) and experience:
            try:
                match = re.search(r"\d+(?:\.\d+)?",experience[0])
                if match:
                    value= float(match.group())
                    experience = int(value) if value.is_integer() else value
            except:
                experience = 0        
        elif isinstance(experience, str):
            try:
                 match = re.search(r"\:\s*\d+(?:\.\d+)?",experience)
                 if match:
                    value = float(match.group())
                    experience = int(value) if value.is_integer() else value #experience = int(''.join(filter(str.isdigit, experience))) for integer just
            except:
                experience = 0
        else:
            experience = 0
        phone = item.get("Phone", [""])[0] if item.get("Phone") else ""
        email = item.get("Email", [""])[0] if item.get("Email") else ""

        cleaned.append({
            "Name": name,
            "Skills": skills,
            "Experience": experience,
            "Phone": phone,
            "Email": email
        })
    return cleaned

# Function to insert a single resume
def insert_resumes(cursor,person):
    cursor.execute('''
        INSERT INTO resumes (name, skills, experience, phone, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        person["Name"],
        ", ".join(person["Skills"]),
        person["Experience"],
        person["Phone"],
        person["Email"] if isinstance(person["Email"], str) else person["Email"][0]
    ))

# Function to clean all and insert all
def insert_all(all_resumes):
    cleaned = cleaning_format(all_resumes)
    with sqlite3.connect("resumes.db") as conn:
        cursor = conn.cursor()
        for person in cleaned:
            insert_resumes(cursor, person)
        conn.commit()

