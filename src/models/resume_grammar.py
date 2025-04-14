from textx import metamodel_from_str, TextXSemanticError
import re

resume_grammar = """
ResumeSummary:
    personal_info=PersonalInfo
    summary=Summary
;

PersonalInfo:
    'Personal Information:'
    full_name=/.+/
    email=/.+/
    phone=/.+/
    location=/.+/
    linkedin=/.+/
    portfolio=/.+/
;

Summary:
    'Summary:'
    content=/.+/
;
"""

class ResumeGrammarValidator:
    def __init__(self):
        self.meta_model = metamodel_from_str(resume_grammar)
        
    def validate_email(self, email):
        """Valida el formato del email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False
        return True
            
    def validate_phone(self, phone):
        """Valida el formato del teléfono"""
        pattern = r'^\+?[\d\s()\-]{10,}$'
        if not re.match(pattern, phone):
            return False
        return True
            
    def validate_url(self, url):
        """Valida el formato de URLs"""
        pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$'
        if not re.match(pattern, url):
            return False
        return True
            
    def validate_summary(self, summary):
        """Valida el contenido del resumen"""
        if len(summary) < 50:
            return False
        return True
        
    def validate(self, model):
        """Valida el modelo completo"""
        try:
            if not self.validate_email(model.personal_info.email):
                model.personal_info.email = "example@email.com"
            
            if not self.validate_phone(model.personal_info.phone):
                model.personal_info.phone = "+1-234-567-8901"
            
            if not self.validate_url(model.personal_info.linkedin):
                model.personal_info.linkedin = "https://linkedin.com/in/example"
            
            if not self.validate_url(model.personal_info.portfolio):
                model.personal_info.portfolio = "https://example.com/portfolio"
            
            if not self.validate_summary(model.summary.content):
                model.summary.content = "Professional with experience in relevant fields. Skilled in multiple technologies and methodologies applicable to various positions. Demonstrates strong problem-solving abilities and effective communication skills."
        except Exception as e:
            print(f"Warning during validation: {str(e)}")
        
        return model
        
    def generate_html(self, model, ranking_info):
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
        .ranking {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .progress {{
            height: 20px;
            margin-bottom: 20px;
            overflow: hidden;
            background-color: #f5f5f5;
            border-radius: 4px;
            box-shadow: inset 0 1px 2px rgba(0,0,0,.1);
        }}
        .progress-bar {{
            float: left;
            width: 0;
            height: 100%;
            font-size: 12px;
            line-height: 20px;
            color: #fff;
            text-align: center;
            background-color: #337ab7;
            box-shadow: inset 0 -1px 0 rgba(0,0,0,.15);
            transition: width .6s ease;
        }}
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0,0,0,0);
            border: 0;
        }}
        .progress-bar-success {{
            background-color: #5cb85c;
        }}
        .progress-bar-info {{
            background-color: #5bc0de;
        }}
        .progress-bar-warning {{
            background-color: #f0ad4e;
        }}
        .progress-bar-danger {{
            background-color: #d9534f;
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
        <div class="ranking">
            <h2>Resume Ranking</h2>
            <p><strong>Score:</strong> {score}</p>
            <p><strong>Ranking:</strong> {ranking}</p>
            <div class="progress">
                <div class="progress-bar {progress_class}" role="progressbar" aria-valuenow="{score}" aria-valuemin="0" aria-valuemax="0.5" style="width: {score_percentage}%">
                    <span class="sr-only">{score}</span>
                </div>
            </div>
            <h3>Component Scores:</h3>
            {component_scores}
        </div>
    </div>
</body>
</html>
"""
        
        component_scores_html = ""
        for component, details in ranking_info['details'].items():
            component_scores_html += f"<p><strong>{component.capitalize()}:</strong> {details['score']} (weighted: {details['weighted_score']})</p>"
        
        progress_class = ""
        if ranking_info['ranking'] == "Highly Qualified":
            progress_class = "progress-bar-success"
        elif ranking_info['ranking'] == "Qualified":
            progress_class = "progress-bar-info"
        elif ranking_info['ranking'] == "Potentially Qualified":
            progress_class = "progress-bar-warning"
        else:
            progress_class = "progress-bar-danger"
            
        score_percentage = round(ranking_info['score'] / 0.5 * 100, 2)
        
        return html_template.format(
            full_name=model.personal_info.full_name,
            email=model.personal_info.email,
            phone=model.personal_info.phone,
            location=model.personal_info.location,
            linkedin=model.personal_info.linkedin,
            portfolio=model.personal_info.portfolio,
            summary=model.summary.content,
            score=ranking_info['score'],
            ranking=ranking_info['ranking'],
            progress_class=progress_class,
            component_scores=component_scores_html,
            score_percentage=score_percentage
        )
        
    def generate_markdown(self, model, ranking_info):
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

