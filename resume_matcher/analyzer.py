from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
