import pandas as pd
import streamlit as st

from resume_matcher.analyzer import MatchAnalyzer
from resume_matcher.processors import JobDescriptionParser, ResumeParser
from resume_matcher.reports import build_pdf_report
from resume_matcher.skills import SkillExtractor
from resume_matcher.themes import get_theme_css
from resume_matcher.visualizations import (
    build_bar,
    build_gauge,
    chips,
    score_card,
)


def render_app():
    st.set_page_config(page_title="Resume Match Intelligence",
                       layout="wide")
    theme_name = st.session_state.get("theme_choice", "Dark")
    st.markdown(get_theme_css(theme_name), unsafe_allow_html=True)

    st.markdown(
        '<div class="app-header"><div class="brand-block">'
        '<div class="brand-title">Resume Match Intelligence</div>'
        '<div class="brand-subtitle">Candidate-to-role fit analysis</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero">'
        '<span class="tag">AI Resume Screening</span>'
        '<h1>Evaluate candidate fit with skill and text intelligence</h1>'
        '<p>Compare a resume against a job description, identify matched and '
        'missing capabilities, and export a concise hiring report.</p>'
        '</div>', unsafe_allow_html=True)

    st.markdown('<div class="theme-panel"><div class="theme-panel-title">'
                'Appearance</div>', unsafe_allow_html=True)
    theme_name = st.radio(
        "Theme",
        ["Dark", "Light"],
        key="theme_choice",
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="workflow-row">'
        '<div class="workflow-item"><div class="workflow-label">Step 01</div>'
        '<div class="workflow-title">Upload resume</div></div>'
        '<div class="workflow-item"><div class="workflow-label">Step 02</div>'
        '<div class="workflow-title">Add job description</div></div>'
        '<div class="workflow-item"><div class="workflow-label">Step 03</div>'
        '<div class="workflow-title">Review match report</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Resume Document</div>',
                    unsafe_allow_html=True)
        pdf_file = st.file_uploader("", type=["pdf"])
    with col2:
        st.markdown('<div class="section-title">Job Description</div>',
                    unsafe_allow_html=True)
        job_text = st.text_area("", height=200,
                                placeholder="Paste the job description here...")

    analyze = st.button("Analyze Candidate Fit")

    if analyze:
        if pdf_file is None or not job_text.strip():
            st.warning("Upload a resume PDF and enter a job description.")
            return

        resume_parser = ResumeParser(pdf_file)
        resume_parser.extract_text()
        resume_clean = resume_parser.get_clean_text()

        job_parser = JobDescriptionParser(job_text)
        job_clean = job_parser.get_clean_text()

        extractor = SkillExtractor()
        resume_skills = extractor.extract(resume_clean)
        job_skills = extractor.extract(job_clean)

        analyzer = MatchAnalyzer(resume_clean, job_clean,
                                 resume_skills, job_skills)

        skill_score = analyzer.skill_match_score()
        text_score = analyzer.text_similarity_score()
        overall = analyzer.overall_score()
        matched = analyzer.matched_skills()
        missing = analyzer.missing_skills()

        st.markdown('<div class="section-title">Match Overview</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(score_card("Skill Match", skill_score, "sc-blue"),
                    unsafe_allow_html=True)
        c2.markdown(score_card("Text Similarity", text_score, "sc-purple"),
                    unsafe_allow_html=True)
        c3.markdown(score_card("Overall Match", overall, "sc-green"),
                    unsafe_allow_html=True)

        g1, g2 = st.columns(2)
        with g1:
            st.markdown('<div class="section-title">Overall Score</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_gauge(overall, theme_name),
                            use_container_width=True)
        with g2:
            st.markdown('<div class="section-title">Skill Coverage</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_bar(matched, missing, theme_name),
                            use_container_width=True)

        st.markdown('<div class="section-title">Matched Skills</div>',
                    unsafe_allow_html=True)
        st.markdown(chips(matched, "chip-matched"), unsafe_allow_html=True)

        st.markdown('<div class="section-title">Missing Skills</div>',
                    unsafe_allow_html=True)
        st.markdown(chips(missing, "chip-missing"), unsafe_allow_html=True)

        st.markdown('<div class="section-title">Recommendation</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="rec-box">{analyzer.recommendation()}</div>',
                    unsafe_allow_html=True)

        df = pd.DataFrame({
            "Job Skill": sorted(job_skills),
            "In Resume": ["Yes" if s in resume_skills else "No"
                          for s in sorted(job_skills)],
        })
        pdf_report = build_pdf_report(
            skill_score, text_score, overall, matched, missing,
            analyzer.recommendation(), job_skills, resume_skills
        )

        st.write("")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button("Download CSV",
                               df.to_csv(index=False).encode("utf-8"),
                               "match_results.csv", "text/csv")
        with d2:
            st.download_button("Download PDF Report",
                               pdf_report,
                               "match_report.pdf", "application/pdf")
