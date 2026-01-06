import requests
import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# Environment & Config
# =====================================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://careerlens-ai.streamlit.app",
    "X-Title": "CareerLens AI",
}

MODEL = "mistralai/mistral-7b-instruct"

MAX_INPUT_CHARS = 1200     # 🔴 critical
MAX_OUTPUT_TOKENS = 350   # 🔴 critical


# =====================================================
# Utility: Safe truncation
# =====================================================
def _truncate(text, max_chars=MAX_INPUT_CHARS):
    if not text:
        return ""
    return text[:max_chars]


# =====================================================
# Core LLM Call (SAFE)
# =====================================================
def generate_ai_response(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": MAX_OUTPUT_TOKENS,
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return (
                "⚠️ AI service is temporarily unavailable.\n\n"
                "Please try again in a moment.\n"
                "Rule-based insights are still available."
            )

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return (
            "⚠️ AI service error occurred.\n\n"
            "Please try again shortly."
        )


# =====================================================
# AI Features
# =====================================================
def generate_career_explanation(skills, roles):
    prompt = (
        f"Skills: {', '.join(skills)}\n"
        f"Suggested roles: {', '.join(roles)}\n\n"
        "Explain why these roles fit the candidate.\n"
        "Use 5–6 concise bullet points."
    )
    return generate_ai_response(prompt)


def rewrite_resume_bullets(resume_text):
    safe_resume = _truncate(resume_text)

    prompt = (
        "You are a senior technical resume reviewer.\n\n"
        "Provide ONLY improvement suggestions.\n\n"
        "Rules:\n"
        "- Do NOT rewrite the resume\n"
        "- Do NOT repeat content\n"
        "- Point out weaknesses\n"
        "- Suggest improvements and replacements\n"
        "- Focus on impact and technical clarity\n"
        "- Use bullet points only\n\n"
        f"Resume excerpt:\n{safe_resume}"
    )
    return generate_ai_response(prompt)


def generate_interview_questions(skills, roles):
    prompt = (
        f"Candidate skills: {', '.join(skills)}\n"
        f"Target roles: {', '.join(roles)}\n\n"
        "Generate exactly 6 interview questions:\n"
        "- 3 technical\n"
        "- 3 behavioral\n"
        "Number them clearly.\n"
        "Ensure the response completes fully."
    )
    return generate_ai_response(prompt)






