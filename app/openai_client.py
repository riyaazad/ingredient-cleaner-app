import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# read our .env file
project_root = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You normalize cosmetic ingredient strings.

Rules:
- If uncertain, return null values.
- Do NOT merge chemically different ingredients.
- Avoid guessing.
- Return ONLY valid JSON matching this schema:

{
  "normalized_inci": string | null,
  "normalized_common": string | null,
  "category": "ingredient" | "fragrance" | "colorant" | "marketing_term" | "unknown",
  "confidence": number,
  "flags": string[],
  "explanation": string
}
"""

# added this in case AI has error, to automatically try again
@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def call_openai(raw: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0.1,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw}
        ]
    )

    try:
        text_output = response.output[0].content[0].text
    except (AttributeError, IndexError):
        return {}

    text_output = text_output.strip().strip("```json").strip("```").strip()

    try:
        parsed = json.loads(text_output)
    except json.JSONDecodeError:
        return {}

    return {
        "normalized_inci": parsed.get("normalized_inci"),
        "normalized_common": parsed.get("normalized_common"),
        "category": parsed.get("category", "unknown"),
        "confidence": parsed.get("confidence", 0.0),
        "flags": parsed.get("flags", []),
        "explanation": parsed.get("explanation", "")
    }
