import os
from docx import Document
import PyPDF2
import re
from src.config import regex_config

class ResumeParser:

    def read_docx(self, file_path):
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    def read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

    def read_txt(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def read_resume(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()  
        if extension == '.docx':
            return self.read_docx(file_path)
        elif extension == '.pdf':
            return self.read_pdf(file_path)
        elif extension == '.txt':
            return self.read_txt(file_path)
        else:
            raise ValueError("Unsupported file type. Please upload a .docx, .pdf, or .txt file.")

    def extract_resume_info(self, resume_text, role):
        info = {}

        name_match = re.search(regex_config.name_regex, resume_text)
        info['name'] = "\n" + name_match.group(1).strip() + "\n" if name_match else "None\n" 

        email_match = re.search(regex_config.email_regex, resume_text, re.IGNORECASE)
        info['email'] = "\n" + email_match.group(0).strip() if email_match else "None\n" 

        phone_match = re.search(regex_config.phone_regex, resume_text)
        info['phone'] = "\n" + phone_match.group(0).strip() if phone_match else "None\n" 

        education_match = re.search(regex_config.education_regex, resume_text, re.DOTALL | re.IGNORECASE)
        info['education'] = "\n" + education_match.group(1).strip() + "\n" if education_match else "None\n"  

        work_match = re.search(regex_config.work_experience_regex, resume_text, re.DOTALL | re.IGNORECASE)
        info['work_experience'] = "\n" + work_match.group(1).strip() + "\n" if work_match else "None\n" 

        projects_match = re.search(regex_config.projects_regex, resume_text, re.DOTALL | re.IGNORECASE)
        info['projects'] = "\n" + projects_match.group(1).strip() if projects_match else "None\n" 

        activities_match = re.search(regex_config.activities_regex, resume_text, re.DOTALL | re.IGNORECASE)
        info['activities'] = "\n" + activities_match.group(1).strip() if activities_match else "None\n" 

        skills_pattern = regex_config.skills_regex.get(role)
        if skills_pattern:
            skills_match = re.search(skills_pattern, resume_text, re.DOTALL | re.IGNORECASE)
            info['skills'] = "\n" + skills_match.group(1).strip() if skills_match else "None\n" 
        else:
            info['skills'] = "None\n" 

        return info