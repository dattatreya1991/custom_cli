import json
import os
from functools import lru_cache

MODELS_FILE = os.path.join(os.path.dirname(__file__), "models.json")

@lru_cache(maxsize=1)
def load_models():
   """
   Load model registry from models.json and return
   a list of tuples: [(id, description), …]
   """
   try:
       with open(MODELS_FILE, encoding="utf-8") as fp:
           data = json.load(fp)
       return [(m["id"], m["description"]) for m in data]
   except FileNotFoundError:
       raise RuntimeError(f"Model registry file not found: {MODELS_FILE}")
   except (json.JSONDecodeError, KeyError) as e:
       raise RuntimeError(f"Malformed model registry: {e}")

# Convenience alias for the old name
AVAILABLE_MODELS = load_models()
