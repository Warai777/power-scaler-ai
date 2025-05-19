import json
import os

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def _get_cache_path(key):
    return os.path.join(CACHE_DIR, f"{key.replace(' ', '_').lower()}.json")

def load_cache(key):
    path = _get_cache_path(key)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("result")
    return None

def save_cache(key, result):
    path = _get_cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"result": result}, f, ensure_ascii=False, indent=2)
