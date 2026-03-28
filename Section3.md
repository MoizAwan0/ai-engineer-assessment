Q1 — Retry function (Anthropic API)

Code

import time

import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

def call_api_with_retry(prompt):

    for attempt in range(3):
        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        except Exception as e:
            print("Error:", e)
            break

    return "Failed after retries"

Explanation

I implemented a retry mechanism that attempts the API call up to three times if a rate limit error occurs. I used exponential backoff so each retry waits longer than the previous one. This helps avoid repeated failures and makes the function more stable in real-world usage.

Q2 — Debug LangChain RAG pipeline

Answer

If a LangChain RAG pipeline is not working correctly, I would check these common issues:

The embedding model used for indexing and querying is different, which leads to poor or incorrect retrieval.
The retriever is not returning any documents due to incorrect configuration or indexing issues.
The chain is not passing retrieved documents into the final prompt, so the model answers without context.
Source documents are not returned because return_source_documents=True is missing.

Explanation

The most important part of RAG is making sure retrieval actually works. If documents are not retrieved properly or not passed to the model, the system behaves like a normal LLM instead of a grounded system.

Q3 — System prompt (brand tone enforcer)

Prompt
You are a brand tone enforcer for an advertising agency.

Your task is to rewrite marketing copy so it strictly follows the brand guidelines:

Tone rules:
- Premium and confident
- Clear and professional
- No slang or casual language
- Persuasive but not exaggerated

Instructions:
- Rewrite the input text to match the tone
- Keep the original meaning
- Improve clarity and flow
- Do not add unnecessary information

Return only the rewritten text.

Explanation

I designed this prompt to behave like an editor rather than a creative writer. The goal is consistency, not creativity. The instructions ensure the meaning stays the same while improving tone and clarity.

Q4 — Brand safety evaluation

Answer

Image 1 — Score: 9/10

The image appears safe for advertising use. There is no visible harmful content such as violence or inappropriate material. It is suitable for most campaigns.

Image 2 — Score: 5/10

This image has some risk due to suggestive elements. It may not be suitable for all brands or platforms and would require review before use.

Image 3 — Score: 2/10

This image is not brand safe. It includes content that could damage brand reputation, such as violence or offensive themes. It should not be used in advertising.

Explanation

Brand safety is based on whether the image could create legal, ethical, or reputational risk. I considered factors like violence, nudity, and appropriateness for a general audience.

Q5 — System architecture (Ad personalization engine)

Answer

User

  ↓

Website / App Tracking (events, clicks, behavior)

  ↓

Data Pipeline (streaming / batch processing)

  ↓

User Profile Store / Feature Store

  ↓

AI Personalization Engine
  ├─ Rules (campaign targeting)
  ├─ ML / LLM ranking model
  └─ Business constraints

  ↓

Ad Decision API

  ↓

Ad Server / Frontend

  ↓

Performance Tracking & Feedback Loop

Explanation

The system collects user behavior data, builds a profile, and uses AI to decide which ad to show. The feedback loop is important because it allows the system to improve over time based on performance data.