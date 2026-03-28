#Task 2.1
import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app
app = FastAPI(title="Campaign Brief Analyzer API")

# Request model
class BriefRequest(BaseModel):
    brief_text: str


@app.post("/analyze-brief")
async def analyze_brief(request: BriefRequest):
    system_prompt = (
        "You are a marketing strategist working at an advertising agency. "
        "Analyze campaign briefs and return structured JSON only."
    )

    user_prompt = f"""
Analyze the campaign brief below and return JSON with exactly these fields:
- audience
- key_messages (array)
- tone
- channels (array)
- risks (array)

Campaign brief:
{request.brief_text}

Return JSON only in this format:
{{
  "audience": "",
  "key_messages": ["", ""],
  "tone": "",
  "channels": ["", ""],
  "risks": ["", ""]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,  # lower temperature for more consistent analysis
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    return json.loads(content)

