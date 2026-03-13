from fastapi import UploadFile, HTTPException
from pathlib import Path

# Allowed File Types Configuration
ALLOWED_FILE_TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

# Maximum allowed resume file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


class ResumeValidator:
    """Validates uploaded resume files."""

    @staticmethod
    async def validate(resume: UploadFile):
        """
        Performs layered validation:
        - Extension check
        - MIME type validation
        - File size enforcement
        - Magic number verification
        Returns raw file bytes and file extension.
        """

        if not resume.filename:
            raise HTTPException(
                status_code=400,
                detail="Missing filename."
            )

        # Extension Validation
        file_extension = Path(resume.filename.lower()).suffix

        if file_extension not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Only PDF and DOCX are allowed."
            )

        # MIME Type Validation
        expected_mime = ALLOWED_FILE_TYPES[file_extension]
        if resume.content_type != expected_mime:
            raise HTTPException(
                status_code=400,
                detail="MIME type does not match file extension."
            )

        # File Size Validation
        resume.file.seek(0, 2)
        file_size = resume.file.tell()
        resume.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum allowed size (5 MB)."
            )

        # File Signature Validation
        header = await resume.read(8)
        resume.file.seek(0)

        if file_extension == ".pdf":
            if not header.startswith(b"%PDF"):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid PDF file signature."
                )

        elif file_extension == ".docx":
            if not header.startswith(b"PK"):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid DOCX file signature."
                )

        # Read full file after all checks pass
        file_bytes = await resume.read()

        return file_bytes, file_extension
