from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from collections import defaultdict
import re

class FiniteStateTransducer:
    """
    Implementación formal de un Transductor de Estado Finito (FST).
    Mapea secuencias de símbolos de entrada a secuencias de símbolos de salida.
    """
    def __init__(self):
        # Conjunto de estados
        self.states = set()
        # Símbolos de entrada
        self.input_symbols = set()
        # Símbolos de salida
        self.output_symbols = set()
        # Estado inicial
        self.initial_state = None
        # Estados finales
        self.final_states = set()
        # Función de transición: (estado_actual, símbolo_entrada) -> [(estado_siguiente, símbolo_salida)]
        self.transitions = {}
        
    def add_state(self, state):
        """Añadir un estado al FST"""
        self.states.add(state)
        return self
        
    def add_states(self, states):
        """Añadir múltiples estados al FST"""
        for state in states:
            self.add_state(state)
        return self
        
    def set_initial_state(self, state):
        """Establecer el estado inicial"""
        if state not in self.states:
            self.add_state(state)
        self.initial_state = state
        return self
        
    def add_final_state(self, state):
        """Añadir un estado final"""
        if state not in self.states:
            self.add_state(state)
        self.final_states.add(state)
        return self
        
    def add_transition(self, from_state, input_symbol, to_state, output_symbol):
        """Añadir una transición al FST"""
        if from_state not in self.states:
            self.add_state(from_state)
        if to_state not in self.states:
            self.add_state(to_state)
            
        self.input_symbols.add(input_symbol)
        self.output_symbols.add(output_symbol)
        
        # Crear el diccionario para el estado si no existe
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
            
        # Crear la lista para la entrada si no existe
        if input_symbol not in self.transitions[from_state]:
            self.transitions[from_state][input_symbol] = []
            
        # Añadir la transición
        self.transitions[from_state][input_symbol].append((to_state, output_symbol))
        return self
        
    def process(self, input_sequence):
        """
        Procesa una secuencia de entrada y retorna todas las posibles secuencias de salida
        junto con el estado final alcanzado.
        """
        # Si no hay estado inicial, no podemos procesar
        if self.initial_state is None:
            return []
            
        # Lista de configuraciones: (estado actual, salida acumulada)
        configurations = [(self.initial_state, [])]
        
        # Para cada símbolo de entrada
        for input_symbol in input_sequence:
            new_configurations = []
            
            # Para cada configuración actual
            for current_state, output_sequence in configurations:
                # Si el estado actual tiene transiciones para este símbolo
                if current_state in self.transitions and input_symbol in self.transitions[current_state]:
                    # Obtener todas las transiciones posibles
                    for next_state, output_symbol in self.transitions[current_state][input_symbol]:
                        # Añadir nueva configuración con la salida acumulada
                        new_output = output_sequence + [output_symbol]
                        new_configurations.append((next_state, new_output))
                
            # Actualizar configuraciones
            configurations = new_configurations
            
            # Si no hay configuraciones, no hay camino válido
            if not configurations:
                return []
                
        # Filtrar solo las configuraciones que terminan en estados finales
        final_configurations = [(state, output) for state, output in configurations if state in self.final_states]
        
        return final_configurations

