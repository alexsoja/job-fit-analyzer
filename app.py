# app.py

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from jobfit.analyze import analyze
from jobfit.ingest.pdf_extract import extract_text_from_pdf

import jobfit
st.write("jobfit imported from:", jobfit.__file__)


st.title("Job Fit Analyzer")

resume_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
jd_text_input = st.text_area("Paste job description", height=220)

analyze_clicked = st.button("Analyze")

if analyze_clicked:
    if resume_file is None or not jd_text_input.strip():
        st.error("Please upload a resume PDF and paste a job description.")
        st.stop()

    # Save uploaded PDF to a temp file (pypdf needs a file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        pdf_path = Path(tmp.name)

    resume_text = extract_text_from_pdf(pdf_path)

    # Debug: confirm what text we extracted from the PDF
    with st.expander("Debug: extracted resume text (first 2000 chars)"):
        st.text(resume_text[:2000])

    result = analyze(resume_text, jd_text_input)
    with st.expander("Debug: extracted skills sets"):
        st.write("resume_skills:", result["skills"]["resume_skills"])
        st.write("jd_skills:", result["skills"]["jd_skills"])
        st.write("missing:", result["skills"]["missing"])
    with st.expander("Debug: normalized JD (first 400 chars)"):
        from jobfit.preprocess.normalize import normalize_text
        st.text(normalize_text(jd_text_input)[:400])

    # ----- Score -----
    st.header("Score")
    s = result["score"]
    st.write(f"Skills score: {s['skills_points']}/{s['skills_max']}")
    st.write(f"Education score: {s['education_points']}/{s['education_max']}")
    st.write(f"Total score: {s['total_points']}/{s['total_max']}")
    st.caption(s["note"])

    # ----- Skills -----
    st.header("Skills")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matched")
        st.write(result["skills"]["matched"])

    with col2:
        st.subheader("Missing")
        st.write(result["skills"]["missing"])

    # ----- Education -----
    st.header("Education")
    edu = result["education"]
    st.write(f"JD degree: {edu['jd_degree']}")
    st.write(f"Resume degree: {edu['resume_degree']}")
    st.write(f"Matched majors: {edu['matched_majors']}")
    st.write(f"Missing majors: {edu['missing_majors']}")
    st.write(f"Education score: {edu['education_total']}/15")

    # ----- Requirement coverage -----
    st.header("Requirement coverage (skills-based)")
    cov = result["requirements"]["coverage"]
    if not cov:
        st.write("No requirement lines matched to known skills yet.")
    else:
        for item in cov[:12]:
            st.write(f"- {item['line']}")
            if item["matched"]:
                st.caption(f"matched: {item['matched']}")
            if item["missing"]:
                st.caption(f"missing: {item['missing']}")
