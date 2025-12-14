from pydantic import BaseModel
from typing import List, Optional

class IngredientRequest(BaseModel):
    raw: str #the raw/messy ingredient string input

class IngredientResponse(BaseModel):
    raw: str #original input
    normalized_inci: Optional[str] #standardized INCI name (or null)
    normalized_common: Optional[str] #common name (or null)
    category: str #ingredient, frag, color, term, unknown
    confidence: float
    flags: List[str] #typo, not_inci
    explanation: str #readable human explanation, 1-3 sentence
