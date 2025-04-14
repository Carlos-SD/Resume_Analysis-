import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_parser import ResumeParser
from src.config import regex_config

class TestResumeParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = ResumeParser()
        self.temp_dir = tempfile.mkdtemp()
        
        self.txt_content = """
        JOHN SMITH
        john.smith@example.com
        (123) 456-7890
        New York, NY
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Example, 2018-2022
        
        WORK EXPERIENCE
        Software Engineer
        Tech Company Inc., 2022-Present
        - Developed web applications using Python and JavaScript
        - Collaborated with cross-functional teams
        
        PROJECTS
        E-commerce Platform
        - Implemented shopping cart functionality using React
        
        ACTIVITIES
        Hackathon participant, 2021
        
        SKILLS
        Programming: Python, JavaScript, Java
        Frameworks: React, Django, Flask
        Tools: Git, Docker, AWS
        """
        
        self.txt_path = os.path.join(self.temp_dir, "sample_resume.txt")
        with open(self.txt_path, 'w') as f:
            f.write(self.txt_content)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_read_txt(self):
        """Verificar la correcta lectura de archivos TXT"""
        text = self.parser.read_txt(self.txt_path)
        self.assertIsNotNone(text)
        self.assertIn("JOHN SMITH", text)
        self.assertIn("EDUCATION", text)
        self.assertIn("WORK EXPERIENCE", text)
    
    def test_read_resume(self):
        """Verificar la función general de lectura de resumes"""
        text = self.parser.read_resume(self.txt_path)
        self.assertIsNotNone(text)
        self.assertIn("JOHN SMITH", text)
    
   
    def test_extract_email(self):
        """Verificar la extracción del email"""
        info = self.parser.extract_resume_info(self.txt_content, "Software Engineer")
        self.assertIn("email", info)
        self.assertEqual("john.smith@example.com", info["email"])
    
    def test_extract_phone(self):
        """Verificar la extracción del teléfono"""
        info = self.parser.extract_resume_info(self.txt_content, "Software Engineer")
        self.assertIn("phone", info)
        self.assertEqual("(123) 456-7890", info["phone"])
    
    def test_extract_education(self):
        """Verificar la extracción de educación"""
        info = self.parser.extract_resume_info(self.txt_content, "Software Engineer")
        self.assertIn("education", info)
        self.assertIn("Bachelor of Science", info["education"])
    
    def test_extract_work_experience(self):
        """Verificar la extracción de experiencia laboral"""
        info = self.parser.extract_resume_info(self.txt_content, "Software Engineer")
        self.assertIn("work_experience", info)
        self.assertIn("Software Engineer", info["work_experience"])
    
    def test_extract_skills(self):
        """Verificar la extracción de habilidades"""
        info = self.parser.extract_resume_info(self.txt_content, "Software Engineer")
        self.assertIn("skills", info)
        self.assertIn("Python", info["skills"])
    
    def test_missing_info_handling(self):
        """Verificar el manejo de información faltante"""
        minimal_content = """
        JOHN DOE
        
        SKILLS
        Programming: Python, JavaScript
        """
        
        info = self.parser.extract_resume_info(minimal_content, "Software Engineer")
        
        self.assertEqual("example@email.com", info["email"])
        self.assertEqual("+1-234-567-8901", info["phone"])
        
    def test_different_role(self):
        """Verificar extracción con diferentes roles"""
        data_scientist_info = self.parser.extract_resume_info(self.txt_content, "Data Scientist")
        web_developer_info = self.parser.extract_resume_info(self.txt_content, "Web Developer")
        
        self.assertEqual(data_scientist_info["name"], web_developer_info["name"])
        self.assertIn("skills", data_scientist_info)
        self.assertIn("skills", web_developer_info)

if __name__ == "__main__":
    unittest.main()