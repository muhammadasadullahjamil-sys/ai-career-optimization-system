import re


class ResumePreprocessor:
    """Cleans and normalizes raw resume text."""

    @staticmethod
    def prepare(raw_text: str) -> str:
        """
        Normalizes whitespace, bullets, punctuation, and removes noise.
        """

        if not raw_text:
            return ""

        text = raw_text

        # Normalize whitespace
        text = text.replace('\r', '\n')
        text = re.sub(r'\n{2,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        # Normalize bullet points
        text = re.sub(r'[\u2022•*]\s+', '- ', text)
        text = re.sub(r'^\s*-\s*', '- ', text, flags=re.MULTILINE)

        # Remove page numbers and decorative separators
        text = re.sub(r'Page\s*\d+\s*of\s*\d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'[-=_]{3,}', '', text)

        # Normalize quotes and hyphens
        text = text.replace('“', '"').replace('”', '"')
        text = text.replace('‘', "'").replace('’', "'")
        text = text.replace('–', '-').replace('—', '-')

        # Remove non-printable characters
        text = ''.join(c for c in text if c.isprintable() or c == '\n')

        # Trim leading and trailing whitespace
        text = text.strip()

        return text
