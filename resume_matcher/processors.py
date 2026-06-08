import re

import fitz


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
