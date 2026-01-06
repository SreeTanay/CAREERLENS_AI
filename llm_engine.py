import requests
import os

OPENROUTER_API_KEY = "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"

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "mistralai/mistral-7b-instruct"

def generate_ai_response(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 800
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    data = response.json()

    return data["choices"][0]["message"]["content"]
def generate_career_explanation(skills, roles):
    prompt = (
        f"The candidate has skills: {', '.join(skills)}. "
        f"Suggested roles: {', '.join(roles)}. "
        "Explain clearly why these roles are suitable."
    )
    return generate_ai_response(prompt)


def rewrite_resume_bullets(resume_text):
    prompt = (
        "You are a senior technical resume reviewer.\n\n"
        "Analyze the resume below and provide ONLY improvement suggestions.\n\n"
        "Rules:\n"
        "- Do NOT rewrite the entire resume\n"
        "- Do NOT repeat resume content verbatim\n"
        "- Identify weak bullet points\n"
        "- Suggest how to improve them\n"
        "- Mention what should be replaced and why\n"
        "- Focus on impact, clarity, and technical depth\n"
        "- Use bullet points for suggestions\n\n"
        "Resume:\n"
        f"{resume_text[:1200]}"
    )
    return generate_ai_response(prompt)



def generate_interview_questions(skills, roles):
    prompt = (
        "You are an interviewer.\n\n"
        f"Candidate skills: {', '.join(skills)}\n"
        f"Target roles: {', '.join(roles)}\n\n"
        "Generate 6 clear interview questions:\n"
        "- 3 technical questions\n"
        "- 3 behavioral questions\n"
        "Format as a numbered list.\n"
        "Do not include any special tokens.\n"
        "Ensure the response is complete."
    )
    return generate_ai_response(prompt)





