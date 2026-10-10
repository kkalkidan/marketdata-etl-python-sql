import os
from pathlib import Path
from dotenv import load_dotenv 

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def get_value(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is not set")
    return value