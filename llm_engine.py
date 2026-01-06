import requests
import os

# =====================================================
# Environment & Config
# =====================================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Do NOT crash the app — let UI handle absence gracefully
if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = None

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}" if OPENROUTER_API_KEY else "",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://careerlens-ai.streamlit.app",
    "X-Title": "CareerLens AI",
}

MODEL = "mistralai/mistral-7b-instruct"
MAX_OUTPUT_TOKENS = 300


# =====================================================
# Core LLM Call (GRACEFUL)
# =====================================================
def generate_ai_response(prompt):
    """
    Returns:
        - string (AI response) on success
        - None on any failure
    """

    if not OPENROUTER_API_KEY:
        return None

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
            timeout=25
        )

        if response.status_code != 200:
            return None

        data = response.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not content:
            return None

        return content

    except Exception:
        return None


# =====================================================
# AI Features (Thin Wrappers)
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
    prompt = (
        "You are a senior technical resume reviewer.\n\n"
        "Provide ONLY improvement suggestions.\n\n"
        "Rules:\n"
        "- Do NOT rewrite the resume\n"
        "- Do NOT repeat content\n"
        "- Identify weak points\n"
        "- Suggest how to improve or replace them\n"
        "- Focus on impact and technical clarity\n"
        "- Use bullet points only\n\n"
        f"Resume:\n{resume_text[:1200]}"
    )
    return generate_ai_response(prompt)


def generate_interview_questions(skills, roles):
    prompt = (
        f"Candidate skills: {', '.join(skills)}\n"
        f"Target roles: {', '.join(roles)}\n\n"
        "Generate exactly 6 interview questions:\n"
        "- 3 technical\n"
        "- 3 behavioral\n"
        "Number them clearly."
    )
    return generate_ai_response(prompt)







