#Task 2.2

import os
import json
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_mime_type(file_ext: str) -> str:
    file_ext = file_ext.lower()
    if file_ext == ".png":
        return "image/png"
    if file_ext == ".webp":
        return "image/webp"
    return "image/jpeg"


def analyze_image(image_path: str) -> dict:
    file_name = os.path.basename(image_path)
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext not in SUPPORTED_EXTENSIONS:
        return {
            "filename": file_name,
            "error": f"Unsupported format: {file_ext}"
        }

    base64_image = encode_image(image_path)
    mime_type = get_mime_type(file_ext)

    system_prompt = (
        "You are an advertising image analysis assistant. "
        "Analyze marketing images and return only valid JSON."
    )

    user_prompt = f"""
Analyze this advertising image and return JSON with exactly these fields:
- filename
- alt_text
- tags (array)
- brand_safety_score (integer from 1 to 10)
- use_cases (array)

Instructions:
- alt_text should be short, clear, and descriptive
- tags should describe objects, mood, style, and setting
- brand_safety_score should reflect commercial safety for advertising use
- use_cases should suggest realistic advertising campaign applications

Return JSON exactly in this format:
{{
  "filename": "{file_name}",
  "alt_text": "",
  "tags": ["", ""],
  "brand_safety_score": 0,
  "use_cases": ["", ""]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


def process_folder(folder_path: str, output_file: str = "tags_output.json") -> None:
    results = []

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)

        if not os.path.isfile(image_path):
            continue

        try:
            result = analyze_image(image_path)
            results.append(result)
            print(f"Processed: {file_name}")
        except Exception as e:
            results.append({
                "filename": file_name,
                "error": str(e)
            })
            print(f"Failed: {file_name} -> {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. Results saved to {output_file}")


if __name__ == "__main__":
    process_folder("test_images")