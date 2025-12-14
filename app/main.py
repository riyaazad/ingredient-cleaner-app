from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.models import IngredientRequest, IngredientResponse
from app.cleaner import basic_clean, map_aliases, contains_concentration, violates_do_not_merge
from app.openai_client import call_openai

app = FastAPI(title="Ingredient Cleaner API")

#i think can take this out but lets leave here incase to see when testing locally, but mostly for frontend from what ive seen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/v1/ingredient/normalize", response_model=IngredientResponse)
async def normalize_ingredient(request: IngredientRequest):
    try:
        #1. first, we clean the input
        cleaned = basic_clean(request.raw)
        #2. map any of our known aliases
        cleaned = map_aliases(cleaned)
        #3. flag any potential issues
        flags = []
        if contains_concentration(request.raw):
            flags.append("contains_concentration")
        if violates_do_not_merge(request.raw):
            flags.append("not_inci")

        #4. now we call openAI for normalization -> sends cleaned ingredient to ai through 
        ai_result = call_openai(cleaned)

        #finally combine all
        response_data = {
            "raw": request.raw,
            "normalized_inci": ai_result.get("normalized_inci"),
            "normalized_common": ai_result.get("normalized_common"),
            "category": ai_result.get("category", "unknown"),
            "confidence": ai_result.get("confidence", 0.0),
            "flags": flags + ai_result.get("flags", []),
            "explanation": ai_result.get("explanation", "")
        }

        return response_data

#error handling
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) #if input doesnt match ingredient request
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #any other error
