import tkinter as tk
from tkinter import filedialog
from src.models.resume_classifier import ResumeClassifier
from src.config import regex_config
from data import sample_resumes
import os
import random
import sys

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
        if self.file_path:
            print(f"\nProcessing resume: {self.file_path}\n")
            classification = resume_classifier.classify_resume(self.file_path, self.role)
            print("Classification:", classification)
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