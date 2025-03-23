import tkinter as tk
from tkinter import filedialog
from src.models.resume_parser import read_resume, extract_resume_info
from data import sample_resumes
import os
import random
import sys

class Main:
    def __init__(self):
        self.file_path = None
        self.role = None 

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
        if self.file_path:
            print(f"\nProcessing resume: {self.file_path}\n")
            resume_text = read_resume(self.file_path)
            info = extract_resume_info(resume_text, self.role)
            print("Extracted Information:")
            for key, value in info.items():
                print(f"{key.capitalize()}: {value}")
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
                    self.role = input("Please enter the role (e.g., Web Developer, Data Scientist, etc.): ").strip()
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