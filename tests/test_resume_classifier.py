import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_classifier import ResumeClassifier

class TestResumeClassifier(unittest.TestCase):
    
    def setUp(self):
        self.classifier = ResumeClassifier()
        self.temp_dir = tempfile.mkdtemp()
        
        self.complete_resume = """
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
        
        self.incomplete_resume = """
        JANE DOE
        
        EDUCATION
        Bachelor of Arts in Graphic Design
        
        WORK EXPERIENCE
        Freelance Designer, 2020-Present
        
        SKILLS
        Design: Adobe Creative Suite
        """
        
        self.minimal_resume = """
        ROBERT JOHNSON
        
        SKILLS
        Basic programming knowledge
        """
        
        self.complete_path = os.path.join(self.temp_dir, "complete_resume.txt")
        with open(self.complete_path, 'w') as f:
            f.write(self.complete_resume)
            
        self.incomplete_path = os.path.join(self.temp_dir, "incomplete_resume.txt")
        with open(self.incomplete_path, 'w') as f:
            f.write(self.incomplete_resume)
            
        self.minimal_path = os.path.join(self.temp_dir, "minimal_resume.txt")
        with open(self.minimal_path, 'w') as f:
            f.write(self.minimal_resume)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_transform_info_to_tokens_complete(self):
        info = {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "phone": "(123) 456-7890",
            "education": "Bachelor of Science in Computer Science",
            "work_experience": "Software Engineer at Tech Company",
            "projects": "E-commerce Platform",
            "activities": "Hackathon participant",
            "skills": "Python, JavaScript, Java"
        }
        
        tokens = self.classifier.transform_info_to_tokens(info)
        
        self.assertIn("name", tokens)
        self.assertIn("email", tokens)
        self.assertIn("phone", tokens)
        self.assertIn("education", tokens)
        self.assertIn("work_experience", tokens)
        self.assertIn("projects_activities", tokens)
        self.assertIn("skills", tokens)
        
        self.assertNotIn("missing_name", tokens)
        self.assertNotIn("missing_email", tokens)
        
    def test_transform_info_to_tokens_incomplete(self):
        info = {
            "name": "Jane Doe",
            "email": "example@email.com",
            "phone": "+1-234-567-8901",
            "education": "Bachelor of Arts in Graphic Design",
            "work_experience": "Freelance Designer",
            "projects": "None",
            "activities": "None",
            "skills": "Design: Adobe Creative Suite"
        }
        
        tokens = self.classifier.transform_info_to_tokens(info)
        
        self.assertIn("name", tokens)
        self.assertIn("missing_email", tokens)
        self.assertIn("missing_phone", tokens)
        self.assertIn("education", tokens)
        self.assertIn("work_experience", tokens)
        self.assertIn("projects_activities", tokens)
        self.assertIn("skills", tokens)
        
    def test_classify_complete_resume(self):
        classification = self.classifier.classify_resume(self.complete_path, "Software Engineer")
        self.assertEqual("REJECTED", classification)
        
    def test_classify_incomplete_resume(self):
        classification = self.classifier.classify_resume(self.incomplete_path, "Web Developer")
        self.assertEqual("REJECTED", classification)
        
    def test_classify_minimal_resume(self):
        classification = self.classifier.classify_resume(self.minimal_path, "Software Engineer")
        self.assertEqual("REJECTED", classification)
        
    def test_dfa_transitions(self):
        tokens = ["name", "email", "phone", "education", "work_experience", "projects_activities", "skills"]
        
        current_state = self.classifier.dfa.start_state
        for token in tokens:
            next_states = self.classifier.dfa._transition_function(current_state, token)
            self.assertTrue(next_states, f"No hay transición para {token} desde {current_state}")
            current_state = next_states.pop()
            
        self.assertEqual('q7', current_state)
        self.assertEqual('HIGHLY QUALIFIED', self.classifier.dictionary[current_state])
        
        tokens = ["missing_name"]
        
        current_state = self.classifier.dfa.start_state
        for token in tokens:
            next_states = self.classifier.dfa._transition_function(current_state, token)
            self.assertTrue(next_states, f"No hay transición para {token} desde {current_state}")
            current_state = next_states.pop()
            
        self.assertEqual('q8', current_state)
        self.assertEqual('REJECTED', self.classifier.dictionary[current_state])

if __name__ == "__main__":
    unittest.main()