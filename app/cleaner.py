import re #pythons regex

ALIASES = {
    "vitamin b-3": "niacinamide",
    "vit b3": "niacinamide",
    "octinoxate": "ethylhexyl methoxycinnamate",
    "aqua": "water",
    "phenoxyehtanol": "phenoxyethanol",
    "niacinimide": "niacinamide",
    "sodum hyaluronate": "sodium hyaluronate",
    "parfum": "fragrance"
    #we can keep adding more/extending this list for common mix ups
}

def map_aliases(text: str) -> str:
    key = text.lower().strip()
    return ALIASES.get(key, text)

DO_NOT_MERGE = [
    ("chloride", "chlorite")
]

def basic_clean(raw: str) -> str:
    #this is to trim whitespace, lowercase, remove white space and clean string
    cleaned = raw.strip().lower()
    cleaned = cleaned.strip('"').strip("'")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def contains_concentration(text: str) -> bool:
    return bool(re.search(r"\d+%", text)) #this is to check if we have a concentration (basically anything with %)

def violates_do_not_merge(text: str) -> bool:
    for a, b in DO_NOT_MERGE:
        if a in text and b in text:
            return True #true, dont merge
    return False
