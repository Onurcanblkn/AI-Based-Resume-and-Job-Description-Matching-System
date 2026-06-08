import re
import textwrap
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextProcessor:
    def __init__(self, raw_text: str = ""):
        self.raw_text = raw_text
        self.clean_text = ""

    def preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def get_clean_text(self) -> str:
        self.clean_text = self.preprocess(self.raw_text)
        return self.clean_text


class ResumeParser(TextProcessor):
    def __init__(self, pdf_file=None):
        super().__init__()
        self.pdf_file = pdf_file

    def extract_text(self) -> str:
        text = ""
        with fitz.open(stream=self.pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        self.raw_text = text
        return text


class JobDescriptionParser(TextProcessor):
    def __init__(self, raw_text: str = ""):
        super().__init__(raw_text)


class SkillExtractor:
    DEFAULT_SKILLS = [
        "python", "java", "c#", "c++", "javascript", "typescript",
        "react", "angular", "vue", "node.js", "django", "flask",
        "spring boot", "sql", "postgresql", "mysql", "mongodb",
        "docker", "kubernetes", "git", "github", "linux", "aws",
        "azure", "gcp", "rest api", "graphql", "machine learning",
        "deep learning", "data analysis", "pandas", "numpy", "opencv",
        "tensorflow", "pytorch", "scikit-learn", "html", "css",
        "nlp", "tableau", "power bi", "excel", "spark", "hadoop",
    ]

    def __init__(self, skill_list=None):
        self.skill_list = skill_list if skill_list else self.DEFAULT_SKILLS

    def extract(self, clean_text: str) -> set:
        found = set()
        for skill in self.skill_list:
            pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
            if re.search(pattern, clean_text):
                found.add(skill)
        return found


class MatchAnalyzer:
    def __init__(self, resume_clean: str, job_clean: str,
                 resume_skills: set, job_skills: set):
        self.resume_clean = resume_clean
        self.job_clean = job_clean
        self.resume_skills = resume_skills
        self.job_skills = job_skills

    def matched_skills(self) -> set:
        return self.resume_skills & self.job_skills

    def missing_skills(self) -> set:
        return self.job_skills - self.resume_skills

    def skill_match_score(self) -> float:
        if not self.job_skills:
            return 0.0
        return len(self.matched_skills()) / len(self.job_skills) * 100

    def text_similarity_score(self) -> float:
        if not self.resume_clean.strip() or not self.job_clean.strip():
            return 0.0
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([self.resume_clean, self.job_clean])
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(sim) * 100

    def overall_score(self) -> float:
        return self.skill_match_score() * 0.7 + self.text_similarity_score() * 0.3

    def recommendation(self) -> str:
        missing = sorted(self.missing_skills())
        matched = sorted(self.matched_skills())
        overall = self.overall_score()

        if not self.job_skills:
            return "No recognizable skills were found in the job description."

        if not missing:
            return (f"Excellent! Your resume covers all the required skills in "
                    f"this job posting. Overall match: {overall:.0f}%.")

        msg = f"Your resume matches this job at {overall:.0f}%. "
        if matched:
            msg += "Your strengths are " + ", ".join(matched) + ". "
        msg += ("To strengthen your resume, consider adding or improving the "
                "following skills: " + ", ".join(missing) + ".")
        return msg


THEMES = {
    "Dark": {
        "background": "#0f172a",
        "surface": "#111827",
        "surface_alt": "#1f2937",
        "text": "#e2e8f0",
        "muted": "#94a3b8",
        "border": "rgba(148,163,184,0.22)",
        "input": "#111827",
        "input_text": "#e5e7eb",
        "hero_start": "#2563eb",
        "hero_mid": "#7c3aed",
        "hero_end": "#db2777",
        "shadow": "rgba(15,23,42,0.45)",
        "matched_text": "#4ade80",
        "missing_text": "#f87171",
        "rec_bg": "rgba(124,58,237,0.14)",
        "rec_border": "rgba(139,92,246,0.42)",
    },
    "Light": {
        "background": "#f8fafc",
        "surface": "#ffffff",
        "surface_alt": "#eef2ff",
        "text": "#111827",
        "muted": "#64748b",
        "border": "rgba(100,116,139,0.24)",
        "input": "#ffffff",
        "input_text": "#111827",
        "hero_start": "#0ea5e9",
        "hero_mid": "#6366f1",
        "hero_end": "#14b8a6",
        "shadow": "rgba(15,23,42,0.12)",
        "matched_text": "#15803d",
        "missing_text": "#b91c1c",
        "rec_bg": "rgba(99,102,241,0.08)",
        "rec_border": "rgba(99,102,241,0.25)",
    },
}


def get_theme_css(theme_name: str) -> str:
    theme = THEMES[theme_name]
    css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: {theme["background"]}; color: {theme["text"]}; }
