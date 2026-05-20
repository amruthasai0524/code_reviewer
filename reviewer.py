import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def review_code(code_snippet, language):

    prompt = f"""
You are an expert AI code reviewer.

Analyze ONLY the provided code snippet.

Strict Review Rules:
- Do NOT invent issues.
- Do NOT force suggestions unnecessarily.
- Variables like 'i' are acceptable in short loops.
- Only identify REAL syntax or readability issues.
- If code is already good, return empty issue and suggestion lists.

IMPORTANT:
- Do NOT execute code
- Return ONLY valid JSON
- No markdown formatting

Expected JSON format:

{{
  "identified_issues": [],
  "improvement_suggestions": [],
  "code_quality_level": "",
  "review_summary": ""
}}

Programming Language:
{language}

Code Snippet:
{code_snippet}
"""

    try:

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only AI code review assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        result_text = completion.choices[0].message.content

        # Clean markdown formatting
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "")
        result_text = result_text.strip()

        # Parse JSON
        result = json.loads(result_text)

        # Ensure required fields
        result.setdefault("identified_issues", [])
        result.setdefault("improvement_suggestions", [])
        result.setdefault("code_quality_level", "Unknown")
        result.setdefault("review_summary", "No summary available.")

        return result

    except Exception as e:

        return {
            "identified_issues": [
                "Unable to analyze code properly."
            ],
            "improvement_suggestions": [
                "Check API key or model configuration."
            ],
            "code_quality_level": "Unknown",
            "review_summary": str(e)
        }
