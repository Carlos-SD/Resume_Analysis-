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
        return f"""
Personal Information:
{resume_info.get('name', 'Unknown')}
{resume_info.get('email', 'unknown@email.com')}
{resume_info.get('phone', 'Unknown')}
{resume_info.get('location', 'Unknown')}
{resume_info.get('linkedin', 'https://linkedin.com/in/unknown')}
{resume_info.get('portfolio', 'https://portfolio.com/unknown')}

Summary:
{resume_info.get('summary', 'No summary available.')}
"""

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
            
            parser = resume_classifier.resume
            resume_text = parser.read_resume(self.file_path)
            resume_info = parser.extract_resume_info(resume_text, self.role)
            
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
                model = self.grammar_validator.parse_and_validate(summary_text)
                
                # Generar visualizaciones
                html_content = self.grammar_validator.generate_html(model)
                markdown_content = self.grammar_validator.generate_markdown(model)
                
                # Guardar resúmenes
                html_path, md_path = self.save_summary(html_content, markdown_content, self.file_path)
                
                print("\n--- Resume Summary Generated ---")
                print(f"HTML summary saved to: {html_path}")
                print(f"Markdown summary saved to: {md_path}")
                
            except Exception as e:
                print(f"\nError generating summary: {str(e)}")
                
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
                    archives = os.listdir(default_folder)
                    if not archives:
                        print("No default resumes found in the folder.")
                        continue
                    selected_archive = random.choice(archives)
                    self.file_path = os.path.join(default_folder, selected_archive)
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