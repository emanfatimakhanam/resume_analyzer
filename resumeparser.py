import re
import pdfplumber

from extractor import extract_email,extract_experience,extract_name,extract_skills,phone_extract

def pdf_parser(path):
        resumes = []
        with pdfplumber.open(path) as pdf:
           full_text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
        if full_text.count("Name:") > 1:
                people_section = re.split(r"Name[:\s]+",full_text)
                for people in people_section[1:]:
                    if extract_name("Name: "+ people):
                        resumes_data = {
                                "Name": extract_name("Name: "+ people),
                                "Phone": phone_extract(people),
                                "Email": extract_email(people),
                                "Skills": extract_skills(people),
                                "Experience": extract_experience(people)

                }
                        resumes.append(resumes_data)
        else:

            resumes_data = {
                        "Name": extract_name(full_text),
                        "Phone": phone_extract(full_text),
                        "Email": extract_email(full_text),
                        "Skills": extract_skills(full_text),
                        "Experience": extract_experience(full_text)

                    }
            resumes.append(resumes_data)
        return resumes
    