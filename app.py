from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from jobfit.analyze import analyze
from jobfit.ingest.pdf_extract import extract_text_from_pdf


st.title("Job Fit Analyzer")
st.write("Upload a resume PDF and paste a job description to get a basic fit score and gaps.")

resume_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
jd_text_input = st.text_area("Paste job description", height=260)

analyze_clicked = st.button("Analyze")

if analyze_clicked:
    if resume_file is None or not jd_text_input.strip():
        st.error("Please upload a resume PDF and paste a job description.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        pdf_path = Path(tmp.name)

    resume_text = extract_text_from_pdf(pdf_path)

    result = analyze(resume_text, jd_text_input)

    s = result["score"]
    st.subheader("Score")
    st.write(f"Skills score: {s['skills_points']}/{s['skills_max']}")
    st.write(f"Total score: {s['total_points']}/{s['total_max']}")
    st.caption(s["note"])

    st.subheader("Skills")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Matched")
        st.write(result["skills"]["matched"])
    with col2:
        st.write("Missing")
        st.write(result["skills"]["missing"])

    st.subheader("Requirement coverage (skills-based)")
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
