import tkinter as tk
from tkinter import filedialog
from src.models.resume_parser import process_resume

class Main:
    def __init__(self):
        # Esta es la clase principal que coordina todo el flujo
        self.file_path = None
        self.role = "Web Developer"  # O el rol que quieras establecer

    def upload_resume(self):
        """Abre una ventana para seleccionar el archivo."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        self.file_path = filedialog.askopenfilename(
            title="Select Resume File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx"),
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]
        )

        # Verificar si el archivo fue seleccionado
        if not self.file_path:
            print("No file selected.")
            return None

        root.quit()  # Cerrar la ventana de Tkinter después de la selección
        return self.file_path

    def process_resume(self):
        """Procesar el archivo de currículo una vez que sea seleccionado."""
        if self.file_path:
            print(f"Processing resume: {self.file_path}")
            process_resume(self.file_path, self.role)  # Llama a la función para procesar el archivo
        else:
            print("No file to process.")

    def run(self):
        """Ejecuta el flujo principal."""
        print("Please select a resume file...")
        self.upload_resume()

        if self.file_path:
            print(f"Processing the resume from {self.file_path}...\n")
            self.process_resume()
        else:
            print("No valid file was selected to process.")

if __name__ == "__main__":
    main_app = Main()  # Crear una instancia de la clase Main
    main_app.run()  # Ejecutar el flujo