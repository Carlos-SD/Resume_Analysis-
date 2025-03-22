contact_info_regex = {
    "name": r"(Name:\s*([A-Za-z\s]+))",
    "email": r"(Email:\s*([\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}))",
    "phone": r"(Phone:\s*(\+?\d{1,2}\s?\(?\d+\)?[\s.-]?\d+[\s.-]?\d+))",
    "role": r"(Role:\s*([A-Za-z\s]+))"
}

education_regex = r"(Education:\s*(.*\n.*))"
work_experience_regex = r"(Work Experience:\s*(.*\n.*))"
skills_regex = {
    "Data Scientist": r"(Skills:\s*(Python|R|Machine Learning|Deep Learning|Data Science))",
    "AI Engineer": r"(Skills:\s*(TensorFlow|Keras|PyTorch|AI|Neural Networks))",
    "Software Engineer": r"(Skills:\s*(Java|C++|Python|Git|Software Development))",
    "Web Developer": r"(Skills:\s*(HTML|CSS|JavaScript|React|Node.js|Angular))",
    "DevOps Engineer": r"(Skills:\s*(Docker|Kubernetes|CI/CD|AWS|Terraform|Ansible))"
}