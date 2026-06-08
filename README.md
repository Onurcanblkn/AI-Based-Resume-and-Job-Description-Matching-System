# Resume Analyzer and Job Matching System

AI-based resume and job description matching system using NLP and TF-IDF.

## Features

- Upload a resume as PDF and paste a job description
- Extracts skills from both using a predefined skill database
- Calculates **Skill Match Score**, **Text Similarity Score** (TF-IDF + Cosine Similarity), and **Overall Match Score**
- Shows matched and missing skills as visual tags
- Generates a personalized recommendation
- Download results as CSV

## Technologies

| Library | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| PyMuPDF | PDF text extraction |
| scikit-learn | TF-IDF vectorizer + cosine similarity |
| pandas | Data handling |
| plotly | Charts and gauge |

## OOP Architecture

- `TextProcessor` — base class for text preprocessing
- `ResumeParser(TextProcessor)` — extracts text from PDF
- `JobDescriptionParser(TextProcessor)` — processes job description input
- `SkillExtractor` — finds skills using regex matching
- `MatchAnalyzer` — computes all scores and recommendation

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
