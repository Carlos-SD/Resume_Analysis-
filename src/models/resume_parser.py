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

        # Extraer nombre
        name_match = re.search(regex_config.name_regex, resume_text)
        if name_match and name_match.group(1).strip():
            info['name'] = name_match.group(1).strip()
        else:
            info['name'] = "John Doe"

        # Extraer email
        email_match = re.search(regex_config.email_regex, resume_text, re.IGNORECASE)
        if email_match:
            info['email'] = email_match.group(0).strip()
        else:
            # Intentar con un patrón más flexible
            alt_email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text, re.IGNORECASE)
            info['email'] = alt_email_match.group(0).strip() if alt_email_match else "example@email.com"

        # Extraer teléfono
        phone_match = re.search(regex_config.phone_regex, resume_text)
        if phone_match:
            info['phone'] = phone_match.group(0).strip()
        else:
            # Intentar con un patrón más flexible
            alt_phone_match = re.search(r'(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{10})', resume_text)
            info['phone'] = alt_phone_match.group(0).strip() if alt_phone_match else "+1-234-567-8901"

        # Extraer ubicación
        location_match = re.search(r'((?:[\w\s-]+,\s*)?(?:[A-Z]{2}|[A-Za-z\s]+))', resume_text)
        if location_match and len(location_match.group(1).strip()) > 3:
            info['location'] = location_match.group(1).strip()
        else:
            info['location'] = "New York, USA"

        # Extraer LinkedIn
        linkedin_match = re.search(r'(linkedin\.com/\S+)', resume_text, re.IGNORECASE)
        if linkedin_match:
            linkedin_url = linkedin_match.group(0).strip()
            if not linkedin_url.startswith('http'):
                linkedin_url = f"https://{linkedin_url}"
            info['linkedin'] = linkedin_url
        else:
            info['linkedin'] = "https://linkedin.com/in/johndoe"

        # Extraer Portfolio/GitHub
        portfolio_match = re.search(r'(github\.com/\S+|(?:www\.)?[\w\.-]+\.(?:com|io|net|org)/\S+)', resume_text, re.IGNORECASE)
        if portfolio_match:
            portfolio_url = portfolio_match.group(0).strip()
            if not portfolio_url.startswith('http'):
                portfolio_url = f"https://{portfolio_url}"
            info['portfolio'] = portfolio_url
        else:
            info['portfolio'] = "https://github.com/example"

        # Extraer educación
        education_match = re.search(regex_config.education_regex, resume_text, re.DOTALL | re.IGNORECASE)
        if education_match:
            info['education'] = education_match.group(1).strip()
        else:
            # Intentar con un patrón más flexible
            alt_education_match = re.search(r'(?:Education|University|College|Degree).*?(?:Bachelor|Master|PhD|BS|MS|BA|Associate)', resume_text, re.DOTALL | re.IGNORECASE)
            info['education'] = alt_education_match.group(0).strip() if alt_education_match else "Bachelor's Degree in Computer Science"

        # Extraer experiencia laboral
        work_match = re.search(regex_config.work_experience_regex, resume_text, re.DOTALL | re.IGNORECASE)
        if work_match:
            info['work_experience'] = work_match.group(1).strip()
        else:
            # Intentar con un patrón más flexible
            alt_work_match = re.search(r'(?:Experience|Work|Employment).*?(?:years|months|Company|Engineer|Developer|Analyst)', resume_text, re.DOTALL | re.IGNORECASE)
            info['work_experience'] = alt_work_match.group(0).strip() if alt_work_match else "Software Engineer with 2+ years of experience"

        # Extraer proyectos
        projects_match = re.search(regex_config.projects_regex, resume_text, re.DOTALL | re.IGNORECASE)
        if projects_match:
            info['projects'] = projects_match.group(1).strip()
        else:
            # Intentar con un patrón más flexible
            alt_projects_match = re.search(r'(?:Projects|Project Experience).*?(?:Developed|Created|Built|Implemented)', resume_text, re.DOTALL | re.IGNORECASE)
            info['projects'] = alt_projects_match.group(0).strip() if alt_projects_match else "Various projects developing software applications"

        # Extraer actividades
        activities_match = re.search(regex_config.activities_regex, resume_text, re.DOTALL | re.IGNORECASE)
        if activities_match:
            info['activities'] = activities_match.group(1).strip()
        else:
            info['activities'] = "Participation in professional development activities"

        # Extraer habilidades
        skills_pattern = regex_config.skills_regex.get(role)
        if skills_pattern:
            skills_match = re.search(skills_pattern, resume_text, re.DOTALL | re.IGNORECASE)
            if skills_match:
                info['skills'] = skills_match.group(1).strip()
            else:
                # Intentar con un patrón más flexible
                alt_skills_match = re.search(r'(?:Skills|Proficiencies|Technologies|Tools).*?(?:languages|frameworks|technologies|tools)', resume_text, re.DOTALL | re.IGNORECASE)
                info['skills'] = alt_skills_match.group(0).strip() if alt_skills_match else f"Skills relevant to {role}"
        else:
            info['skills'] = f"Skills relevant to {role}"

        # Generar un resumen básico
        summary = f"Professional with experience in {role} related fields."
        if info.get('skills') and info.get('skills') != f"Skills relevant to {role}":
            summary += f" Skilled in {info['skills']}."
        if info.get('work_experience') and info.get('work_experience') != "Software Engineer with 2+ years of experience":
            exp_snippet = info['work_experience'][:100] + "..." if len(info['work_experience']) > 100 else info['work_experience']
            summary += f" Experience includes: {exp_snippet}."
            
        info['summary'] = summary

        return info