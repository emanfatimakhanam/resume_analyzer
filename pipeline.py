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
        print(f"PDF check failed for {path}: {e}")
        return False


def check_process(path):
    if check_pdf(path):
        return pdf_parser(path) or []
    else:
        return ocr_scanned(path) or []


def process_file_text(path, selected_job):
    resumes = check_process(path)
    if not resumes:
        return []

    # DB write is best-effort logging only — never let it break the user-facing result
    try:
        from database import db_initialize
        db_initialize()
        database.insert_all(resumes)
    except Exception as e:
        print(f"DB insert skipped (non-critical): {e}")

    return run_matching(resumes[0]["Skills"], selected_job)