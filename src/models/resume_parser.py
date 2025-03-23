import os
from docx import Document
import PyPDF2
import re
from src.config import regex_config

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def read_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_resume(file_path):
    extension = os.path.splitext(file_path)[1].lower()  # Obtener la extensión del archivo

    if extension == '.docx':
        return read_docx(file_path)
    elif extension == '.pdf':
        return read_pdf(file_path)
    elif extension == '.txt':
        return read_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a .docx, .pdf, or .txt file.")
    

def extract_resume_info(resume_text, role):
    info = {}

    name_match = re.search(regex_config.name_regex, resume_text)
    info['name'] = name_match.group(1).strip() if name_match else None

    email_match = re.search(regex_config.email_regex, resume_text, re.IGNORECASE)
    info['email'] = email_match.group(0).strip() if email_match else None

    phone_match = re.search(regex_config.phone_regex, resume_text)
    info['phone'] = phone_match.group(0).strip() if phone_match else None

    education_match = re.search(regex_config.education_regex, resume_text, re.DOTALL | re.IGNORECASE)
    info['education'] = education_match.group(1).strip() if education_match else None

    work_match = re.search(regex_config.work_experience_regex, resume_text, re.DOTALL | re.IGNORECASE)
    info['work_experience'] = work_match.group(1).strip() if work_match else None

    skills_pattern = regex_config.skills_regex.get(role)
    if skills_pattern:
        skills_match = re.search(skills_pattern, resume_text, re.DOTALL | re.IGNORECASE)
        info['skills'] = skills_match.group(1).strip() if skills_match else None
    else:
        info['skills'] = None

    return info  