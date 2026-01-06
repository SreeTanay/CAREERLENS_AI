import streamlit as st
from resume_parser import extract_text_from_pdf
from resume_validator import is_likely_resume
from skill_extractor import extract_skills
from role_mapper import suggest_roles
from llm_engine import (
    generate_career_explanation,
    rewrite_resume_bullets,
    generate_interview_questions,
)

# =====================================================
# Page Configuration (FIRST Streamlit call)
# =====================================================
st.set_page_config(
    page_title="CareerLens AI",
    page_icon="📈",
    layout="wide",
)

# =====================================================
# Session State (SAFE defaults)
# =====================================================
st.session_state.setdefault("career_explanation", None)
st.session_state.setdefault("improved_resume", None)
st.session_state.setdefault("interview_questions", None)

# =====================================================
# Header
# =====================================================
col1, col2 = st.columns([1, 7])

with col1:
    st.image("assets/careerlens_logo.png", width=80)

with col2:
    st.markdown(
        """
        <h2 style="color:#3B82F6; margin-bottom:4px;">
            CareerLens AI 🔍
        </h2>
        <p style="font-size:16px; margin-top:-6px;">
            AI-powered resume insights, career guidance,<br>
            and interview preparation
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# =====================================================
# File Upload
# =====================================================
uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF only)",
    type=["pdf"],
)

if uploaded_file is None:
    st.info("👆 Please upload a resume PDF to continue.")
    st.stop()

# =====================================================
# Resume Processing
# =====================================================
with st.spinner("🔍 Reading and validating your resume..."):
    resume_text = extract_text_from_pdf(uploaded_file)

if not is_likely_resume(resume_text):
    st.error("❌ This document does not appear to be a valid resume.")
    st.stop()

st.success("✅ Resume validated successfully!")

# =====================================================
# Rule-Based Analysis
# =====================================================
skills = extract_skills(resume_text)
roles = suggest_roles(skills)

# =====================================================
# Tabs
# =====================================================
tab_resume, tab_career, tab_improve, tab_interview = st.tabs(
    ["📄 Resume", "🎯 Career Fit", "✍️ Improvements", "🎤 Interview Prep"]
)

# =====================================================
# TAB 1 — Resume
# =====================================================
with tab_resume:
    st.subheader("📄 Extracted Resume Content")
    st.text_area("Resume Text", resume_text, height=350)
    st.caption("🔒 Resume is processed only for this session.")

# =====================================================
# TAB 2 — Career Fit
# =====================================================
with tab_career:
    st.subheader("🛠️ Detected Skills")
    st.write(skills if skills else "No recognizable skills detected.")

    st.subheader("🎯 Suggested Career Roles")
    for role in roles:
        st.write("•", role)

    st.divider()
    st.subheader("🤖 AI Career Explanation")

    if st.button("Generate Career Explanation", key="career_btn"):
        with st.spinner("🤖 Generating explanation..."):
            result = generate_career_explanation(skills, roles)

            if isinstance(result, str) and result.strip():
                st.session_state.career_explanation = result.strip()
            else:
                st.session_state.career_explanation = (
                    "⚠️ AI service is currently unavailable.\n\n"
                    "Skills and role suggestions above are still valid."
                )

    if isinstance(st.session_state.career_explanation, str):
        st.markdown(st.session_state.career_explanation)

# =====================================================
# TAB 3 — Resume Improvements
# =====================================================
with tab_improve:
    st.subheader("✍️ Resume Improvement Suggestions")

    if st.button("Analyze Resume for Improvements", key="improve_btn"):
        with st.spinner("🔍 Analyzing resume..."):
            result = rewrite_resume_bullets(resume_text)

            if isinstance(result, str) and result.strip():
                st.session_state.improved_resume = result.strip()
            else:
                st.session_state.improved_resume = (
                    "⚠️ Resume improvement analysis is temporarily unavailable."
                )

    if isinstance(st.session_state.improved_resume, str):
        st.markdown(st.session_state.improved_resume)

# =====================================================
# TAB 4 — Interview Prep
# =====================================================
with tab_interview:
    st.subheader("🎤 Interview Preparation")

    if st.button("Generate Interview Questions", key="interview_btn"):
        with st.spinner("🎯 Generating interview questions..."):
            result = generate_interview_questions(skills, roles)

            if isinstance(result, str) and result.strip():
                cleaned = (
                    result.replace("<s>", "")
                          .replace("[INST]", "")
                          .replace("[/INST]", "")
                          .strip()
                )
                st.session_state.interview_questions = cleaned
            else:
                st.session_state.interview_questions = (
                    "⚠️ Interview questions are temporarily unavailable."
                )

    if isinstance(st.session_state.interview_questions, str):
        st.markdown(st.session_state.interview_questions)











