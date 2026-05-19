import os
import json
from dotenv import load_dotenv
from groq import Groq

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

Review Guidelines:
- Do NOT invent issues.
- Do NOT force suggestions unnecessarily.
- Small code snippets do NOT require a main function.
- Simple loop variables like 'i' are acceptable in short loops.
- Only report genuine syntax, readability, or quality issues.

Tasks:
1. Identify real syntax issues
2. Identify real readability problems
3. Suggest practical improvements only if necessary
4. Evaluate overall code quality fairly

IMPORTANT:
- Do NOT execute code
- Return ONLY valid JSON
- No markdown formatting

Expected JSON format:

{{
  "identified_issues": [],
  "improvement_suggestions": [],
  "code_quality_level": "High/Medium/Low",
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
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        result_text = completion.choices[0].message.content

        # Remove markdown formatting if present
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "")
        result_text = result_text.strip()

        # Parse JSON response
        result = json.loads(result_text)

        # Ensure required keys exist
        result.setdefault("identified_issues", [])
        result.setdefault("improvement_suggestions", [])
        result.setdefault("code_quality_level", "Unknown")
        result.setdefault("review_summary", "No summary provided.")

        return result

    except Exception as e:

        return {
            "identified_issues": [
                "Unable to analyze code properly."
            ],
            "improvement_suggestions": [
                "Check API key, internet connection, or model configuration."
            ],
            "code_quality_level": "Unknown",
            "review_summary": str(e)
        }