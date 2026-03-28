#Task 1.1
import json
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_copy(brief: str) -> dict:
    """
    Generates 3 variations of advertising copy using OpenAI API.
    Includes retry logic and strict JSON output handling.
    """

    system_prompt = (
        "You are a professional advertising copywriter. "
        "Generate high-quality, persuasive ad copy. "
        "Follow the JSON format strictly and do not include extra text."
    )

    user_prompt = f"""
Generate 3 variations of ad copy for this product:

{brief}

Each variation must include:
- headline
- tagline
- body
- cta

Return JSON EXACTLY in this format:

{{
  "variation_1": {{
    "headline": "",
    "tagline": "",
    "body": "",
    "cta": ""
  }},
  "variation_2": {{
    "headline": "",
    "tagline": "",
    "body": "",
    "cta": ""
  }},
  "variation_3": {{
    "headline": "",
    "tagline": "",
    "body": "",
    "cta": ""
  }}
}}
"""

    # Retry logic with exponential backoff
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,  # Higher for creative ad copy
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                print(f"Retrying in {wait_time} seconds...\n")
                time.sleep(wait_time)
            else:
                return {"error": "Failed after retries"}


if __name__ == "__main__":
    brief = "New luxury perfume for men, brand name: Noir, target: 30-45 year old professionals"

    result = generate_copy(brief)

    print("\nGenerated Ad Copy:\n")
    print(json.dumps(result, indent=2))

    # Save output to file (IMPORTANT for submission)
    with open("sample_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\nSaved output to sample_output.json")