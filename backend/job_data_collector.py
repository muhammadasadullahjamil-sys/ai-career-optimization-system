import requests
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class JobDataCollector:
    # ADZUNA API Configuration
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
    ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")
    JOB_DATABASE_NAME = os.getenv("JOB_DATABASE_NAME", "job_market.db")

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError("Adzuna API credentials are not set in environment variables.")

    BASE_URL = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/1"

    @classmethod
    def initialize_database(cls):
        conn = sqlite3.connect(cls.JOB_DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                adzuna_job_id TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                description TEXT,
                salary_min REAL,
                salary_max REAL,
                apply_link TEXT,
                fetched_at TEXT,
                UNIQUE(adzuna_job_id)
            )
        """)

        conn.commit()
        conn.close()

    # Fetch Jobs From API
    @classmethod
    def fetch_jobs_from_api(cls, keyword: str):

        params = {
            "app_id": cls.ADZUNA_APP_ID,
            "app_key": cls.ADZUNA_APP_KEY,
            "results_per_page": 30,
            "what": keyword,
            "content-type": "application/json"
        }

        response = requests.get(cls.BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        return data.get("results", [])


    # Store Jobs (Overwrite Per Keyword)
    @classmethod
    def overwrite_jobs(cls, keyword: str, jobs: list):

        conn = sqlite3.connect(cls.JOB_DATABASE_NAME)
        cursor = conn.cursor()

        # Remove old jobs only for this keyword
        cursor.execute("DELETE FROM jobs WHERE keyword = ?", (keyword,))

        for job in jobs:
            cursor.execute("""
                INSERT OR IGNORE INTO jobs (
                    keyword,
                    adzuna_job_id,
                    title,
                    company,
                    location,
                    description,
                    salary_min,
                    salary_max,
                    apply_link,
                    fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword,
                job.get("id"),
                job.get("title"),
                job.get("company", {}).get("display_name"),
                job.get("location", {}).get("display_name"),
                job.get("description"),
                job.get("salary_min"),
                job.get("salary_max"),
                job.get("redirect_url"),
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

    # Retrieve Stored Jobs
    @classmethod
    def get_jobs_from_database(cls, keyword: str):

        conn = sqlite3.connect(cls.JOB_DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, company, location, description,
                   salary_min, salary_max, apply_link
            FROM jobs
            WHERE keyword = ?
        """, (keyword,))

        rows = cursor.fetchall()
        conn.close()

        jobs = []

        for row in rows:
            jobs.append({
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "description": row[3],
                "salary_min": row[4],
                "salary_max": row[5],
                "apply_link": row[6]
            })

        return jobs

    # Main Entry Point
    @classmethod
    def fetch_jobs(cls, role_keyword: str):

        # Ensure DB exists
        cls.initialize_database()

        # Simple normalization only
        keyword = role_keyword.strip().lower()

        # Try API
        api_jobs = cls.fetch_jobs_from_api(keyword)

        if api_jobs:
            cls.overwrite_jobs(keyword, api_jobs)

        # Always return stored jobs
        return cls.get_jobs_from_database(keyword)
