import streamlit as st
import json
from reviewer import review_code

# Page configuration
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="💻",
    layout="centered"
)

# App title
st.title("💻 AI Code Review Assistant")
st.markdown("Generative AI powered code reviewer using Groq Llama 3")

# Language selection
language = st.selectbox(
    "Select Programming Language",
    [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "Go",
        "SQL"
    ]
)

# Code input
code_input = st.text_area(
    "Paste Your Code Snippet",
    height=300,
    placeholder="Paste your code here..."
)

# Code preview
if code_input:
    st.subheader("📄 Code Preview")
    st.code(code_input, language=language.lower())

# Review button
if st.button("🚀 Review Code"):

    if code_input.strip() == "":
        st.warning("Please enter a code snippet.")

    else:

        with st.spinner("Analyzing code..."):

            result = review_code(code_input, language)

            st.success("Analysis Completed")

            # -------------------------
            # Identified Issues
            # -------------------------
            st.subheader("📌 Identified Issues")

            issues = result.get("identified_issues", [])

            if not issues:
                st.write("No major issues found.")

            else:

                for issue in issues:

                    if isinstance(issue, dict):

                        description = issue.get("description", "")
                        line_number = issue.get("line_number")

                        if line_number:
                            st.write(f"• Line {line_number}: {description}")
                        else:
                            st.write(f"• {description}")

                    else:
                        st.write(f"• {issue}")

            # -------------------------
            # Improvement Suggestions
            # -------------------------
            st.subheader("✅ Improvement Suggestions")

            suggestions = result.get(
                "improvement_suggestions",
                []
            )

            if not suggestions:
                st.write("No suggestions needed.")

            else:

                for suggestion in suggestions:

                    if isinstance(suggestion, dict):

                        description = suggestion.get(
                            "description",
                            ""
                        )

                        line_number = suggestion.get(
                            "line_number"
                        )

                        if line_number:
                            st.write(
                                f"• Line {line_number}: {description}"
                            )
                        else:
                            st.write(f"• {description}")

                    else:
                        st.write(f"• {suggestion}")

            # -------------------------
            # Code Quality Level
            # -------------------------
            st.subheader("📊 Code Quality Level")

            quality = result.get(
                "code_quality_level",
                "Unknown"
            )

            quality_lower = quality.lower()

            if quality_lower == "high":
                st.success(quality)

            elif quality_lower == "medium":
                st.warning(quality)

            elif quality_lower == "low":
                st.error(quality)

            else:
                st.info(quality)

            # -------------------------
            # Review Summary
            # -------------------------
            st.subheader("📝 Review Summary")

            st.write(
                result.get(
                    "review_summary",
                    "No summary available."
                )
            )

            # -------------------------
            # JSON Output Viewer
            # -------------------------
            st.subheader("📦 JSON Output")

            st.json(result)

            # -------------------------
            # Download Report Button
            # -------------------------
            st.download_button(
                label="⬇ Download Review Report",
                data=json.dumps(result, indent=4),
                file_name="code_review_report.json",
                mime="application/json"
            )