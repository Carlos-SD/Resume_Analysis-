from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from collections import defaultdict
import re

class ResumeRanker:
    def __init__(self):
        # Definición de pesos para diferentes componentes del CV
        self.component_weights = {
            "education": 0.2,  # 20% de la puntuación
            "work_experience": 0.3,  # 30% de la puntuación
            "projects": 0.15,  # 15% de la puntuación
            "skills": 0.35,    # 35% de la puntuación
        }
        
        # Definición de las habilidades relevantes por rol y sus pesos (keywords)
        self.skills_by_role = {
            "Data Scientist": {
                "python": 0.15, "r": 0.1, "machine learning": 0.2, "deep learning": 0.15,
                "data analysis": 0.15, "statistics": 0.1, "sql": 0.08, "pandas": 0.07
            },
            "AI Engineer": {
                "python": 0.12, "tensorflow": 0.15, "pytorch": 0.15, "computer vision": 0.12,
                "nlp": 0.12, "deep learning": 0.15, "reinforcement learning": 0.1, "algorithms": 0.09
            },
            "Software Engineer": {
                "java": 0.12, "c++": 0.12, "python": 0.1, "algorithms": 0.12,
                "data structures": 0.12, "oop": 0.1, "git": 0.08, "software design": 0.1, "testing": 0.08
            },
            "Web Developer": {
                "html": 0.1, "css": 0.1, "javascript": 0.15, "react": 0.12,
                "node.js": 0.12, "database": 0.1, "responsive design": 0.08, "api": 0.08, "git": 0.05
            },
            "DevOps Engineer": {
                "linux": 0.1, "docker": 0.15, "kubernetes": 0.15, "ci/cd": 0.12,
                "cloud": 0.12, "aws": 0.1, "infrastructure as code": 0.08, "monitoring": 0.08, "scripting": 0.05
            }
        }
        
        # Palabras clave para experiencia laboral por rol
        self.experience_keywords = {
            "Data Scientist": ["data analysis", "machine learning", "modeling", "statistics", "research"],
            "AI Engineer": ["machine learning", "deep learning", "neural networks", "model deployment", "research"],
            "Software Engineer": ["software development", "application", "backend", "frontend", "architecture"],
            "Web Developer": ["frontend", "backend", "web application", "ui", "responsive", "user interface"],
            "DevOps Engineer": ["infrastructure", "deployment", "pipeline", "monitoring", "automation"]
        }
        
        # FST para evaluar experiencia (simplificado como un DFA con salidas)
        self.experience_fst_states = {
            'start': {'junior': ('mid', 0.5), 'intern': ('entry', 0.3), 'senior': ('senior', 1.0), '': ('entry', 0.3)},
            'entry': {'year': ('entry_years', 0.0)},
            'entry_years': {'1': ('complete', 0.4), '2': ('complete', 0.5), '3+': ('complete', 0.6)},
            'mid': {'year': ('mid_years', 0.0)},
            'mid_years': {'1': ('complete', 0.6), '2': ('complete', 0.7), '3+': ('complete', 0.8)},
            'senior': {'year': ('senior_years', 0.0)},
            'senior_years': {'1': ('complete', 0.8), '2': ('complete', 0.9), '3+': ('complete', 1.0)},
            'complete': {}  # Estado final
        }
        
    def extract_experience_level(self, experience_text):
        """Extrae el nivel de experiencia usando FST simplificado"""
        # Determina nivel básico basado en palabras clave
        level = ''
        years = '1'  # Por defecto
        
        # Detecta nivel
        if re.search(r'\b(senior|lead|principal)\b', experience_text, re.IGNORECASE):
            level = 'senior'
        elif re.search(r'\b(mid|intermediate)\b', experience_text, re.IGNORECASE):
            level = 'mid'
        elif re.search(r'\b(junior|entry(-|\s)?level)\b', experience_text, re.IGNORECASE):
            level = 'junior'
        elif re.search(r'\b(intern|internship)\b', experience_text, re.IGNORECASE):
            level = 'intern'
            
        # Detecta años
        year_match = re.search(r'(\d+)[\+]?\s*(year|yr)', experience_text, re.IGNORECASE)
        if year_match:
            year_num = int(year_match.group(1))
            if year_num >= 3:
                years = '3+'
            else:
                years = str(year_num)
            
        # Procesa a través del FST
        state = 'start'
        score = 0.0
        
        # Primera transición - nivel
        if level in self.experience_fst_states[state]:
            state, level_score = self.experience_fst_states[state][level]
            score = level_score
        else:
            state, level_score = self.experience_fst_states[state]['']
            score = level_score
            
        # Segunda transición - years
        if state in ['entry', 'mid', 'senior']:
            state, _ = self.experience_fst_states[state]['year']
            
            # Tercera transición - número de años
            if years in self.experience_fst_states[state]:
                state, years_score = self.experience_fst_states[state][years]
                score = max(score, years_score)  # Tomamos el mayor score
            else:
                state, years_score = self.experience_fst_states[state]['1']
                score = max(score, years_score)
                
        return score
        
    def calculate_skill_score(self, skills_text, role):
        """Calcula puntuación de habilidades basada en keywords para el rol"""
        if role not in self.skills_by_role:
            return 0.0
            
        score = 0.0
        max_possible_score = 0.0
        skills_text = skills_text.lower()
        
        # Suma todos los pesos posibles para normalizar
        for keyword, weight in self.skills_by_role[role].items():
            max_possible_score += weight
            
            # Busca la habilidad en el texto
            if re.search(r'\b' + re.escape(keyword) + r'\b', skills_text, re.IGNORECASE):
                score += weight
                
        # Normaliza la puntuación
        if max_possible_score > 0:
            return score / max_possible_score
        return 0.0
        
    def calculate_experience_relevance(self, experience_text, role):
        """Calcula relevancia de la experiencia para el rol específico"""
        if role not in self.experience_keywords:
            return 0.0
            
        relevance_score = 0.0
        keywords = self.experience_keywords[role]
        
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', experience_text, re.IGNORECASE):
                relevance_score += 1.0 / len(keywords)
                
        # Combina relevancia con nivel de experiencia
        experience_level_score = self.extract_experience_level(experience_text)
        combined_score = 0.6 * relevance_score + 0.4 * experience_level_score
        
        return combined_score
        
    def calculate_education_score(self, education_text):
        """Calcula puntuación de educación"""
        score = 0.5  # Puntuación base
        
        # Detecta nivel educativo
        if re.search(r'\b(phd|doctor|doctorate)\b', education_text, re.IGNORECASE):
            score = 1.0
        elif re.search(r'\b(master|msc|ms|ma|mba)\b', education_text, re.IGNORECASE):
            score = 0.85
        elif re.search(r'\b(bachelor|bsc|bs|ba)\b', education_text, re.IGNORECASE):
            score = 0.7
        elif re.search(r'\b(associate|diploma)\b', education_text, re.IGNORECASE):
            score = 0.6
        
        # Bonus por universidad prestigiosa (podría expandirse)
        if re.search(r'\b(harvard|mit|stanford|berkeley|cambridge|oxford)\b', education_text, re.IGNORECASE):
            score += 0.1
            
        return min(score, 1.0)  # Máximo 1.0
        
    def calculate_projects_score(self, projects_text, role):
        """Calcula puntuación de proyectos basada en relevancia para el rol"""
        if not projects_text or projects_text == "None\n":
            return 0.0
            
        # Utiliza las mismas keywords que para experiencia
        if role in self.experience_keywords:
            keywords = self.experience_keywords[role]
            score = 0.0
            
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', projects_text, re.IGNORECASE):
                    score += 1.0 / len(keywords)
                    
            return score
        return 0.5  # Score por defecto
        
    def rank_resume(self, resume_info, role):
        """Función principal para puntuar un CV usando FST"""
        if not resume_info or not role:
            return {"score": 0.0, "ranking": "Not Qualified", "details": {}}
            
        # Obtiene los componentes del CV
        education = resume_info.get('education', "None\n")
        work_experience = resume_info.get('work_experience', "None\n")
        projects = resume_info.get('projects', "None\n")
        skills = resume_info.get('skills', "None\n")
        
        # Calcula puntuaciones por componente
        education_score = self.calculate_education_score(education)
        experience_score = self.calculate_experience_relevance(work_experience, role)
        projects_score = self.calculate_projects_score(projects, role)
        skills_score = self.calculate_skill_score(skills, role)
        
        # Calcula puntuación ponderada total
        total_score = (
            self.component_weights["education"] * education_score +
            self.component_weights["work_experience"] * experience_score +
            self.component_weights["projects"] * projects_score +
            self.component_weights["skills"] * skills_score
        )
        
        # Determina ranking basado en la puntuación
        ranking = "Not Qualified"
        if total_score >= 0.8:
            ranking = "Highly Qualified"
        elif total_score >= 0.6:
            ranking = "Qualified"
        elif total_score >= 0.4:
            ranking = "Potentially Qualified"
            
        # Detalles para explicabilidad
        details = {
            "education": {
                "score": round(education_score, 2),
                "weight": self.component_weights["education"],
                "weighted_score": round(education_score * self.component_weights["education"], 2)
            },
            "experience": {
                "score": round(experience_score, 2),
                "weight": self.component_weights["work_experience"],
                "weighted_score": round(experience_score * self.component_weights["work_experience"], 2)
            },
            "projects": {
                "score": round(projects_score, 2),
                "weight": self.component_weights["projects"],
                "weighted_score": round(projects_score * self.component_weights["projects"], 2)
            },
            "skills": {
                "score": round(skills_score, 2),
                "weight": self.component_weights["skills"],
                "weighted_score": round(skills_score * self.component_weights["skills"], 2)
            }
        }
        
        return {
            "score": round(total_score, 2),
            "ranking": ranking,
            "details": details
        } 