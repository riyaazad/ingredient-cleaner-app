import os
from dotenv import load_dotenv

#read our .env file
project_root = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, ".env"))
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You normalize cosmetic ingredient strings.
If uncertain, return null values.
Do NOT merge chemically different ingredients.
Return ONLY valid JSON matching the schema.
"""

#added this in case ai has error, to automatically try again
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
    return response.output_parsed