.block-container { padding-top: 1.25rem; max-width: 1100px; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {
  display: none;
}

.theme-panel {
  background: {theme["surface"]}; border: 1px solid {theme["border"]};
  border-radius: 12px; padding: 14px 18px; margin: -8px 0 24px 0;
  box-shadow: 0 10px 24px {theme["shadow"]};
}
.theme-panel-title {
  color: {theme["text"]}; font-size: 14px; font-weight: 800;
  margin-bottom: 6px;
}

.hero {
  background: linear-gradient(135deg, {theme["hero_start"]} 0%, {theme["hero_mid"]} 52%, {theme["hero_end"]} 100%);
  padding: 34px 38px; border-radius: 14px; margin-bottom: 28px;
  box-shadow: 0 14px 32px {theme["shadow"]};
}
.hero h1 { color: #fff; font-size: 34px; font-weight: 800; margin: 0; }
.hero p { color: rgba(255,255,255,0.9); font-size: 16px; margin: 8px 0 0 0; }
.hero .tag {
  display: inline-block; background: rgba(255,255,255,0.18); color: #fff;
  padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 600;
  margin-bottom: 14px;
}

.score-card {
  border-radius: 12px; padding: 22px; text-align: center; color: #fff;
  box-shadow: 0 10px 24px {theme["shadow"]};
}
.score-card .label { font-size: 13px; font-weight: 600; opacity: .9; text-transform: uppercase; }
.score-card .value { font-size: 40px; font-weight: 800; margin-top: 6px; }
.sc-blue   { background: linear-gradient(135deg,#0ea5e9,#2563eb); }
.sc-purple { background: linear-gradient(135deg,#8b5cf6,#7c3aed); }
.sc-green  { background: linear-gradient(135deg,#10b981,#16a34a); }

.chip {
  display: inline-block; padding: 7px 14px; margin: 5px; border-radius: 8px;
  font-size: 14px; font-weight: 600;
}
.chip-matched { background: rgba(34,197,94,0.14); color: {theme["matched_text"]}; border: 1px solid rgba(34,197,94,0.55); }
.chip-missing { background: rgba(239,68,68,0.11); color: {theme["missing_text"]}; border: 1px solid rgba(239,68,68,0.5); }
.empty-chip { color: {theme["muted"]}; }

.section-title { font-size: 20px; font-weight: 800; margin: 26px 0 10px 0; color: {theme["text"]}; }

.rec-box {
  background: {theme["rec_bg"]}; border: 1px solid {theme["rec_border"]};
  border-radius: 12px; padding: 20px 22px; color: {theme["text"]};
  font-size: 15px; line-height: 1.6;
}

.stButton > button, .stDownloadButton > button {
  background: linear-gradient(135deg,{theme["hero_mid"]},{theme["hero_end"]});
  color: #fff; border: none; border-radius: 10px; padding: 12px 0;
  font-size: 16px; font-weight: 700; width: 100%;
  box-shadow: 0 8px 18px {theme["shadow"]};
}
.stButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.06); color: #fff;
}

div[data-testid="stFileUploader"], div[data-testid="stTextArea"] textarea {
  background: {theme["input"]}; color: {theme["input_text"]};
}
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploaderDropzone"] {
  background: {theme["surface"]};
  border: 1px solid {theme["border"]};
  border-radius: 10px;
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] section *,
div[data-testid="stFileUploaderDropzone"] * {
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploaderDropzone"] small {
  color: {theme["muted"]};
}
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploaderDropzone"] button {
  background: {theme["surface_alt"]};
  border: 1px solid {theme["border"]};
  color: {theme["text"]};
  border-radius: 8px;
  font-weight: 700;
}
div[data-testid="stFileUploader"] button *,
div[data-testid="stFileUploaderDropzone"] button * {
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] svg,
div[data-testid="stFileUploaderDropzone"] svg {
  color: {theme["text"]};
  fill: currentColor;
}
div[data-testid="stTextArea"] textarea {
  border: 1px solid {theme["border"]}; border-radius: 10px;
}
div[data-testid="stMarkdownContainer"] p, label, .stRadio label {
  color: {theme["text"]};
}
div[role="radiogroup"] {
  gap: 12px;
}
div[role="radiogroup"] label {
  background: {theme["surface_alt"]}; border: 1px solid {theme["border"]};
  border-radius: 8px; padding: 8px 12px; margin-right: 8px;
}
</style>
"""
    for key, value in theme.items():
        css = css.replace('{theme["' + key + '"]}', value)
    return css


def score_card(label: str, value: float, css_class: str) -> str:
    return (f'<div class="score-card {css_class}">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value:.0f}%</div></div>')


def chips(skills, css_class: str) -> str:
    if not skills:
        return '<span class="empty-chip">None</span>'
    return "".join(f'<span class="chip {css_class}">{s}</span>'
                   for s in sorted(skills))


def build_gauge(score: float, theme_name: str) -> go.Figure:
    theme = THEMES[theme_name]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"color": theme["text"], "size": 34}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.25)"},
                {"range": [40, 70], "color": "rgba(234,179,8,0.25)"},
                {"range": [70, 100], "color": "rgba(34,197,94,0.25)"},
            ],
        },
    ))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      font={"color": theme["text"]},
                      margin=dict(l=30, r=30, t=30, b=10))
    return fig


def build_bar(matched, missing, theme_name: str) -> go.Figure:
    theme = THEMES[theme_name]
    fig = go.Figure(go.Bar(
        x=["Matched", "Missing"],
        y=[len(matched), len(missing)],
        marker_color=["#22c55e", "#ef4444"],
        text=[len(matched), len(missing)],
        textposition="outside",
        textfont={"color": theme["text"], "size": 16},
    ))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font={"color": theme["text"]},
                      yaxis={"gridcolor": "rgba(148,163,184,0.2)",
                             "title": "Number of skills"},
                      margin=dict(l=20, r=20, t=30, b=20))
    return fig


def build_pdf_report(skill_score: float, text_score: float, overall: float,
                     matched, missing, recommendation: str, job_skills,
                     resume_skills) -> bytes:
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    margin = 50
    y = 50

    def add_line(text: str, size: int = 11, bold: bool = False,
                 gap: int = 18):
        nonlocal y, page
        if y > 790:
            page = doc.new_page(width=595, height=842)
            y = 50
        font = "Helvetica-Bold" if bold else "Helvetica"
        page.insert_text((margin, y), text, fontsize=size, fontname=font,
                         color=(0.12, 0.16, 0.24))
        y += gap

    def y_gap(amount: int = 10):
        nonlocal y
        y += amount

    def add_wrapped(title: str, value: str):
        add_line(title, 13, True, 20)
        for line in textwrap.wrap(value or "None", width=82):
            add_line(line, 10, False, 14)
        y_gap()

    add_line("Resume Analyzer and Job Matching System", 18, True, 28)
    add_line("Match Report", 13, True, 24)

    add_line(f"Skill Match Score: {skill_score:.0f}%", 12)
    add_line(f"Text Similarity Score: {text_score:.0f}%", 12)
    add_line(f"Overall Match Score: {overall:.0f}%", 12)
    y_gap()

    add_wrapped("Matched Skills", ", ".join(sorted(matched)))
    add_wrapped("Missing Skills", ", ".join(sorted(missing)))
    add_wrapped("Recommendation", recommendation)

    add_line("Job Skills Summary", 13, True, 20)
    for skill in sorted(job_skills):
        status = "Yes" if skill in resume_skills else "No"
        add_line(f"- {skill}: In Resume = {status}", 10, False, 14)

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def main():
    st.set_page_config(page_title="Resume Analyzer & Job Matcher",
                       page_icon="\U0001F4C4", layout="wide")
    theme_name = st.session_state.get("theme_choice", "Dark")
    st.markdown(get_theme_css(theme_name), unsafe_allow_html=True)

    st.markdown(
        '<div class="hero">'
        '<span class="tag">SEN 4015 - Advanced Python Programming</span>'
        '<h1>Resume Analyzer and Job Matching System</h1>'
        '<p>Upload your resume and paste a job description to see your match '
        'score, matched and missing skills, and tailored recommendations.</p>'
        '</div>', unsafe_allow_html=True)

    st.markdown('<div class="theme-panel"><div class="theme-panel-title">'
                'Theme Settings</div>', unsafe_allow_html=True)
    theme_name = st.radio(
        "Theme",
        ["Dark", "Light"],
        key="theme_choice",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">1. Upload Resume (PDF)</div>',
                    unsafe_allow_html=True)
        pdf_file = st.file_uploader("", type=["pdf"])
    with col2:
        st.markdown('<div class="section-title">2. Job Description</div>',
                    unsafe_allow_html=True)
        job_text = st.text_area("", height=200,
                                placeholder="Paste the job description here...")

    analyze = st.button("Analyze Resume")

    if analyze:
        if pdf_file is None or not job_text.strip():
            st.warning("Please upload a resume (PDF) and enter a job description.")
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

        st.markdown('<div class="section-title">Results</div>',
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
            st.markdown('<div class="section-title">Overall Match</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_gauge(overall, theme_name),
                            use_container_width=True)
        with g2:
            st.markdown('<div class="section-title">Skills Breakdown</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(build_bar(matched, missing, theme_name),
                            use_container_width=True)

        st.markdown('<div class="section-title">\u2705 Matched Skills</div>',
                    unsafe_allow_html=True)
        st.markdown(chips(matched, "chip-matched"), unsafe_allow_html=True)

        st.markdown('<div class="section-title">\u274C Missing Skills</div>',
                    unsafe_allow_html=True)
        st.markdown(chips(missing, "chip-missing"), unsafe_allow_html=True)

        st.markdown('<div class="section-title">\U0001F4A1 Recommendation</div>',
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
            st.download_button("Download results as CSV",
                               df.to_csv(index=False).encode("utf-8"),
                               "match_results.csv", "text/csv")
        with d2:
            st.download_button("Download results as PDF",
                               pdf_report,
                               "match_report.pdf", "application/pdf")


if __name__ == "__main__":
    main()
