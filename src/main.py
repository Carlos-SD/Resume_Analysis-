import tkinter as tk
from tkinter import filedialog
import os
import sys
import random
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_classifier import ResumeClassifier
from src.models.resume_ranker import ResumeRanker
from src.models.resume_grammar import ResumeGrammarValidator
from src.config import regex_config
from data import sample_resumes

class Main:
    def __init__(self):
        self.file_path = None
        default_roles = ["Data Scientist", "AI Engineer", "Software Engineer", "Web Developer", "DevOps Engineer"]
        self.role = random.choice(default_roles)
        self.grammar_validator = ResumeGrammarValidator()

    def upload_resume(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(
            title="Select Resume File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx"),
                ("PDF Files", "*.pdf")
            ]
        )
        if not self.file_path:
            print("No file selected.")
            return None
        root.quit()
        return self.file_path

    def generate_summary_text(self, resume_info):
        """Genera el texto del resumen en el formato requerido por la gramática"""
        # Asegurar que todos los campos tengan valores válidos
        name = resume_info.get('name', '').strip() or "John Doe"
        if name == "None\n":
            name = "John Doe"
            
        email = resume_info.get('email', '').strip() or "example@email.com"
        if email == "None\n":
            email = "example@email.com"
            
        phone = resume_info.get('phone', '').strip() or "+1-234-567-8901"
        if phone == "None\n":
            phone = "+1-234-567-8901"
            
        location = resume_info.get('location', '').strip() or "New York, USA"
        if location == "None\n" or not location:
            location = "New York, USA"
            
        linkedin = resume_info.get('linkedin', '').strip() or "https://linkedin.com/in/example"
        if linkedin == "None\n" or not linkedin.startswith("http"):
            linkedin = "https://linkedin.com/in/example"
            
        portfolio = resume_info.get('portfolio', '').strip() or "https://example.com/portfolio"
        if portfolio == "None\n" or not portfolio.startswith("http"):
            portfolio = "https://example.com/portfolio"
            
        summary = resume_info.get('summary', '').strip() or "Professional with experience in relevant fields."
        if summary == "None\n" or len(summary) < 50:
            # Asegurar que el resumen tenga al menos 50 caracteres
            role_summaries = {
                "Data Scientist": "Data scientist with experience in machine learning, statistical analysis, and data visualization. Skilled in Python, R, and SQL with a focus on delivering data-driven insights.",
                "AI Engineer": "AI engineer specialized in developing machine learning models and intelligent systems. Proficient in neural networks, computer vision, and natural language processing.",
                "Software Engineer": "Software engineer with expertise in designing and developing robust applications. Experienced in object-oriented programming, algorithms, and software architecture.",
                "Web Developer": "Web developer skilled in creating responsive and user-friendly websites. Proficient in HTML, CSS, JavaScript, and modern frameworks for frontend and backend development.",
                "DevOps Engineer": "DevOps engineer focused on automation, continuous integration, and deployment pipelines. Experienced in containerization, cloud infrastructure, and monitoring systems."
            }
            summary = role_summaries.get(self.role, "Professional with extensive experience in relevant fields. Skilled in multiple technologies and methodologies applicable to the position.")
            
        # Formatear correctamente con saltos de línea exactos para coincidir con la gramática
        return f"""Personal Information:
{name}
{email}
{phone}
{location}
{linkedin}
{portfolio}

Summary:
{summary}"""

    def save_summary(self, html_content, markdown_content, resume_name):
        """Guarda los resúmenes generados en archivos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(resume_name))[0]
        
        output_dir = "output/summaries"
        os.makedirs(output_dir, exist_ok=True)
        
        html_path = os.path.join(output_dir, f"{base_name}_{timestamp}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        md_path = os.path.join(output_dir, f"{base_name}_{timestamp}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        return html_path, md_path

    def process_resume(self):
        resume_classifier = ResumeClassifier()
        resume_ranker = ResumeRanker()
        
        if self.file_path:
            print(f"\nProcessing resume: {self.file_path}\n")
            
            try:
                parser = resume_classifier.resume
                resume_text = parser.read_resume(self.file_path)
                resume_info = parser.extract_resume_info(resume_text, self.role)
                
                # Agregar información de ubicación y resumen si no se extrajo
                if 'location' not in resume_info:
                    resume_info['location'] = "Unknown"
                    
                if 'summary' not in resume_info:
                    # Generar un resumen básico basado en las habilidades y experiencia
                    skills = resume_info.get('skills', 'None\n').strip()
                    experience = resume_info.get('work_experience', 'None\n').strip()
                    
                    if skills != 'None' and len(skills) > 5:
                        resume_info['summary'] = f"Professional with skills in {skills}. {experience if experience != 'None' else ''}"
                    else:
                        resume_info['summary'] = f"Professional with experience in {self.role} related fields."
                
                classification = resume_classifier.classify_resume(self.file_path, self.role)
                print("Classification (using DFA):", classification)
                
                ranking_result = resume_ranker.rank_resume(resume_info, self.role)
                
                print("\n--- CV Ranking using FST ---")
                print(f"Score: {ranking_result['score']} - Ranking: {ranking_result['ranking']}")
                print("\nComponent Scores:")
                
                for component, details in ranking_result['details'].items():
                    print(f"  - {component.capitalize()}: {details['score']} (weighted: {details['weighted_score']})")
                
                print("\nRecommendation:")
                if ranking_result['ranking'] == "Highly Qualified":
                    print("- Este candidato es altamente cualificado para el puesto. Se recomienda proceder a entrevista.")
                elif ranking_result['ranking'] == "Qualified":
                    print("- Este candidato está cualificado para el puesto. Se recomienda revisar puntos específicos durante la entrevista.")
                elif ranking_result['ranking'] == "Potentially Qualified":
                    print("- Este candidato podría ser adecuado. Se recomienda una revisión adicional.")
                else:
                    print("- Este candidato no parece cumplir con los requisitos mínimos para el puesto.")
                    
                try:
                    summary_text = self.generate_summary_text(resume_info)
                    print("\nGenerating summary using grammar validator...")
                    model = self.grammar_validator.parse_and_validate(summary_text)
                    
                    # Generar visualizaciones
                    html_content = self.grammar_validator.generate_html(model)
                    markdown_content = self.grammar_validator.generate_markdown(model)
                    
                    # Crear directorio de salida si no existe
                    output_dir = "output/summaries"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Guardar resúmenes
                    html_path, md_path = self.save_summary(html_content, markdown_content, self.file_path)
                    
                    print("\n--- Resume Summary Generated ---")
                    print(f"HTML summary saved to: {html_path}")
                    print(f"Markdown summary saved to: {md_path}")
                    
                except Exception as e:
                    print(f"\nError generating summary: {str(e)}")
                    print("\nUsing fallback summary generation...")
                    
                    # Generar un resumen HTML básico como fallback
                    name = resume_info.get('name', '').strip() or "John Doe"
                    if name == "None\n": name = "John Doe"
                    
                    email = resume_info.get('email', '').strip() or "example@email.com"
                    if email == "None\n": email = "example@email.com"
                    
                    # Crear directorio de salida si no existe
                    output_dir = "output/summaries"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Crear un HTML básico
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    base_name = os.path.splitext(os.path.basename(self.file_path))[0]
                    fallback_path = os.path.join(output_dir, f"{base_name}_fallback_{timestamp}.html")
                    
                    with open(fallback_path, 'w', encoding='utf-8') as f:
                        f.write(f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Basic Resume Summary</title>
                            <style>
                                body {{ font-family: Arial; margin: 20px; }}
                                .container {{ max-width: 600px; margin: 0 auto; }}
                                h1 {{ color: #333; }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h1>Resume Summary (Fallback)</h1>
                                <p><strong>Name:</strong> {name}</p>
                                <p><strong>Email:</strong> {email}</p>
                                <p><strong>Score:</strong> {ranking_result['score']}</p>
                                <p><strong>Ranking:</strong> {ranking_result['ranking']}</p>
                            </div>
                        </body>
                        </html>
                        """)
                    
                    print(f"Fallback HTML summary saved to: {fallback_path}")
                    
            except Exception as e:
                print(f"Error processing resume: {str(e)}")
                
        else:
            print("No file to process.")

    def run(self):
        while True:
            print("\nWelcome to the Resume Parser App!\n")
            print("Please select an option:")
            print("1. Use a default resume file")
            print("2. Upload a resume file")
            print("3. Exit")
            option = input("Please select an option: ").strip()

            match option:
                case "1":
                    default_folder = "data/sample_resumes"
                    if not os.path.isdir(default_folder):
                        print("Default resumes folder not found.")
                        continue
                    
                    # Listar los CV disponibles
                    archives = os.listdir(default_folder)
                    if not archives:
                        print("No default resumes found in the folder.")
                        continue
                    
                    print("\nAvailable default resumes:")
                    for idx, archive in enumerate(archives, 1):
                        print(f"{idx}. {archive}")
                    
                    # Elegir un CV específico
                    try:
                        selection = input("\nEnter the number of the resume you want to use (or 'r' for random): ").strip()
                        
                        if selection.lower() == 'r':
                            selected_archive = random.choice(archives)
                        else:
                            selection_idx = int(selection) - 1
                            if 0 <= selection_idx < len(archives):
                                selected_archive = archives[selection_idx]
                            else:
                                print("Invalid selection. Using a random resume.")
                                selected_archive = random.choice(archives)
                    except (ValueError, IndexError):
                        print("Invalid input. Using a random resume.")
                        selected_archive = random.choice(archives)
                    
                    # Elegir el rol
                    valid_roles = list(regex_config.skills_regex.keys())
                    print("\nAvailable roles:")
                    for idx, role in enumerate(valid_roles, 1):
                        print(f"{idx}. {role}")
                    
                    try:
                        role_selection = input("\nEnter the number of the role (or 'r' for random): ").strip()
                        
                        if role_selection.lower() == 'r':
                            self.role = random.choice(valid_roles)
                        else:
                            role_idx = int(role_selection) - 1
                            if 0 <= role_idx < len(valid_roles):
                                self.role = valid_roles[role_idx]
                            else:
                                print("Invalid selection. Using a random role.")
                                self.role = random.choice(valid_roles)
                    except (ValueError, IndexError):
                        print("Invalid input. Using a random role.")
                        self.role = random.choice(valid_roles)
                    
                    self.file_path = os.path.join(default_folder, selected_archive)
                    print(f"\nSelected resume: {selected_archive}")
                    print(f"Selected role: {self.role}")
                    self.process_resume()
                    
                case "2":
                    valid_roles = list(regex_config.skills_regex.keys())
                    while True:
                        role_input = input("Please enter the role (e.g., Web Developer, Data Scientist, etc.): ").strip()
                        if role_input in valid_roles:
                            self.role = role_input
                            break
                        else:
                            print(f"Invalid role. Valid options are: {', '.join(valid_roles)}")
                            
                    print("\nPlease select a resume file...")
                    self.upload_resume()
                    if self.file_path:
                        self.process_resume()
                    else:
                        print("No valid file was selected to process.")
                case "3":
                    print("Exiting the Resume Parser App.")
                    sys.exit(0)
                case _:
                    print("Invalid option, please try again.")

if __name__ == "__main__":
    main_app = Main()
    main_app.run()