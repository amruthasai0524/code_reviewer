# AI Code Review Assistant using Generative AI

A lightweight AI-powered code review system that analyzes code snippets and returns structured feedback.

## Features

- Syntax issue detection
- Readability analysis
- Improvement suggestions
- Code quality evaluation
- Structured JSON response
- Multi-language support

## Tech Stack

- Python
- Streamlit
- Gemini API
- Prompt Engineering

## Installation

pip install -r requirements.txt

## Run Project

streamlit run app.py

## Output Schema

{
  "identified_issues": [],
  "improvement_suggestions": [],
  "code_quality_level": "",
  "review_summary": ""
}