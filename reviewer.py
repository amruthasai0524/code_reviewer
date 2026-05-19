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

Strict Review Rules:
- Do NOT invent issues.
- Do NOT force suggestions unnecessarily.
- Simple snippets should not receive unnecessary criticism.
- Variables like 'i', 'j', and 'k' are acceptable in short loops.
- Do NOT suggest adding a main function for small snippets.
- Only identify REAL problems.
- If the code is already good, return empty issue and suggestion lists.

Tasks:
1. Identify real syntax issues
2. Identify real readability issues
3. Suggest meaningful improvements only if genuinely needed
4. Evaluate overall code quality fairly

IMPORTANT:
- Do NOT execute code
- Return ONLY valid JSON
- No markdown formatting
- No explanations outside JSON

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
                    "role": "system",
                    "content": "You are a strict JSON-only code review assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        result_text = completion.choices[0].message.content

        # Remove markdown formatting if present
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "")
        result_text = result_text.strip()

        # Parse JSON response
        result = json.loads(result_text)

        # Ensure required fields exist
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
