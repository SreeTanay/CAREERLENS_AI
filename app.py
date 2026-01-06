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
# Session State Initialization
# =====================================================
if "career_explanation" not in st.session_state:
    st.session_state.career_explanation = None

if "improved_resume" not in st.session_state:
    st.session_state.improved_resume = None

if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None


# =====================================================
# Page Configuration
# =====================================================
st.set_page_config(
    page_title="CareerLens AI",
    page_icon="📈",
    layout="wide",
)


# =====================================================
# Header: Logo BESIDE Title (Clean & Professional)
# =====================================================
header_col1, header_col2 = st.columns([1, 7])

with header_col1:
    st.image("assets/careerlens_logo.png", width=80)

with header_col2:
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
# Resume Processing & Validation
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
# Tabs Layout
# =====================================================
tab_resume, tab_career, tab_improve, tab_interview = st.tabs(
    ["📄 Resume", "🎯 Career Fit", "✍️ Improvements", "🎤 Interview Prep"]
)


# =====================================================
# TAB 1 — Resume
# =====================================================
with tab_resume:
    st.subheader("📄 Extracted Resume Content")
    st.text_area(
        "Resume Text",
        resume_text,
        height=350,
    )
    st.caption("🔒 Uploaded resumes are processed only for this session and are not stored.")


# =====================================================
# TAB 2 — Career Fit
# =====================================================
with tab_career:
    st.subheader("🛠️ Detected Skills")

    if skills:
        st.write(skills)
    else:
        st.warning("No recognizable skills detected.")

    st.subheader("🎯 Suggested Career Roles")
    for role in roles:
        st.write("•", role)

    st.divider()

    st.subheader("🤖 AI Career Explanation")

    if st.button("Generate Career Explanation"):
        with st.spinner("🤖 Generating explanation..."):
            st.session_state.career_explanation = generate_career_explanation(
                skills, roles
            )

    if st.session_state.career_explanation:
        st.markdown(st.session_state.career_explanation)


# =====================================================
# TAB 3 — Resume Improvements
# =====================================================
with tab_improve:
    st.subheader("✍️ Resume Improvement Suggestions")
    st.write(
        "Actionable feedback on **what to improve**, "
        "what to replace, and how to strengthen impact."
    )

    if st.button("Analyze Resume for Improvements"):
        with st.spinner("🔍 Analyzing resume..."):
            st.session_state.improved_resume = rewrite_resume_bullets(resume_text)

    if st.session_state.improved_resume:
        st.markdown(st.session_state.improved_resume)


# =====================================================
# TAB 4 — Interview Preparation
# =====================================================
with tab_interview:
    st.subheader("🎤 Interview Preparation")
    st.write(
        "Role-specific technical and behavioral interview questions "
        "based on your resume and skill set."
    )

    if st.button("Generate Interview Questions"):
        with st.spinner("🎯 Generating interview questions..."):
            st.session_state.interview_questions = generate_interview_questions(
                skills, roles
            )

    if st.session_state.interview_questions:
        cleaned_questions = (
            st.session_state.interview_questions
            .replace("<s>", "")
            .replace("[INST]", "")
            .replace("[/INST]", "")
            .strip()
        )
        st.markdown(cleaned_questions)










