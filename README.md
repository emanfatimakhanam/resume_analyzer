# Resume Analyzer - AI & ML Job Roles

A **Python project** that analyzes resumes against predefined AI & Machine Learning job roles and calculates a **skill match score**.  
This project is created for **learning purposes** and demonstrates how resumes can be matched to specific job requirements.

---

## 🚀 Features
- Predefined job descriptions for **AI & ML related roles** (e.g., Machine Learning Engineer, Data Scientist, AI Engineer).  
- Extracts skills from uploaded resumes.  
- Compares resume skills with required job skills.  
- Calculates a **match score (%)**.  
- Displays results showing matched and missing skills, with hyperlinks.  

---

## 🛠️ Tech Stack
- **Python** – Core programming language  
- **Regex** – For text processing and skill extraction  
- **SQLite** – Optional database for storing resumes & results  
- **Flask** – Web interface  

---

## 📂 Project Structure

resume_analyzer/
├── app.py # Main application file
├── extractor.py # Resume text extraction
├── matcher.py # Matching logic
├── database.py # Database handling
├── requirements.txt # Project dependencies
├── resumes.db # Sample database (ignored in .gitignore)
├── data.json # Example job description data
├── sample_resumes/ # Folder containing test resumes
└── .env.example # Example environment variables


## ⚡ How It Works
1. Input a **job description**.  
2. Upload one or more **resumes**.  
3. The system extracts **keywords/skills**.  
4. A **match score (%)** is calculated:

```python
score = (matched_skills / total_required_skills) * 100


📦 Installation & Usage

Clone this repository:
git clone https://github.com/emanfatimakhanam/resume_analyzer.git
cd resume_analyzer
Create a virtual environment & install dependencies:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
Run the app:
python app.py
🎯 Future Improvements
Integrate advanced NLP models for better skill extraction.

Build a web-based dashboard for recruiters.

Implement a resume ranking system.

🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.
