def extract_skills(resume_text):
    skill_keywords = [
        "python", "machine learning", "deep learning", "data analysis",
        "statistics", "sql", "streamlit", "nlp", "ai",
        "prompt engineering", "pandas", "numpy", "scikit-learn"
    ]

    resume_text = resume_text.lower()
    detected_skills = []

    for skill in skill_keywords:
        if skill in resume_text:
            detected_skills.append(skill.title())

    return detected_skills
