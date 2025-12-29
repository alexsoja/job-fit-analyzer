# Job Fit Analyzer

A simple Python project that compares a resume and a job description to produce:
- a basic fit score (/100)
- matched vs missing skills
- requirement line coverage (skills-based)
- CLI and Streamlit UI

This repo is intentionally designed to be easy to understand and rebuild.

## Setup

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run the CLI

```bash
python -m jobfit.cli --resume src/tests/fixtures/sample_resume.txt --jd src/tests/fixtures/sample_jd.txt
```

## Run the Streamlit app

```bash
streamlit run app.py
```

## What is implemented right now

- TXT and PDF resume ingestion (PDF uses pypdf)
- Text normalization (lowercasing and whitespace cleanup)
- Skill extraction using a small seed list (JSON)
- Basic score out of 100 (skills-only so far)
- Requirement line extraction and coverage (skills-based)
- Shared analysis function used by both CLI and Streamlit (`jobfit.analyze.analyze`)
