import re

def is_likely_resume(resume_text):
    text = resume_text.lower()

    resume_sections = [
        "experience", "education", "skills", "projects",
        "internship", "certification", "work experience"
    ]

    resume_role_words = [
        "engineer", "developer", "analyst", "intern",
        "scientist", "manager"
    ]

    # Heuristic signals
    section_hits = sum(1 for s in resume_sections if s in text)
    role_hits = sum(1 for r in resume_role_words if r in text)

    has_email = bool(re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text))
    has_years = bool(re.search(r"(19|20)\d{2}", text))

    word_count = len(text.split())

    # STRONGER decision rule
    if (
        word_count > 200 and
        section_hits >= 2 and
        (has_email or has_years) and
        role_hits >= 1
    ):
        return True

    return False