class ResumeRanker:
    def __init__(self):
        self.component_weights = {
            "education": 0.2,
            "work_experience": 0.3,
            "projects": 0.15,
            "skills": 0.35, 
        }
        
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
        
        self.experience_keywords = {
            "Data Scientist": ["data analysis", "machine learning", "modeling", "statistics", "research"],
            "AI Engineer": ["machine learning", "deep learning", "neural networks", "model deployment", "research"],
            "Software Engineer": ["software development", "application", "backend", "frontend", "architecture"],
            "Web Developer": ["frontend", "backend", "web application", "ui", "responsive", "user interface"],
            "DevOps Engineer": ["infrastructure", "deployment", "pipeline", "monitoring", "automation"]
        }
        
        # Crear FST para evaluar la experiencia
        self.experience_fst = self._build_experience_fst()
        
        # Crear FST para evaluar las habilidades por rol
        self.skills_fst = {}
        for role in self.skills_by_role:
            self.skills_fst[role] = self._build_skills_fst(role)
        
    def _build_experience_fst(self):
        """
        Construye un FST formal para evaluar el nivel de experiencia.
        Este FST mapea características de experiencia a puntuaciones.
        """
        fst = FiniteStateTransducer()
        
        # Definir estados
        fst.add_states(["start", "entry", "mid", "senior", 
                        "entry_years", "mid_years", "senior_years", 
                        "complete"])
        
        # Estado inicial
        fst.set_initial_state("start")
        
        # Estado final
        fst.add_final_state("complete")
        
        # Transiciones
        # Desde estado inicial
        fst.add_transition("start", "junior", "entry", "0.3")
        fst.add_transition("start", "intern", "entry", "0.2")
        fst.add_transition("start", "entry", "entry", "0.3")
        fst.add_transition("start", "mid", "mid", "0.5")
        fst.add_transition("start", "senior", "senior", "0.7")
        fst.add_transition("start", "lead", "senior", "0.8")
        fst.add_transition("start", "principal", "senior", "0.9")
        fst.add_transition("start", "other", "entry", "0.3")
        
        # Transiciones basadas en años
        for state, base_score in [("entry", "0.3"), ("mid", "0.5"), ("senior", "0.7")]:
            fst.add_transition(state, "years", f"{state}_years", "0.0")
        
        # Transiciones basadas en número específico de años
        year_scores = {
            "entry_years": {"1": "0.4", "2": "0.5", "3": "0.6", "4": "0.65", "5+": "0.7"},
            "mid_years": {"1": "0.6", "2": "0.7", "3": "0.75", "4": "0.8", "5+": "0.85"},
            "senior_years": {"1": "0.8", "2": "0.85", "3": "0.9", "4": "0.95", "5+": "1.0"}
        }
        
        for state, scores in year_scores.items():
            for years, score in scores.items():
                fst.add_transition(state, years, "complete", score)
        
        return fst
    
    def _build_skills_fst(self, role):
        """
        Construye un FST formal para evaluar habilidades específicas por rol.
        Este FST mapea habilidades mencionadas a puntuaciones.
        """
        fst = FiniteStateTransducer()
        
        # Definir estados
        states = ["start", "scored"]
        for skill in self.skills_by_role[role]:
            states.append(f"has_{skill.replace(' ', '_')}")
        
        fst.add_states(states)
        
        # Estado inicial
        fst.set_initial_state("start")
        
        # Estado final
        fst.add_final_state("scored")
        
        # Para cada habilidad, añadir una transición desde start
        total_possible_score = sum(self.skills_by_role[role].values())
        
        for skill, weight in self.skills_by_role[role].items():
            skill_state = f"has_{skill.replace(' ', '_')}"
            score = str(round(weight / total_possible_score, 2))
            fst.add_transition("start", skill, skill_state, score)
            fst.add_transition(skill_state, "end", "scored", "0.0")
        
        return fst
        
    def extract_experience_level(self, experience_text):
        """
        Extrae el nivel de experiencia usando un FST formal
        """
        input_sequence = []
        
        # Determinar nivel de experiencia basado en palabras clave
        if re.search(r'\b(senior|lead|principal|director|head|chief|architect)\b', experience_text, re.IGNORECASE):
            if re.search(r'\b(chief|director|head)\b', experience_text, re.IGNORECASE):
                input_sequence.append("principal")
            elif re.search(r'\b(lead|architect)\b', experience_text, re.IGNORECASE):
                input_sequence.append("lead")
            else:
                input_sequence.append("senior")
        elif re.search(r'\b(mid|intermediate|associate)\b', experience_text, re.IGNORECASE):
            input_sequence.append("mid")
        elif re.search(r'\b(junior|entry|intern|trainee|recent graduate)\b', experience_text, re.IGNORECASE):
            if re.search(r'\b(intern|trainee)\b', experience_text, re.IGNORECASE):
                input_sequence.append("intern")
            else:
                input_sequence.append("junior")
        else:
            # Determinar por los años de experiencia
            year_matches = re.findall(r'(\d+)[\+]?\s*(?:year|yr)s?', experience_text, re.IGNORECASE)
            if year_matches:
                years = max([int(y) for y in year_matches])
                if years > 8:
                    input_sequence.append("senior")
                elif years > 3:
                    input_sequence.append("mid")
                elif years > 0:
                    input_sequence.append("junior")
                else:
                    input_sequence.append("other")
            else:
                input_sequence.append("other")
        
        # Añadir información sobre años
        input_sequence.append("years")
        
        year_matches = re.findall(r'(\d+)[\+]?\s*(?:year|yr)s?', experience_text, re.IGNORECASE)
        if year_matches:
            years = max([int(y) for y in year_matches])
            if years > 5:
                input_sequence.append("5+")
            else:
                input_sequence.append(str(years))
        else:
            # Estimar años por número de posiciones
            positions = len(re.findall(r'\b(position|title|role|job|company)s?\b', experience_text, re.IGNORECASE))
            if positions > 3:
                input_sequence.append("5+")
            elif positions > 1:
                input_sequence.append("3")
            elif positions > 0:
                input_sequence.append("1")
            else:
                input_sequence.append("1")
        
        # Procesar mediante FST para obtener puntuación
        results = self.experience_fst.process(input_sequence)
        
        if not results:
            return 0.3  # Valor por defecto si no hay resultados
            
        # Tomar la puntuación más alta
        best_score = max([float(output[-1]) for _, output in results])
        return best_score
        
    def calculate_skill_score(self, skills_text, role):
        """
        Calcula una puntuación basada en las habilidades mencionadas respecto al rol.
        Utiliza un enfoque basado en autómatas finitos para la evaluación.
        """
        if role not in self.skills_by_role:
            return 0.5  # Valor por defecto si el rol no está definido
            
        # Preprocesar el texto para mayor precisión
        skills_text = skills_text.lower()
        
        # Reemplazar símbolos comunes y normalizar
        skills_text = re.sub(r'[^\w\s]', ' ', skills_text)
        skills_text = re.sub(r'\s+', ' ', skills_text)
        
        # Tokenizar el texto de habilidades
        tokens = skills_text.split()
        
        # Detectar n-gramas que coincidan con habilidades relevantes
        found_skills = set()
        total_weight = 0
        
        # Primero buscar n-gramas más largos (máximo 3 palabras)
        for skill in sorted(self.skills_by_role[role].keys(), key=lambda x: len(x.split()), reverse=True):
            skill_terms = skill.split()
            skill_len = len(skill_terms)
            
            if skill_len > 1:
                # Buscar n-gramas
                for i in range(len(tokens) - skill_len + 1):
                    ngram = ' '.join(tokens[i:i+skill_len])
                    if skill in ngram or ngram in skill:
                        found_skills.add(skill)
                        total_weight += self.skills_by_role[role][skill]
                        break
            else:
                # Buscar términos individuales
                if skill in tokens or any(skill in token for token in tokens):
                    found_skills.add(skill)
                    total_weight += self.skills_by_role[role][skill]
        
        # Calcular puntuación
        max_possible_weight = sum(self.skills_by_role[role].values())
        skill_score = total_weight / max_possible_weight if max_possible_weight > 0 else 0
        
        # Bonificación por cobertura de habilidades
        coverage = len(found_skills) / len(self.skills_by_role[role])
        coverage_bonus = min(coverage * 0.2, 0.2)  # Máximo 20% de bonificación
        
        # Bonificación por mencionar frameworks/herramientas específicas
        framework_bonus = 0
        framework_patterns = [
            r'\b(framework|library|tool|platform|environment)\b',
            r'\b(react|angular|vue|django|flask|spring|laravel|express)\b',
            r'\b(tensorflow|pytorch|scikit-learn|pandas|numpy)\b', 
            r'\b(kubernetes|docker|aws|azure|gcp)\b'
        ]
        
        for pattern in framework_patterns:
            if re.search(pattern, skills_text, re.IGNORECASE):
                framework_bonus += 0.05
                
        framework_bonus = min(framework_bonus, 0.15)  # Máximo 15% de bonificación
        
        final_score = min(skill_score + coverage_bonus + framework_bonus, 1.0)
        return final_score
        
    def calculate_experience_relevance(self, experience_text, role):
        """
        Calcula la relevancia de la experiencia para un rol específico.
        Evalúa tanto el nivel de experiencia como la relevancia temática.
        """
        if not experience_text or experience_text == "None\n":
            return 0.2
        
        # Obtener nivel de experiencia usando FST
        experience_level = self.extract_experience_level(experience_text)
        
        # Calcular relevancia temática
        relevance_score = 0.0
        max_relevance = 0.0
        
        # Analizar la relevancia basada en palabras clave del rol
        if role in self.experience_keywords:
            for keyword in self.experience_keywords[role]:
                weight = 1.0 / len(self.experience_keywords[role])
                max_relevance += weight
                if re.search(r'\b' + re.escape(keyword) + r'\b', experience_text, re.IGNORECASE):
                    relevance_score += weight
        
        # Normalizar la relevancia
        normalized_relevance = relevance_score / max_relevance if max_relevance > 0 else 0.5
        
        # Evaluar antigüedad y diversidad de experiencia
        diversity_score = 0.0
        
        # Contar diferentes roles o posiciones
        roles_count = len(re.findall(r'\b(position|title|role|job)\b', experience_text, re.IGNORECASE))
        if roles_count > 3:
            diversity_score = 0.2
        elif roles_count > 1:
            diversity_score = 0.1
        
        # Contar diferentes empresas
        companies_count = len(re.findall(r'\b(company|organization|employer|firm|inc|llc)\b', experience_text, re.IGNORECASE))
        if companies_count > 2:
            diversity_score += 0.1
        
        # Bonificación por experiencia reciente
        recency_bonus = 0.0
        if re.search(r'\b(current|present|now|today|ongoing)\b', experience_text, re.IGNORECASE):
            recency_bonus = 0.1
            
        # Combinar todas las puntuaciones con pesos apropiados
        final_score = (experience_level * 0.5) + (normalized_relevance * 0.3) + (diversity_score * 0.1) + recency_bonus
        
        return min(final_score, 1.0)
        
    def calculate_education_score(self, education_text):
        """
        Calcula una puntuación para la educación basada en nivel académico y relevancia.
        """
        if not education_text or education_text == "None\n":
            return 0.3
            
        education_score = 0.5  # Valor base
        
        # Bonificación por nivel académico
        if re.search(r'\b(PhD|Doctorate|Doctor|Ph\.D)\b', education_text, re.IGNORECASE):
            education_score = 1.0
        elif re.search(r'\b(Master|MS|M\.S|MBA|MSc|M\.Sc)\b', education_text, re.IGNORECASE):
            education_score = 0.9
        elif re.search(r'\b(Bachelor|BS|B\.S|BA|B\.A|BSc|B\.Sc)\b', education_text, re.IGNORECASE):
            education_score = 0.8
        elif re.search(r'\b(Associate|Diploma|Certificate|Certification)\b', education_text, re.IGNORECASE):
            education_score = 0.6
            
        # Bonificación por relevancia del campo
        relevance_bonus = 0.0
        tech_fields = [
            r'\b(Computer Science|Computer Engineering|Software Engineering)\b',
            r'\b(Information Technology|Information Systems|Software Development)\b',
            r'\b(Data Science|Artificial Intelligence|Machine Learning|Statistics)\b',
            r'\b(Engineering|Mathematics|Physics|Cybersecurity|Network)\b'
        ]
        
        for field_pattern in tech_fields:
            if re.search(field_pattern, education_text, re.IGNORECASE):
                relevance_bonus = 0.1
                break
                
        # Bonificación por prestigio académico
        prestige_bonus = 0.0
        prestigious_institutions = [
            r'\b(MIT|Stanford|Harvard|Berkeley|CMU|Carnegie Mellon)\b',
            r'\b(Oxford|Cambridge|ETH|Imperial College|CalTech)\b',
            r'\b(University of California|University of Michigan|Georgia Tech)\b',
            r'\b(Princeton|Yale|Columbia|Cornell|University of Pennsylvania)\b'
        ]
        
        for institution_pattern in prestigious_institutions:
            if re.search(institution_pattern, education_text, re.IGNORECASE):
                prestige_bonus = 0.05
                break
                
        # Bonificación por distinciones
        honors_bonus = 0.0
        if re.search(r'\b(honors|distinction|summa cum laude|magna cum laude|cum laude|first class|merit)\b', 
                     education_text, re.IGNORECASE):
            honors_bonus = 0.05
            
        final_score = min(education_score + relevance_bonus + prestige_bonus + honors_bonus, 1.0)
        return final_score
        
    def calculate_projects_score(self, projects_text, role):
        """
        Evalúa los proyectos del candidato en función de su complejidad y relevancia.
        """
        if not projects_text or projects_text == "None\n":
            return 0.3
            
        base_score = 0.5
        
        # Evaluar relevancia temática para el rol
        relevance_score = 0.0
        if role in self.experience_keywords:
            keywords_count = 0
            for keyword in self.experience_keywords[role]:
                if re.search(r'\b' + re.escape(keyword) + r'\b', projects_text, re.IGNORECASE):
                    keywords_count += 1
                    
            relevance_score = min(0.2, (keywords_count / len(self.experience_keywords[role])) * 0.2)
            
        # Evaluar complejidad de los proyectos
        complexity_score = 0.0
        
        # Indicadores de complejidad técnica
        tech_complexity_indicators = [
            r'\b(architecture|system design|scalable|performance|optimization|algorithm)\b',
            r'\b(database|cloud|infrastructure|distributed|concurrent|parallel)\b',
            r'\b(framework|library|api|service|integration|deployment)\b'
        ]
        
        for indicator in tech_complexity_indicators:
            if re.search(indicator, projects_text, re.IGNORECASE):
                complexity_score += 0.05
                
        complexity_score = min(complexity_score, 0.2)
        
        # Evaluar cantidad de proyectos
        project_count_score = 0.0
        project_count = len(re.findall(r'(?:^|\n)(?:\*|\-|\d+\.|\w+:)', projects_text))
        
        if project_count > 3:
            project_count_score = 0.1
        elif project_count > 1:
            project_count_score = 0.05
            
        # Bonificación por proyectos destacados
        achievement_bonus = 0.0
        achievement_indicators = [
            r'\b(award|recognition|published|featured|selected|competition|hackathon|winner)\b',
            r'\b(github|stars|fork|contribution|open source|community)\b',
            r'\b(deployed|production|users|customers|clients|impact|result)\b'
        ]
        
        for indicator in achievement_indicators:
            if re.search(indicator, projects_text, re.IGNORECASE):
                achievement_bonus += 0.025
                
        achievement_bonus = min(achievement_bonus, 0.1)
        
        # Calcular puntuación final
        final_score = min(base_score + relevance_score + complexity_score + project_count_score + achievement_bonus, 1.0)
        return final_score
        
    def rank_resume(self, resume_info, role):
        """
        Calcula una puntuación para un CV basado en sus componentes.
        Implementa un enfoque formal basado en autómatas para la evaluación.
        """
        education = resume_info.get('education', "None\n")
        work_experience = resume_info.get('work_experience', "None\n")
        projects = resume_info.get('projects', "None\n")
        skills = resume_info.get('skills', "None\n")
        
        # Calcular puntuaciones individuales
        education_score = self.calculate_education_score(education)
        experience_score = self.calculate_experience_relevance(work_experience, role)
        projects_score = self.calculate_projects_score(projects, role)
        skills_score = self.calculate_skill_score(skills, role)
        
        # Calcular puntuación total ponderada
        total_score = (
            self.component_weights["education"] * education_score +
            self.component_weights["work_experience"] * experience_score +
            self.component_weights["projects"] * projects_score +
            self.component_weights["skills"] * skills_score
        )
        
        # Determinar ranking basado en la puntuación
        ranking = "Not Qualified"
        if total_score >= 0.8:
            ranking = "Highly Qualified"
        elif total_score >= 0.6:
            ranking = "Qualified"
        elif total_score >= 0.4:
            ranking = "Potentially Qualified"
            
        # Preparar detalles de la evaluación
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