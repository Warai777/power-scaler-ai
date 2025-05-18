from db import characters

def get_character_profile(name):
    profile = characters.find_one({"name": name.lower()})
    if profile:
        return profile.get("stats", "No stats available.")
    return "Character not found."

def update_character_profile(name, stats):
    characters.update_one(
        {"name": name.lower()},
        {"$set": {"stats": stats}},
        upsert=True
    )
