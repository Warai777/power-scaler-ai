import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
MAP_FILE = "data/name_map.json"

def _load_map():
    if not os.path.exists(MAP_FILE):
        return {}
    with open(MAP_FILE, "r") as f:
        return json.load(f)

def _save_map(data):
    os.makedirs(os.path.dirname(MAP_FILE), exist_ok=True)
    with open(MAP_FILE, "w") as f:
        json.dump(data, f, indent=4)

def resolve_character_name(nickname):
    """
    Resolves a character nickname to their series name.
    1. Check name_map.json first
    2. If missing, ask GPT and save to cache
    """
    key = nickname.strip().lower()
    mapping = _load_map()

    if key in mapping:
        return mapping[key]

    # Ask GPT if not found
    try:
        prompt = f"What anime, manga, game, or series is the character '{nickname}' from? Reply only with the series title."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You're a database assistant. Only respond with the name of the series the character is from. No explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=20
        )

        series = response.choices[0].message.content.strip().title()
        mapping[key] = series
        _save_map(mapping)
        return series
    except Exception as e:
        print(f"[Name Resolver Error] {e}")
        return nickname.title()
