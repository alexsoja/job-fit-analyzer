from __future__ import annotations

import argparse
from pathlib import Path

from jobfit.analyze import analyze
from jobfit.ingest.pdf_extract import extract_text_from_pdf


def read_input_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)

    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise SystemExit(f"File not found: {path}") from e
    except UnicodeDecodeError as e:
        raise SystemExit(f"Could not read {path} as UTF-8 text.") from e


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobfit",
        description="Job Fit Analyzer: compare a resume and job description.",
    )
    parser.add_argument("--resume", required=True, type=Path, help="Path to resume (.txt or .pdf).")
    parser.add_argument("--jd", required=True, type=Path, help="Path to job description (.txt).")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    resume_text = read_input_file(args.resume)
    jd_text = read_input_file(args.jd)

    result = analyze(resume_text, jd_text)

    print("Loaded inputs successfully.")
    print(f"Resume characters: {len(resume_text)}")
    print(f"Job description characters: {len(jd_text)}")

    print("\n--- Preview BEFORE normalize (first 120 chars) ---")
    print("RESUME:", result["previews"]["resume_before"])
    print("JD:", result["previews"]["jd_before"])

    print("\n--- Preview AFTER normalize (first 120 chars) ---")
    print("RESUME:", result["previews"]["resume_after"])
    print("JD:", result["previews"]["jd_after"])

    print("\n--- Skill Matching ---")
    print("Resume skills:", result["skills"]["resume_skills"])
    print("JD skills:", result["skills"]["jd_skills"])
    print("Matched skills:", result["skills"]["matched"])
    print("Missing skills:", result["skills"]["missing"])

    print("\n--- Score ---")
    s = result["score"]
    print(f"Skills score: {s['skills_points']}/{s['skills_max']}")
    print(f"Total score: {s['total_points']}/{s['total_max']} ({s['note']})")

    print("\n--- Requirement coverage (skills-based) ---")
    cov = result["requirements"]["coverage"]
    if not cov:
        print("No requirement lines matched to known skills yet.")
    else:
        for item in cov[:10]:
            print(f"- {item['line']}")
            if item["matched"]:
                print(f"  matched: {item['matched']}")
            if item["missing"]:
                print(f"  missing: {item['missing']}")


if __name__ == "__main__":
    main()
