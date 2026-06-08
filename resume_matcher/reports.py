import textwrap

import fitz


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
