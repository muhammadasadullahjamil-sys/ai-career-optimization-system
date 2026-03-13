from fastapi import HTTPException
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO


class ResumeParser:
    """Extracts raw text from resume files."""

    @staticmethod
    def extract_text(file_bytes: bytes, file_extension: str) -> str:
        """
        Routes text extraction based on file extension.
        """

        if file_extension == ".pdf":
            return ResumeParser.extract_pdf_text(file_bytes)

        if file_extension == ".docx":
            return ResumeParser.extract_docx_text(file_bytes)

        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    @staticmethod
    def extract_pdf_text(file_bytes: bytes) -> str:
        """
        Extracts text from PDF resumes using PyMuPDF.
        """

        try:
            text = ""

            with fitz.open(stream=BytesIO(file_bytes), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()

            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="No readable text found in the PDF resume."
                )

            return text

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Failed to process PDF file."
            )

    @staticmethod
    def extract_docx_text(file_bytes: bytes) -> str:
        """
        Extracts text from DOCX resumes using python-docx.
        """

        try:
            document = Document(BytesIO(file_bytes))
            text = ""

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="No readable text found in the DOCX resume."
                )

            return text

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Failed to process DOCX file."
            )
