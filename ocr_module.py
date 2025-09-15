from PIL import Image
import cv2         #used to preprocess images using threshold
import numpy as np
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path
from extractor import extract_fields
load_dotenv()
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
POPPLER_PATH = os.getenv("POPLER_PATH")
import pytesseract #  it is python wrapper behind it google tesseract ocr engine in back ground is working
pytesseract.pytesseract.tesseract_cmd =  TESSERACT_PATH
def preprocess_images(img):
        img = np.array(img)                          #Opencv takes as a numpy array 3d (height,width,color)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)           #color converted into grayscale standard fomula(height,width)
        blur = cv2.GaussianBlur(img,(3,3),0)        #Kernel size to change and calculate values of pixels
        _, thresh = cv2.threshold(blur,150,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    #images are preprocess to reduce noise increase accuracy of extraction data
        clean_img = Image.fromarray(thresh)      #convert image into pil image
        return clean_img
resumes = []
def ocr_scanned(path):
          images = convert_from_path(path,poppler_path=POPPLER_PATH,dpi = 300)
          text = " "
          for img in images:
            preprocessed_image =  preprocess_images(img)
            text += pytesseract.image_to_string(preprocessed_image) 
          full_text = text.replace("|", "1")
          print("full_text",full_text)
          list = extract_fields(full_text)
          resumes.append(list)
          return resumes
    

