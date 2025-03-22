import os
from docx import Document
import PyPDF2
import re
from src.config.regex_config import contact_info_regex, education_regex, work_experience_regex, skills_regex

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
    
def extract_contact_info(resume_text):
    contact_info = {}
    for section, pattern in contact_info_regex.items():
        match = re.search(pattern, resume_text)
        if match:
            contact_info[section] = match.group(2)  
    return contact_info

def extract_education(resume_text):
    match = re.search(education_regex, resume_text)
    if match:
        return match.group(1)  
    return None

def extract_work_experience(resume_text):
    match = re.search(work_experience_regex, resume_text)
    if match:
        return match.group(1)  
    return None

def extract_skills(resume_text, role):
    skills_section_regex = skills_regex.get(role)
    if skills_section_regex:
        match = re.search(skills_section_regex, resume_text)
        if match:
            return match.group(1)  
    return None

# Función para procesar el archivo cargado (BORRAR DESPUES)
def process_resume(file_path, role):
    # Leer el contenido del archivo
    resume_text = read_resume(file_path)
    
    # Extraer la información de contacto
    contact_info = extract_contact_info(resume_text)
    print("Contact Information:", contact_info)
    
    # Extraer la educación
    education = extract_education(resume_text)
    print("\nEducation:", education)
    
    # Extraer la experiencia laboral
    work_experience = extract_work_experience(resume_text)
    print("\nWork Experience:", work_experience)
    
    # Extraer las habilidades
    skills = extract_skills(resume_text, role)
    print("\nSkills:", skills)