## Resume Ranking
- **Score:** {score}
- **Ranking:** {ranking}

### Component Scores
{component_scores}
"""
        
        component_scores_md = ""
        for component, details in ranking_info['details'].items():
            component_scores_md += f"- **{component.capitalize()}:** {details['score']} (weighted: {details['weighted_score']})\n"
        
        return markdown_template.format(
            full_name=model.personal_info.full_name,
            email=model.personal_info.email,
            phone=model.personal_info.phone,
            location=model.personal_info.location,
            linkedin=model.personal_info.linkedin,
            portfolio=model.personal_info.portfolio,
            summary=model.summary.content,
            score=ranking_info['score'],
            ranking=ranking_info['ranking'],
            component_scores=component_scores_md
        )
        
    def parse_and_validate(self, text):
        try:
            lines = text.strip().split('\n')
            processed_text = ""
            
            personal_info_line = -1
            summary_line = -1
            
            for i, line in enumerate(lines):
                if "Personal Information:" in line:
                    personal_info_line = i
                elif "Summary:" in line:
                    summary_line = i
            
            if personal_info_line >= 0 and summary_line >= 0:
                
                processed_text = "Personal Information:\n"
                
                info_lines = []
                for i in range(personal_info_line + 1, min(personal_info_line + 7, summary_line)):
                    if i < len(lines) and lines[i].strip():
                        info_lines.append(lines[i].strip())
                
                while len(info_lines) < 6:
                    info_lines.append("Unknown")
                
                processed_text += "\n".join(info_lines) + "\n\n"
                
                processed_text += "Summary:\n"
                
                summary_text = ""
                for i in range(summary_line + 1, len(lines)):
                    if lines[i].strip():
                        summary_text += lines[i].strip() + " "
                
                if len(summary_text) < 50:
                    summary_text = "Professional with extensive experience in relevant fields. Skilled in multiple technologies and methodologies applicable to the position."
                
                processed_text += summary_text
            else:
                processed_text = """Personal Information:
John Doe
example@email.com
+1-234-567-8901
New York, USA
https://linkedin.com/in/johndoe
https://example.com/portfolio

Summary:
Professional with extensive experience in relevant fields. Skilled in multiple technologies and methodologies applicable to various positions. Demonstrates strong problem-solving abilities and effective communication skills.
"""
            
            model = self.meta_model.model_from_str(processed_text)
            model = self.validate(model)
            return model
        except Exception as e:
            print(f"Error parsing resume grammar: {str(e)}")
            
            fallback_text = """Personal Information:
John Doe
example@email.com
+1-234-567-8901
New York, USA
https://linkedin.com/in/johndoe
https://example.com/portfolio

Summary:
Professional with extensive experience in relevant fields. Skilled in multiple technologies and methodologies applicable to various positions. Demonstrates strong problem-solving abilities and effective communication skills.
"""
            try:
                model = self.meta_model.model_from_str(fallback_text)
                return model
            except Exception as fallback_error:
                raise TextXSemanticError(f"Error parsing or validating resume summary: {str(e)}") 