import unittest
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_grammar import ResumeGrammarValidator
from textx import TextXSyntaxError, TextXSemanticError

class TestResumeGrammar(unittest.TestCase):
    
    def setUp(self):
        self.validator = ResumeGrammarValidator()
        
        self.valid_summary = """
Personal Information:
John Smith
john.smith@example.com
(123) 456-7890
New York, USA
https://www.linkedin.com/in/johnsmith
https://johnsmith.dev

Summary:
Experienced software engineer with over 8 years of expertise in full-stack development, 
specializing in scalable web applications and cloud architecture. Proficient in Python, 
JavaScript, and various cloud platforms with a track record of delivering high-quality, 
performance-optimized solutions.
"""
        
        self.invalid_email_summary = """
Personal Information:
Jane Doe
janedoe.example.com
(123) 456-7890
San Francisco, USA
https://www.linkedin.com/in/janedoe
https://janedoe.dev

Summary:
Frontend developer with experience in React and Angular.
"""
        
        self.short_summary = """
Personal Information:
Bob Johnson
bob.johnson@example.com
(123) 456-7890
Chicago, USA
https://www.linkedin.com/in/bobjohnson
https://bobjohnson.dev

Summary:
Junior developer.
"""
        
        self.malformatted_summary = """
Personal Info:
Alice Brown
alice@example.com
(123) 456-7890

About Me:
Data scientist with 3 years of experience.
"""
    
    def test_valid_grammar(self):
        """Verificar que un resumen válido pasa la validación sin cambios"""
        model = self.validator.parse_and_validate(self.valid_summary)
        
        self.assertEqual("John Smith", model.personal_info.full_name)
        self.assertEqual("john.smith@example.com", model.personal_info.email)
        self.assertEqual("(123) 456-7890", model.personal_info.phone)
        self.assertEqual("New York, USA", model.personal_info.location)
        self.assertEqual("https://www.linkedin.com/in/johnsmith", model.personal_info.linkedin)
        self.assertEqual("https://johnsmith.dev", model.personal_info.portfolio)
        self.assertIn("Experienced software engineer", model.summary.content)
    
    def test_invalid_email_correction(self):
        """Verificar la corrección de un email inválido"""
        model = self.validator.parse_and_validate(self.invalid_email_summary)
        
        original_email = "janedoe.example.com"
        self.assertNotEqual(original_email, model.personal_info.email)
        
        self.assertTrue(self.validator.validate_email(model.personal_info.email))
    
    def test_short_summary_extension(self):
        """Verificar la extensión de un resumen demasiado corto"""
        model = self.validator.parse_and_validate(self.short_summary)
        
        original_summary = "Junior developer."
        
        self.assertNotEqual(original_summary, model.summary.content)
        self.assertGreater(len(model.summary.content), 50)
    
    
    
    def test_validate_email(self):
        """Verificar la validación específica de emails"""
        self.assertTrue(self.validator.validate_email("test@example.com"))
        
        self.assertFalse(self.validator.validate_email("test.example.com"))
        self.assertFalse(self.validator.validate_email("test@"))
        self.assertFalse(self.validator.validate_email("@example.com"))
    
    def test_validate_phone(self):
        """Verificar la validación específica de teléfonos"""
        self.assertTrue(self.validator.validate_phone("(123) 456-7890"))
        self.assertTrue(self.validator.validate_phone("+1-123-456-7890"))
        self.assertTrue(self.validator.validate_phone("1234567890"))
        
        self.assertFalse(self.validator.validate_phone("123"))
        self.assertFalse(self.validator.validate_phone("abc-def-ghij"))
    
    def test_validate_url(self):
        """Verificar la validación específica de URLs"""
        self.assertTrue(self.validator.validate_url("https://example.com"))
        self.assertTrue(self.validator.validate_url("http://example.com/path"))
        self.assertTrue(self.validator.validate_url("https://www.example.co.uk/path?query=value"))
        
        self.assertFalse(self.validator.validate_url("example.com"))
        self.assertFalse(self.validator.validate_url("https://"))
        self.assertFalse(self.validator.validate_url("not a url"))
    
    def test_validate_summary(self):
        """Verificar la validación de longitud del resumen"""
        long_summary = "This is a detailed summary with more than fifty characters to test the validation logic."
        self.assertTrue(self.validator.validate_summary(long_summary))
        
        short_summary = "Too short summary."
        self.assertFalse(self.validator.validate_summary(short_summary))

if __name__ == "__main__":
    unittest.main()