import os
from dotenv import load_dotenv

load_dotenv()  # uses project root by default
print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
