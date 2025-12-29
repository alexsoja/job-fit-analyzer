# Job Fit Analyzer

A Python project that evaluates how well a resume matches a job description.
The tool compares skills, education, and experience to produce a fit score out of 100,
along with matched and missing areas.

## Features
- Resume PDF parsing
- Job description analysis
- Skill and requirement matching
- Weighted fit score (/100)
- Breakdown of matched and missing areas

## Tech Stack
- Python
- PDF parsing (pypdf / pdfplumber)
- Text processing (regex, NLP utilities)
- Optional: sentence embeddings for semantic matching

## How It Works
1. Extracts text from a resume PDF
2. Parses requirements from a job description
3. Matches skills, education, and experience
4. Computes a weighted fit score
5. Outputs matched and missing areas

## Project Status
🚧 In progress — MVP under development

## Future Improvements
- Semantic matching using embeddings
- Streamlit web interface
- Resume feedback suggestions
