import tkinter as tk
from tkinter import filedialog
import os
import sys
import random

# Añadir el directorio raíz al path para que se puedan encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.resume_classifier import ResumeClassifier
from src.models.resume_ranker import ResumeRanker
from src.config import regex_config
from data import sample_resumes

class Main:
    def __init__(self):
        # Se define un rol por defecto aleatorio, pero en la opción 2 se permitirá que el usuario lo ingrese manualmente.
        self.file_path = None
        default_roles = ["Data Scientist", "AI Engineer", "Software Engineer", "Web Developer", "DevOps Engineer"]
        self.role = random.choice(default_roles)

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

    def process_resume(self):
        resume_classifier = ResumeClassifier()
        resume_ranker = ResumeRanker()
        
        if self.file_path:
            print(f"\nProcessing resume: {self.file_path}\n")
            
            # Extraer información del CV
            parser = resume_classifier.resume
            resume_text = parser.read_resume(self.file_path)
            resume_info = parser.extract_resume_info(resume_text, self.role)
            
            # Clasificar usando autómata (método original)
            classification = resume_classifier.classify_resume(self.file_path, self.role)
            print("Classification (using DFA):", classification)
            
            # Ranking usando transductor (FST - nuevo método)
            ranking_result = resume_ranker.rank_resume(resume_info, self.role)
            
            print("\n--- CV Ranking using FST ---")
            print(f"Score: {ranking_result['score']} - Ranking: {ranking_result['ranking']}")
            print("\nComponent Scores:")
            
            # Mostrar puntuaciones detalladas por componente
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