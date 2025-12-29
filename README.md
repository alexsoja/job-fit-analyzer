# Job Fit Analyzer

A Python-based job fit analysis tool that compares a resume against a job description and produces an explainable fit score.

This project focuses on transparent, rule-based analysis rather than black-box models. It highlights which requirements are met, which are missing, and why a given score was assigned.

---

## Features

- Resume ingestion from PDF
- Job description parsing from raw text
- Skill extraction with synonym handling
- Missing skill detection
- Education level and major matching
- Experience requirement parsing and estimation
- Explainable 100-point scoring system
- Command-line interface and Streamlit UI
- Unit tests for core extraction and scoring logic

---

## Scoring Model

The total score is calculated out of 100 points using three independent signals:

| Category    | Max Points |
|------------|------------|
| Skills     | 50         |
| Education  | 15         |
| Experience | 35         |
| **Total**  | **100**    |

Each category produces a detailed, interpretable breakdown rather than a single opaque score.

---

## Project Structure

```
job-fit-analyzer/
├── app.py
├── src/
│   ├── jobfit/
│   │   ├── analyze.py
│   │   ├── preprocess/
│   │   ├── extract/
│   │   ├── score/
│   │   └── ingest/
│   ├── data/
│   │   ├── skills_seed.json
│   │   └── majors_seed.json
│   └── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## How It Works

1. Resume text is extracted from a PDF
2. Resume and job description text are normalized
3. Skills are detected using a curated skill dictionary and synonyms
4. Education level and major keywords are identified
5. Experience requirements are parsed from the job description
6. Resume experience is estimated from date ranges
7. Scores are calculated per category
8. Missing requirements are surfaced explicitly

---

## Running the Application

### Install dependencies
```bash
python -m pip install -e .
```

### Run tests
```bash
python -m pytest
```

### Run the Streamlit app
```bash
python -m streamlit run app.py
```

---

## Example Output

- Matched skills
- Missing skills
- Education alignment
- Experience coverage
- Per-category score breakdown
- Total job fit score

---

## Design Philosophy

This project prioritizes explainability, deterministic logic, and real-world resume and job description edge cases. The goal is to provide candidates with actionable feedback rather than opaque predictions.

---

## Future Improvements

- Required vs nice-to-have weighting
- Experience overlap handling
- Resume feedback suggestions
- Skill gap learning recommendations
- Confidence calibration for scores
- Expanded skill ontology

---

## License

MIT License
