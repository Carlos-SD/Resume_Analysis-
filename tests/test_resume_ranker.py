import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_ranker import ResumeRanker

class TestResumeRanker(unittest.TestCase):
    
    def setUp(self):
        self.ranker = ResumeRanker()
        
        self.senior_experience = """
        Senior Software Engineer at Tech Corp
        2018-Present (5+ years)
        - Led a team of 5 developers building cloud-based applications
        - Architected and implemented microservices infrastructure
        - Mentored junior developers and conducted code reviews
        """
        
        self.junior_experience = """
        Junior Software Developer at StartUp Inc
        2023-Present (1 year)
        - Assisted in frontend development using React
        - Fixed bugs and implemented small features
        - Participated in team meetings and agile processes
        """
        
        self.irrelevant_experience = """
        Administrative Assistant at Office Corp
        2020-2023
        - Managed office schedules and appointments
        - Processed invoices and handled correspondence
        - Organized team events and maintained office supplies
        """
        
        self.data_science_skills = """
        Programming: Python, R
        Machine Learning: Neural Networks, Random Forests, SVM
        Data Analysis: Pandas, NumPy, SQL
        Tools: Jupyter, TensorFlow, PyTorch, Scikit-learn
        Statistics: Hypothesis Testing, Regression Analysis
        """
        
        self.web_dev_skills = """
        Frontend: HTML, CSS, JavaScript, React, Vue.js
        Backend: Node.js, Express, Django, Flask
        Databases: MongoDB, PostgreSQL, MySQL
        Tools: Git, Docker, AWS, Netlify
        Testing: Jest, Cypress, Selenium
        """
        
        self.general_skills = """
        Programming: Basic Python, HTML
        Tools: Microsoft Office, Google Suite
        Languages: English, Spanish
        Soft Skills: Communication, Teamwork
        """
        
        self.phd_education = """
        Ph.D. in Computer Science
        Stanford University, 2018-2022
        Thesis: "Advanced Algorithms for Natural Language Processing"
        """
        
        self.bachelor_education = """
        Bachelor of Science in Computer Engineering
        University of Michigan, 2016-2020
        GPA: 3.8/4.0
        """
        
        self.high_school_education = """
        High School Diploma
        Lincoln High School, 2016-2020
        """
    
    def test_extract_experience_level_junior(self):
        """Verificar la extracción del nivel de experiencia junior"""
        score = self.ranker.extract_experience_level(self.junior_experience)
        self.assertLessEqual(score, 0.6, "La puntuación de experiencia junior debe ser moderada")
        
    def test_calculate_skill_score_relevant(self):
        """Verificar el cálculo de puntuación de habilidades relevantes"""
        score = self.ranker.calculate_skill_score(self.data_science_skills, "Data Scientist")
        self.assertGreaterEqual(score, 0.7, "La puntuación para habilidades relevantes debe ser alta")
        
    def test_calculate_skill_score_irrelevant(self):
        """Verificar el cálculo de puntuación de habilidades irrelevantes"""
        score = self.ranker.calculate_skill_score(self.data_science_skills, "Web Developer")
        self.assertLessEqual(score, 0.5, "La puntuación para habilidades irrelevantes debe ser baja")
        
    def test_calculate_skill_score_general(self):
        """Verificar el cálculo de puntuación de habilidades generales"""
        score = self.ranker.calculate_skill_score(self.general_skills, "Data Scientist")
        self.assertLessEqual(score, 0.3, "La puntuación para habilidades generales debe ser baja")
        
    
    def test_calculate_experience_relevance_mismatched(self):
        """Verificar la relevancia de experiencia no coincidente con el rol"""
        score = self.ranker.calculate_experience_relevance(self.irrelevant_experience, "Data Scientist")
        self.assertLessEqual(score, 0.3, "La puntuación para experiencia irrelevante debe ser baja")
        
    def test_calculate_education_score_phd(self):
        """Verificar la puntuación de educación para un PhD"""
        score = self.ranker.calculate_education_score(self.phd_education)
        self.assertGreaterEqual(score, 0.9, "La puntuación para un PhD debe ser muy alta")
        
    
    def test_calculate_education_score_high_school(self):
        """Verificar la puntuación de educación para educación secundaria"""
        score = self.ranker.calculate_education_score(self.high_school_education)
        self.assertLessEqual(score, 0.6, "La puntuación para educación secundaria debe ser baja")
        
     
    def test_rank_resume_average_candidate(self):
        """Verificar el ranking de un candidato promedio"""
        resume_info = {
            "education": self.bachelor_education,
            "work_experience": self.junior_experience,
            "projects": "Personal website, College projects",
            "skills": self.web_dev_skills
        }
        
        result = self.ranker.rank_resume(resume_info, "Web Developer")
        
        self.assertGreaterEqual(result["score"], 0.5, "La puntuación global debe ser moderada")
        self.assertLessEqual(result["score"], 0.8, "La puntuación global debe ser menor que un candidato ideal")
        
    def test_rank_resume_mismatched_candidate(self):
        """Verificar el ranking de un candidato con perfil no coincidente"""
        resume_info = {
            "education": self.high_school_education,
            "work_experience": self.irrelevant_experience,
            "projects": "None",
            "skills": self.general_skills
        }
        
        result = self.ranker.rank_resume(resume_info, "AI Engineer")
        
        self.assertLessEqual(result["score"], 0.4, "La puntuación global debe ser baja")
        self.assertEqual("Not Qualified", result["ranking"])
        
    def test_weighted_scoring(self):
        """Verificar que las puntuaciones ponderadas se calculan correctamente"""
        resume_info = {
            "education": "PhD in Computer Science",
            "work_experience": "Junior Developer",
            "projects": "Research project",
            "skills": "Python, Machine Learning"
        }
        
        result = self.ranker.rank_resume(resume_info, "Data Scientist")
        
        for component in ["education", "experience", "skills"]:
            self.assertIn("weight", result["details"][component])
            self.assertIn("weighted_score", result["details"][component])
            
            raw_score = result["details"][component]["score"]
            weight = result["details"][component]["weight"]
            weighted_score = result["details"][component]["weighted_score"]
            
            self.assertAlmostEqual(weighted_score, raw_score * weight, places=1)

if __name__ == "__main__":
    unittest.main()