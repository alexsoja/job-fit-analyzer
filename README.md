# Multi-Signal Job Fit Analyzer

A resume and job description analysis tool that evaluates candidate fit using multiple independent signals.  
The system produces an explainable, category-level breakdown rather than a single opaque score, enabling clearer insight into strengths, gaps, and alignment.

---

## Overview

The Multi-Signal Job Fit Analyzer compares a candidate’s resume against a job description using structured parsing and rule-based heuristics.  
It evaluates fit across three core dimensions:

- Skills alignment
- Education alignment
- Experience alignment

Each dimension is scored independently and combined into a 100-point composite score with transparent reasoning.

This project is designed as a foundation for more advanced weighting, calibration, and feedback systems.

---

## Core Features

### Multi-Signal Scoring Model
Candidate fit is evaluated using three independent signals:

- **Skills Matching**
  - Exact and normalized skill matching
  - Detection of missing or underrepresented skills
- **Education Alignment**
  - Degree level detection (Bachelor’s, Master’s, PhD variants)
  - Major-to-role alignment using an expanded taxonomy
- **Experience Evaluation**
  - Parsing of experience requirements from job descriptions
  - Estimation of candidate experience based on resume content

Scores are combined into a 100-point scale with a clear breakdown for each category.

---

## Explainability First

Rather than returning a single numerical score, the analyzer surfaces:

- Why a candidate is a strong or weak fit
- Which categories contribute positively or negatively
- Where gaps exist relative to job requirements

This design supports transparency and future feedback-driven improvements.

---

## Data & Parsing Enhancements

Recent updates focused on improving accuracy and coverage:

- Expanded skills dataset (200+ skills) to reduce false negatives
- Expanded majors dataset (30+ majors) for better education matching
- Improved degree detection logic supporting common abbreviations and variants

These improvements increase recall and reliability without altering the core scoring model.

---

## Technology Stack

- Python
- Streamlit (UI layer)
- Regular expressions and heuristic parsing
- JSON-based seed datasets for skills and majors

---

## Project Structure (High Level)

```
.
├── app.py
├── data/
│   ├── skills.json
│   └── majors.json
├── parsing/
│   ├── skills.py
│   ├── education.py
│   └── experience.py
├── scoring/
│   └── score.py
└── README.md
```

---

## Current Limitations

- Heuristic-based parsing (no ML models yet)
- Equal weighting across scoring categories
- UI focused on functionality rather than polish

---

## Roadmap

Planned future improvements include:

- Category-level weighting and calibration
- Resume feedback and improvement suggestions
- UI and visualization enhancements
- Exportable reports
- Optional ML-assisted parsing and matching

---

## Versioning

This project follows semantic versioning:

- **v0.2.0** – Introduced multi-signal scoring with explainable breakdowns
- **v0.2.1** – Improved parsing accuracy and expanded skills and majors datasets

---

## Disclaimer

This tool is intended for educational and exploratory purposes.  
It does not replace human judgment in hiring decisions.

---

## Author

Developed by Alex Soja
