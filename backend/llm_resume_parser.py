import requests
import json
import os
from dotenv import load_dotenv

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

PRIMARY_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
SECONDARY_MODEL = "meta-llama/llama-3.2-3b-instruct:free"
TERTIARY_MODEL = "liquid/lfm-2.5-1.2b-instruct:free"


class LLMResumeParser:

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set.")

        self.url = ENDPOINT
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        self.system_prompt = """
You are a resume parsing assistant.

The user will provide normalized resume text.
Extract structured information and return ONLY valid JSON.

Output format EXACTLY:

{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "experience": [
    {
      "role": "",
      "company": "",
      "start_date": "",
      "end_date": ""
    }
  ],
  "job_search_keywords": []
}

job_search_keywords generation logic:

1. Extract job titles directly from professional experience.
2. If no professional experience exists, infer realistic entry-level job titles 
   from projects and multiple supporting technical skills.

Strict Constraints:
- Include ONLY job titles.
- Do NOT include industries.
- Do NOT include domains.
- Do NOT include skills.
- Do NOT include tools.
- Do NOT include soft skills.
- Do NOT include broad concepts.
- Do NOT invent unsupported roles.
- Do NOT fabricate seniority.
- If multiple roles are variations of the same base role,
  return only the canonical base role.
- Remove duplicates.
- Maximum 3 roles.
- Remove company branding from job titles.
- If a role includes an employer name,
  return the generalized role only.

Return ONLY valid JSON.
No explanations.
No markdown.
"""

    def _extract_json(self, content: str):
        if not content:
            return None

        content = content.strip()

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            return None

        try:
            return json.loads(content[start:end + 1])
        except json.JSONDecodeError:
            return None

    def _call_model(self, model_name: str, normalized_text: str):
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": normalized_text}
            ],
            "temperature": 0.0
        }

        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        try:
            data = response.json()

            if "choices" not in data or not data["choices"]:
                return None

            content = data["choices"][0]["message"].get("content", "")
            parsed = self._extract_json(content)

            return parsed

        except Exception:
            return None

    def parse_resume(self, normalized_text: str) -> dict:
        """
        Attempts models sequentially with proper fallback.
        Returns immediately on first success.
        """

        # Try Primary Model
        result = self._call_model(PRIMARY_MODEL, normalized_text)
        if result:
            result["model_used"] = PRIMARY_MODEL
            return result

        # Try Secondary Model
        result = self._call_model(SECONDARY_MODEL, normalized_text)
        if result:
            result["model_used"] = SECONDARY_MODEL
            return result

        # Try Tertiary Model
        result = self._call_model(TERTIARY_MODEL, normalized_text)
        if result:
            result["model_used"] = TERTIARY_MODEL
            return result

        # If all models fail
        return {
            "error": "All models failed.",
            "model_used": None
        }
