import pdfplumber
import database
from resumeparser import pdf_parser
from ocr_module import ocr_scanned
from matcher import run_matching
def check_pdf(path):
    try:
        with pdfplumber.open(path) as pdf:
            full_text = " ".join(page.extract_text() or "" for page in pdf.pages)
            if full_text.strip():
                return full_text.strip()
    except Exception as e:
                 return False
def check_process(path):
    if check_pdf(path):
        return pdf_parser(path) or []
    else:
        return ocr_scanned(path) or []
def process_file_text(path, selected_job):
    from database import db_initialize  
    db_initialize()  
    resumes = check_process(path)
    if not resumes:
        return []
    database.insert_all(resumes)
    return run_matching(resumes[0]["Skills"], selected_job)
                   
                   
                  
                   
                   
                   
                   
                   
                   
    
   
