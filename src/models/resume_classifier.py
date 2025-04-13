from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from . import resume_parser

class ResumeClassifier:

    def __init__(self):
        self.resume = resume_parser.ResumeParser()

        self.alphabet = {
            "name", "missing_name",
            "email", "missing_email",
            "phone", "missing_phone",
            "education", "missing_education",
            "work_experience", "missing_work_experience",
            "projects_activities", "missing_projects_activities",
            "skills", "missing_skills"
        }

        self.dfa = DeterministicFiniteAutomaton(
            states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'},
            input_symbols=self.alphabet,
            start_state='q0',
            final_states={'q7', 'q8', 'q9'}
        )

        self.dfa.add_transition('q0', "name", 'q1')
        self.dfa.add_transition('q0', "missing_name", 'q8')  
        
        self.dfa.add_transition('q1', "email", 'q2')
        self.dfa.add_transition('q1', "missing_email", 'q9')  
        
        self.dfa.add_transition('q2', "phone", 'q3')
        self.dfa.add_transition('q2', "missing_phone", 'q9') 
        
        self.dfa.add_transition('q3', "education", 'q4')
        self.dfa.add_transition('q3', "missing_education", 'q9') 
        
        self.dfa.add_transition('q4', "work_experience", 'q5')
        self.dfa.add_transition('q4', "missing_work_experience", 'q9')
        
        self.dfa.add_transition('q5', "projects_activities", 'q6')
        self.dfa.add_transition('q5', "missing_projects_activities", 'q9')
        
        self.dfa.add_transition('q6', "skills", 'q7')
        self.dfa.add_transition('q6', "missing_skills", 'q9')

        self.dictionary = {
        'q7': 'HIGHLY QUALIFIED',
        'q8': 'REJECTED',
        'q9': 'NEEDS REVIEW'
    }
        

    def transform_info_to_tokens(self, info):
         tokens = []
         tokens.append("name" if info.get("name") and info.get("name") != "John Doe" else "missing_name")
         tokens.append("email" if info.get("email") and info.get("email") != "example@email.com" else "missing_email")
         tokens.append("phone" if info.get("phone") and info.get("phone") != "+1-234-567-8901" else "missing_phone")
         tokens.append("education" if info.get("education") and info.get("education") != "Bachelor's Degree in Computer Science" else "missing_education")
         tokens.append("work_experience" if info.get("work_experience") and info.get("work_experience") != "Software Engineer with 2+ years of experience" else "missing_work_experience")
         
         has_projects = info.get("projects") and info.get("projects") != "Various projects developing software applications"
         has_activities = info.get("activities") and info.get("activities") != "Participation in professional development activities"
         if has_projects or has_activities:
             tokens.append("projects_activities")
         else:
             tokens.append("missing_projects_activities")
             
         default_skills = f"Skills relevant to"
         tokens.append("skills" if info.get("skills") and default_skills not in info.get("skills") else "missing_skills")
         
         return tokens

    def classify_resume(self, file_path, role):
        resume_text = self.resume.read_resume(file_path)
        info = self.resume.extract_resume_info(resume_text, role)
        tokens = self.transform_info_to_tokens(info)
        current_state = self.dfa.start_state
        for token in tokens:
            next_states = self.dfa._transition_function(current_state, token)
            if next_states:
                current_state = next_states.pop()
                if current_state in self.dictionary:
                    break
            else:
                current_state = None
                break
            
        classification = self.dictionary.get(current_state, "UNKNOWN")
        return classification
   