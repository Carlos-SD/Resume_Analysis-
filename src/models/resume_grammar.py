from textx import metamodel_from_str, TextXSemanticError
import re

# Definición de la gramática para el resumen del CV
resume_grammar = """
ResumeSummary:
    personal_info=PersonalInfo
    summary=Summary
;

PersonalInfo:
    'Personal Information:'
    full_name=STRING
    email=STRING
    phone=STRING
    location=STRING
    linkedin=STRING
    portfolio=STRING
;

Summary:
    'Summary:'
    content=STRING
;
"""

class ResumeGrammarValidator:
    def __init__(self):
        self.meta_model = metamodel_from_str(resume_grammar)
        
    def validate_email(self, email):
        """Valida el formato del email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise TextXSemanticError(f"Invalid email format: {email}")
            
    def validate_phone(self, phone):
        """Valida el formato del teléfono"""
        pattern = r'^\+?[\d\s-()]{10,}$'
        if not re.match(pattern, phone):
            raise TextXSemanticError(f"Invalid phone format: {phone}")
            
    def validate_url(self, url):
        """Valida el formato de URLs"""
        pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$'
        if not re.match(pattern, url):
            raise TextXSemanticError(f"Invalid URL format: {url}")
            
    def validate_summary(self, summary):
        """Valida el contenido del resumen"""
        if len(summary) < 50:
            raise TextXSemanticError("Summary must be at least 50 characters long")
            
    def validate(self, model):
        """Valida el modelo completo"""
        # Validar email
        self.validate_email(model.personal_info.email)
        
        # Validar teléfono
        self.validate_phone(model.personal_info.phone)
        
        # Validar URLs
        self.validate_url(model.personal_info.linkedin)
        self.validate_url(model.personal_info.portfolio)
        
        # Validar resumen
        self.validate_summary(model.summary.content)
        
    def generate_html(self, model):
        """Genera HTML a partir del modelo validado"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Summary</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
        }}
        .info {{
            margin-bottom: 10px;
            padding: 5px;
            border-bottom: 1px solid #eee;
        }}
        .info:last-child {{
            border-bottom: none;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .summary {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Resume Summary</h1>
        <div class="info"><strong>Full Name:</strong> {full_name}</div>
        <div class="info"><strong>Email:</strong> {email}</div>
        <div class="info"><strong>Phone:</strong> {phone}</div>
        <div class="info"><strong>Location:</strong> {location}</div>
        <div class="info"><strong>LinkedIn:</strong> <a href="{linkedin}" target="_blank">LinkedIn Profile</a></div>
        <div class="info"><strong>Portfolio:</strong> <a href="{portfolio}" target="_blank">Portfolio</a></div>
        <div class="summary">
            <h2>Summary</h2>
            <p>{summary}</p>
        </div>
    </div>
</body>
</html>
"""
        return html_template.format(
            full_name=model.personal_info.full_name,
            email=model.personal_info.email,
            phone=model.personal_info.phone,
            location=model.personal_info.location,
            linkedin=model.personal_info.linkedin,
            portfolio=model.personal_info.portfolio,
            summary=model.summary.content
        )
        
    def generate_markdown(self, model):
        """Genera Markdown a partir del modelo validado"""
        markdown_template = """
# Resume Summary

## Personal Information
- **Full Name:** {full_name}
- **Email:** {email}
- **Phone:** {phone}
- **Location:** {location}
- **LinkedIn:** [{linkedin}]({linkedin})
- **Portfolio:** [{portfolio}]({portfolio})

## Summary
{summary}
"""
        return markdown_template.format(
            full_name=model.personal_info.full_name,
            email=model.personal_info.email,
            phone=model.personal_info.phone,
            location=model.personal_info.location,
            linkedin=model.personal_info.linkedin,
            portfolio=model.personal_info.portfolio,
            summary=model.summary.content
        )
        
    def parse_and_validate(self, text):
        """Parsea y valida el texto del resumen"""
        try:
            model = self.meta_model.model_from_str(text)
            self.validate(model)
            return model
        except Exception as e:
            raise TextXSemanticError(f"Error parsing or validating resume summary: {str(e)}") 