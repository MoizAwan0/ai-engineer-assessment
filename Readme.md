# AI Engineer Assessment — Submission

## Overview

This project contains my solutions for the AI Engineer assessment. The goal was to design and build practical AI tools that could be used in an advertising agency environment.

The tasks cover LLM integration, prompt engineering, API development, image analysis, and retrieval-based systems.

---

## Technologies Used

- Python
- FastAPI
- OpenAI API
- LangChain
- FAISS
- python-dotenv

---

## Task 1.1 — AI Copywriting API

I built a Python script that generates advertising copy using an LLM API.

- Input: Product brief
- Output: 3 variations (headline, tagline, body, CTA)
- Uses structured JSON output
- Includes retry logic
- Temperature set to 0.8 for controlled creativity

Run:


python copy_generator.py

## Task 1.2 — Prompt Engineering

I improved three weak prompts by adding:

- Role assignment
- Target audience
- Tone and constraints
- Structured output

This resulted in more practical and usable outputs.

## Task 2.1 — Campaign Brief Analyzer API

A FastAPI endpoint that analyzes a campaign brief and returns structured insights.

Endpoint:
POST /analyze-brief

### Input:

{
  "brief_text": "..."
}

### Output:

- audience
- key_messages
- tone
- channels
- risks

### Run:

uvicorn main:app --reload

## Task 2.2 — Image Auto-Tagging System

I built a script that processes a folder of images in batch and generates:

- alt text
- tags
- brand safety score
- use cases

The script encodes images in base64 and sends them to a vision-capable LLM.

### Note:
The test images referenced in the task were not included in the provided materials. The system is ready to run once images are added to the test_images folder.

## Task 2.3 — RAG Chatbot

I implemented a simple RAG system using LangChain and FAISS.

- Loads documents
- Splits into chunks
- Retrieves relevant content
- Returns answer + source + quote
- Includes refusal logic for out-of-scope queries

Note:
The additional documents referenced in the task were not included. The system is ready once files are added to the docs folder.

## Section 3 — Practical Tasks

Includes:

- Retry logic implementation
- RAG debugging explanation
- Brand tone enforcement prompt
- Image safety evaluation
- System architecture design
### Setup Instructions
pip install -r requirements.txt

Add your API key in .env:

OPENAI_API_KEY=your_api_key_here
## Author
### Abdul Moiz