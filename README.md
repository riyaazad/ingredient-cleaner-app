#Ingredient Cleaner App

This project implements a small HTTP API that normalizes messy cosmetic ingredient strings into structured, deterministic JSON objects.

##How to Run Locally:
- Create a virtual environment and activate it:
- python3 -m venv venv
- source venv/bin/activate

##Install dependencies:
- pip install -r requirements.txt

##Find the .env file in the project root and put your own key:
- OPENAI_API_KEY=your_openai_api_key_here

##Start the server:
- uvicorn app.main:app --reload

The API will be available at:
- http://127.0.0.1:8000


Endpoint: POST /v1/ingredient/normalize

Request Body
{
  "raw": "Niacinimide"
}

Response Body (strict shape)
{
  "raw": "Niacinimide",
  "normalized_inci": "Niacinamide",
  "normalized_common": "Vitamin B3",
  "category": "ingredient",
  "confidence": 0.95,
  "flags": ["typo_suspected"],
  "explanation": "Detected as a spelling error and normalized to the INCI name Niacinamide."
}

##cURL Example:

curl -X POST \
  http://127.0.0.1:8000/v1/ingredient/normalize \
  -H "Content-Type: application/json" \
  -d '{"raw": "Niacinimide"}'

##Design:
- No guessing when uncertain
- Strict JSON validation
- System Prompt:
You normalize cosmetic ingredient strings.
- If uncertain, return null values.
- Do NOT merge chemically different ingredients, even if names are similar.
- Avoid guessing; prefer null over hallucination.
- Return ONLY valid JSON matching the provided schema.

##Output Schema:

raw: original input string
normalized_inci: best-guess INCI name or null
normalized_common: common name or null
category: one of
"ingredient" | "fragrance" | "colorant" | "marketing_term" | "unknown"
confidence: numeric value between 0 and 1
flags: list of strings (e.g. "typo_suspected", "ambiguous", "contains_concentration")
explanation: 1–3 short sentences for internal debugging

The model output is validated against this schema before returning a response.

##Failure modes:
- OpenAI API quota exceeded → request fails with an error
- Rare INCI variants not represented in prompt examples may reduce confidence

##AI Usage Disclosure:
Tools Used: ChatGPT

Prompt v1: Clean up cosmetic ingredient strings. Return a structured JSON object with the INCI name if confident. Otherwise, set fields to null.

Prompt v2: Normalize ingredient strings from messy input (typos, variants, marketing terms). Ensure the output matches the strict JSON schema. Set confidence to 0 if unsure and include explanatory flags.

Change Log:
v1: Basic JSON returned, but sometimes text was not parseable
v2: Model occasionally returned inconsistent confidence scores so I added retry logic

- Also used chatgpt to help with API set up
