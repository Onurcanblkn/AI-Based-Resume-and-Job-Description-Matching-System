import re


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
