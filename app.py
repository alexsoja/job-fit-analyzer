from __future__ import annotations

import html
import tempfile
from pathlib import Path

import streamlit as st

from jobfit.analyze import analyze
from jobfit.ingest.pdf_extract import extract_text_from_pdf


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Job Fit Analyst",
    page_icon="🧠",
    layout="wide",
)


# -----------------------------
# CSS (theme + cards + typography)
# -----------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.3rem; padding-bottom: 2rem; max-width: 1400px; }

    /* Big center script title */
    .jf-title {
        text-align: center;
        font-size: 3.6rem;
        font-weight: 100;
        letter-spacing: -0.03em;
        margin: 0.3rem 0 1rem 0;
        font-family: "Brush Script MT", "Segoe Script", "Snell Roundhand", cursive;
        color: rgba(255,255,255,0.95);
        text-shadow: 0 12px 35px rgba(0,0,0,0.55);
    }

    /* Divider line under title */
    .jf-divider {
        height: 1px;
        background: rgba(255,255,255,0.10);
        margin: 0.6rem 0 1.2rem 0;
    }

    /* Right-side overall card */
    .jf-card {
        padding: 1.15rem 1.15rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.04);
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        margin-bottom: 1.2rem;
    }

    /* Category cards (big boxes) */
    .jf-cat {
        padding: 0;
        border-radius: 18px;
        border: 2px solid rgba(255,255,255,0.75);
        background: rgba(0,0,0,0.08);
        box-shadow: 0 18px 40px rgba(0,0,0,0.40);
        overflow: hidden;
        min-height: 360px;
    }

    .jf-cat-head {
        padding: 0.9rem 1.1rem;
        border-bottom: 2px solid rgba(255,255,255,0.75);
        text-align: center;
        font-size: 2.2rem;
        font-family: "Brush Script MT", "Segoe Script", "Snell Roundhand", cursive;
        color: rgba(255,255,255,0.95);
    }

    .jf-cat-body {
        padding: 1.1rem 1.2rem 1.2rem 1.2rem;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .jf-label { font-weight: 800; margin-top: 0.2rem; margin-bottom: 0.4rem; }
    .jf-good { color: rgba(140, 255, 170, 0.95); }
    .jf-bad  { color: rgba(255, 140, 140, 0.95); }

    .jf-list { margin: 0.2rem 0 1.0rem 0; padding-left: 1.2rem; }
    .jf-list li { margin: 0.25rem 0; }

    /* Small pills */
    .jf-pill {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 0.95rem;
        margin-right: 0.35rem;
    }

    /* Score bar */
    .score-bar {
        position: relative;
        height: 22px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        overflow: hidden;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.35);
    }
    .score-fill {
        height: 100%;
        border-radius: 999px;
        position: relative;
        box-shadow:
            inset 0 2px 0 rgba(255,255,255,0.35),
            inset 0 -2px 0 rgba(0,0,0,0.25),
            0 10px 20px rgba(0,0,0,0.25);
    }
    .score-fill::before {
        content: "";
        position: absolute;
        left: 0; right: 0; top: 0;
        height: 55%;
        background: linear-gradient(
            to bottom,
            rgba(255,255,255,0.45),
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.0)
        );
    }
    .score-fill::after {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(circle at 10% 30%, rgba(255,255,255,0.45) 0 2px, transparent 3px),
            radial-gradient(circle at 35% 70%, rgba(255,255,255,0.35) 0 1.5px, transparent 3px),
            radial-gradient(circle at 60% 35%, rgba(255,255,255,0.40) 0 2px, transparent 3px),
            radial-gradient(circle at 85% 60%, rgba(255,255,255,0.30) 0 1.5px, transparent 3px);
        opacity: 0.6;
        transform: translateX(-30%);
        animation: shimmer 2.2s linear infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-40%); }
        100% { transform: translateX(40%); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Helpers
# -----------------------------
def score_style(score: int) -> tuple[str, str]:
    if score < 25:
        return "Low", "linear-gradient(90deg, #ff3b3b, #b30000)"
    if score < 40:
        return "Needs work", "linear-gradient(90deg, #ff7a18, #d14b00)"
    if score < 70:
        return "Fair", "linear-gradient(90deg, #ffd000, #caa300)"
    if score < 90:
        return "Strong", "linear-gradient(90deg, #1dd75f, #0f8a3a)"
    return "Excellent", "linear-gradient(90deg, #7c3aed, #22c55e, #fbbf24)"


def render_score_bar(score: int) -> None:
    score = max(0, min(100, int(score)))
    label, grad = score_style(score)

    st.markdown(
        f"""
        <div class="score-bar">
            <div class="score-fill" style="width:{score}%; background:{grad};"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:0.45rem;">
            <div class="jf-pill"><b>{score}</b>/100</div>
            <div class="jf-pill">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bullets(items: list[str]) -> str:
    if not items:
        return "<ul class='jf-list'><li>-</li></ul>"
    li = "".join(f"<li>{html.escape(str(x))}</li>" for x in items)
    return f"<ul class='jf-list'>{li}</ul>"


def render_category_card(title: str, matched: list[str], missing: list[str]) -> None:
    st.markdown(
        f"""
        <div class="jf-cat">
            <div class="jf-cat-head">{html.escape(title)}</div>
            <div class="jf-cat-body">
                <div class="jf-label jf-good">Matched {html.escape(title)}:</div>
                {bullets(matched)}
                <div class="jf-label jf-bad">Missing {html.escape(title)}</div>
                {bullets(missing)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# State
# -----------------------------
if "result" not in st.session_state:
    st.session_state["result"] = None


# -----------------------------
# Title
# -----------------------------
st.markdown("<div class='jf-title'>Job Fit Analyst</div>", unsafe_allow_html=True)
st.markdown("<div class='jf-divider'></div>", unsafe_allow_html=True)


# -----------------------------
# Top row layout: inputs center + overall right
# -----------------------------
left, mid, right = st.columns([1.2, 2.6, 1.6], gap="large")

with mid:
    resume_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    jd_text_input = st.text_area(
        "Paste job description",
        height=220,
        placeholder="Paste the job description here...",
    )

    if st.button("Analyze"):
        if resume_file is None or not jd_text_input.strip():
            st.error("Please upload a resume and paste a job description.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume_file.read())
                pdf_path = Path(tmp.name)

            resume_text = extract_text_from_pdf(pdf_path)
            st.session_state["result"] = analyze(resume_text, jd_text_input)

with right:
    st.markdown("<div class='jf-card'>", unsafe_allow_html=True)
    st.subheader("Overall Fit")

    result = st.session_state["result"]
    if result is None:
        st.caption("Upload a resume and paste a job description to see results.")
    else:
        s = result["score"]
        render_score_bar(s["total_points"])

        m1, m2, m3 = st.columns(3)
        m1.metric("Skills", f"{s['skills_points']}/{s['skills_max']}")
        m2.metric("Education", f"{s['education_points']}/{s['education_max']}")
        m3.metric("Experience", f"{s['experience_points']}/{s['experience_max']}")
        st.caption(s["note"])

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Bottom row: 3 big category cards
# -----------------------------
result = st.session_state["result"]
if result is not None:
    edu = result["education"]
    skills = result["skills"]
    exp = result["experience"]

    # Education summary strings
    edu_matched: list[str] = []
    edu_missing: list[str] = []

    jd_deg = (edu.get("jd_degree") or "none").lower()
    res_deg = (edu.get("resume_degree") or "none").lower()

    if jd_deg == "none":
        edu_matched.append("No degree requirement listed")
    else:
        if jd_deg == res_deg:
            edu_matched.append(f"Degree level: {res_deg}")
        else:
            edu_missing.append(f"Degree level: expected {jd_deg}")

    for m in edu.get("matched_majors", []) or []:
        edu_matched.append(f"Major: {m}")
    for m in edu.get("missing_majors", []) or []:
        edu_missing.append(f"Major: {m}")

    # Experience summary strings
    exp_matched: list[str] = []
    exp_missing: list[str] = []

    jd_req = exp.get("jd_years_required", None)
    have = float(exp.get("resume_years_estimate", 0.0))

    if jd_req is None:
        exp_matched.append("No years requirement listed")
    else:
        req = float(jd_req)
        if have >= req:
            exp_matched.append(f"{have:.1f} yrs vs required {req:.1f} yrs")
        else:
            exp_missing.append(f"{have:.1f} yrs vs required {req:.1f} yrs")

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        render_category_card("Education", edu_matched, edu_missing)
    with c2:
        render_category_card("Skills", skills.get("matched", []), skills.get("missing", []))
    with c3:
        render_category_card("Experience", exp_matched, exp_missing)
