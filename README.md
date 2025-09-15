for line in lines[:1]:
#         name = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+))",line)# no capturing separately last name QUESTION MARK removes non capturing grouo like repeating last word after space or spaces separately capture in separate group
#        # \b means the world word not substring if  {0 } means only first one word separately and {1} first and space and last and {0,2} first middle last
    

#     email = re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9]{2,}",text)

# print(phoneno)
# print(name)       
# with open("Name1.pdf","rb") as file:
#     reader= PyPDF2.PdfReader(file)#pypdf2 has a class pdfreader which allow to read pdf and extract content and checks how many pages etc
#     text = " "
#     for  page in reader.pages:# raeder.pages is list like container property is pages or it is attribute that conatin all pages object and page is
#         #single element of pageobject each page is pageobject
#          text += page.extract_text()
#           content extracted from single page
# Behind the scenes:
# PageObject is a class defined in PyPDF2.

# It wraps all the data and functions needed to interact with a page in a PDF file.
    
# HERE IN CODE the characters are always in brackets becuase multiple [abc] 
# means matches eithre from them which is differnet from abc these \c\a treats python seprately caharcters and here - is range litterals so used it at end or 
# with \ character and + outside brcaket means not onlt match one single character rather match one or more like hyphen dot etc
<!-- import json
data = {
    "name": "Anaya",
    "skill" : "Data"}
with open("data","w") as f:
    <!-- json.dump(data,f) --#this simple code open measn open filename as write and seconds line dump part of built in module json which used to wwrite dictionary into file as a json
    def extract_name(text):
    match = re.search(r"(?:Dr\.\s*)?[A-Z][a-z]+(?:\s[A-Z][a-z]+){1}", text.strip())
    return match.group(0) if match else ""#group 0 means no capturing group whole and if 1 measn 1 group capturing and so on

for filename in os.listdir("resumes"):
    path = os.path.join("resumes", filename)
    with pdfplumber.open(path) as pdf:
        full_text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())# page.extract return text as string and if part ensure skip pages if no text and than string extracted text ready to pass into functiions.name skill etc

    people_section = re.split(r"Name[:\s]+", full_text)

    for people_data in people_section[0:]:#start loop from 1 becuase name split it confuse your result either empty string or etc.
        if extract_name(people_data):  # only append if name found
            resumes_data = {
                "Name": extract_name(people_data),
                "Phone": phone_extract(people_data),
                "Email": extract_email(people_data),
                "Skills": extract_skills(people_data),
                "Experience": extract_experience(people_data)

            }
            resumes.append(resumes_data)
            

with open("data.json", 'w') as f:
    json.dump(resumes, f, indent=3)
    import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image = cv2.imread('image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Optional: Denoising
thresh = cv2.medianBlur(thresh, 3)

# OCR
text = pytesseract.image_to_string(thresh)
print(text)
from PIL import Image
# image_paths = ["resume.jpg","scan1.jpg"]
# images = [Image.open(path).convert('RGB') for path in image_paths]
# images[0].save("merged.pdf",save_all = True,append_images = images[1:])