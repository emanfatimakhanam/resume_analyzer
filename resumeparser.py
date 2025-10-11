import re
import pdfplumber
from extractor import extract_fields

def pdf_parser(path):
        resumes = []
        with pdfplumber.open(path) as pdf:
           full_text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
        resume_data = extract_fields(full_text)
        resumes.append(resume_data)
        return resumes
    