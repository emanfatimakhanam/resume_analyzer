from PIL import Image
import cv2         # used to preprocess images using threshold
import numpy as np
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
from extractor import extract_fields

load_dotenv()
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
POPPLER_PATH = os.getenv("POPPLER_PATH")  # fixed typo: was POPLER_PATH

import pytesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def preprocess_images(img):
    img = np.array(img)                          # OpenCV takes a numpy array (height, width, color)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # convert to grayscale
    blur = cv2.GaussianBlur(img, (3, 3), 0)       # reduce noise before threshold
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    clean_img = Image.fromarray(thresh)           # back to PIL image for pytesseract
    return clean_img


def ocr_scanned(path):
    resumes = []  # fixed: was module-level global, causing stale results across requests

    # Check the file type first — image files (jpg/png) should be opened directly,
    # only actual PDFs need Poppler's convert_from_path()
    file_ext = path.rsplit(".", 1)[-1].lower()
    image_extensions = {"jpg", "jpeg", "png"}

    images = []
    if file_ext in image_extensions:
        images = [Image.open(path)]
    else:
        images = convert_from_path(path, poppler_path=POPPLER_PATH, dpi=300)

    text = " "
    for img in images:
        preprocessed_image = preprocess_images(img)
        text += pytesseract.image_to_string(preprocessed_image)
    full_text = text.replace("|", "1")
    data = extract_fields(full_text)
    resumes.append(data)
    return resumes