def suggest_roles(skills):
    roles = []

    if "Python" in skills and "Machine Learning" in skills:
        roles.append("Machine Learning Engineer")

    if "Statistics" in skills and "Data Analysis" in skills:
        roles.append("Data Analyst")

    if "Prompt Engineering" in skills or "Ai" in skills:
        roles.append("Generative AI / Prompt Engineer")

    if "Python" in skills and "Sql" in skills:
        roles.append("Backend / Data Engineer")

    if not roles:
        roles.append("Software Engineer (Entry Level)")

    return roles
