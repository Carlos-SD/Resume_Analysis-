email_regex = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
phone_regex = r"(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})"
name_regex = r"([A-Za-z\s]+)"
role_regex = r"([A-Za-z\s]+)"
education_regex = r"EDUCATION\s*\n(.*?)(?=\n[A-Z\s]+(?:\n|$))"
work_experience_regex = r"WORK EXPERIENCE\s*\n(.*?)(?=\n[A-Z\s]+(?:\n|$))"
skills_regex = {
    "Data Scientist": r"SKILLS\s*:?\s*\n(.*?)(?=\n[A-Z][A-Z\s]+(?:\n|$)|$)",
    "AI Engineer": r"SKILLS\s*:?\s*\n(.*?)(?=\n[A-Z][A-Z\s]+(?:\n|$)|$)",
    "Software Engineer": r"SKILLS\s*:?\s*\n(.*?)(?=\n[A-Z][A-Z\s]+(?:\n|$)|$)",
    "Web Developer": r"SKILLS\s*:?\s*\n(.*?)(?=\n[A-Z][A-Z\s]+(?:\n|$)|$)",
    "DevOps Engineer": r"SKILLS\s*:?\s*\n(.*?)(?=\n[A-Z][A-Z\s]+(?:\n|$)|$)"
}