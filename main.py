from fastapi import FastAPI, UploadFile, File, Query
from resume_validator import ResumeValidator
from resume_parser import ResumeParser
from resume_preprocessor import ResumePreprocessor
from llm_resume_parser import LLMResumeParser
from market_role_adapter import MarketRoleAdapter
from job_data_collector import JobDataCollector


# FastAPI application instance
app = FastAPI(title="AI-Assisted Market-Driven Career Optimization System")

# LLM resume parser instance
llm_resume_parser = LLMResumeParser()


@app.post("/upload-resume/")
async def upload_resume(resume: UploadFile = File(...)):
    """
    Uploads a resume and processes it through the full pipeline.
    """

    # Validate resume file
    file_bytes, file_extension = await ResumeValidator.validate(resume)

    # Extract raw text from file
    raw_text = ResumeParser.extract_text(file_bytes, file_extension)

    # Normalize extracted text
    normalized_text = ResumePreprocessor.prepare(raw_text)

    # Parse structured resume data using LLM
    parsed_resume = llm_resume_parser.parse_resume(normalized_text)

    return {
        "filename": resume.filename,
        "content_type": resume.content_type,
        "file_size_in_bytes": len(file_bytes),
        "file_format": file_extension,
        "message": "Resume uploaded successfully",
        "normalized_text": normalized_text,
        "parsed_resume": parsed_resume
    }


@app.get("/jobs/search")
def search_jobs(
    query: str = Query(..., description="Job search keyword")
):
    jobs = JobDataCollector.fetch_jobs(query)

    return {
        "query": query,
        "jobs_returned": len(jobs),
        "jobs": jobs
    }


@app.post("/analyze-resume-market/")
async def analyze_resume_market(resume: UploadFile = File(...)):
    """
    Full pipeline:
    - Upload resume
    - Parse with LLM
    - Extract job keywords
    - Fetch Adzuna job data
    - Return combined analysis
    """

    # Validate resume
    file_bytes, file_extension = await ResumeValidator.validate(resume)

    # Extract text
    raw_text = ResumeParser.extract_text(file_bytes, file_extension)

    # Normalize text
    normalized_text = ResumePreprocessor.prepare(raw_text)

    # Parse resume via LLM
    parsed_resume = llm_resume_parser.parse_resume(normalized_text)

    # If parsing failed
    if "error" in parsed_resume:
        return {
            "status": "error",
            "message": "Resume parsing failed",
            "details": parsed_resume
        }

    # Extract role keywords from parsed resume
    keywords = parsed_resume.get("job_search_keywords", [])

    # Normalize all roles at once
    normalized_roles = MarketRoleAdapter.normalize_roles(keywords)

    market_data = {}

    for role in normalized_roles:
        query = MarketRoleAdapter.prepare_for_query(role)

        jobs = JobDataCollector.fetch_jobs(query)

        market_data[role] = {
            "jobs_found": len(jobs),
            "jobs": jobs
        }

    # Return unified response
    return {
        "status": "success",
        "file_info": {
            "filename": resume.filename,
            "content_type": resume.content_type,
            "file_size_in_bytes": len(file_bytes),
            "file_format": file_extension
        },
        "parsed_resume": parsed_resume,
        "market_analysis": {
            "roles_analyzed": keywords,
            "job_data": market_data
        }
    }