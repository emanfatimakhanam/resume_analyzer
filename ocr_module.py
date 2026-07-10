import os
import requests
from dotenv import load_dotenv
from extractor import extract_fields

load_dotenv()
OCR_API_KEY = os.getenv('OCR_SPACE_API_KEY')
print("DEBUG OCR KEY:", OCR_API_KEY) 
OCR_API_URL = "https://api.ocr.space/parse/image"


def ocr_scanned(path):
    resumes = []  # kept local, not module-level — avoids stale results across requests

    file_ext = path.rsplit(".", 1)[-1].lower()

    with open(path, "rb") as f:
        response = requests.post(
            OCR_API_URL,
            files={"file": f},
            data={
                "apikey": OCR_API_KEY,
                "language": "eng",
                "isOverlayRequired": False,
                "OCREngine": 2,          # more accurate engine, handles PDFs + images
                "filetype": file_ext.upper(),
            },
            timeout=30,
        )

    result = response.json()
    print("DEBUG OCR RESPONSE:", result) 

    if result.get("IsErroredOnProcessing"):
        error_msg = result.get("ErrorMessage", ["OCR failed"])
        raise Exception(error_msg[0] if isinstance(error_msg, list) else error_msg)
    text = " "
    for parsed_result in result.get("ParsedResults", []):
        text += parsed_result.get("ParsedText", "")
    full_text = text.replace("|", "1")
    data = extract_fields(full_text)
    resumes.append(data)
    return resumes