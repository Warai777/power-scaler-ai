from pymongo import MongoClient
import os

# Load Mongo URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")

# Create secure MongoDB client with timeout + TLS
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tls=True)

# Access your database and collection
db = client["powerscaler"]
characters = db["characters"]

def get_character_profile(name):
    profile = characters.find_one({"name": name.lower()})
    if profile:
        return profile.get("profile", "No profile found.")
    return "Character not found."

def update_character_profile(name, data):
    characters.update_one(
        {"name": name.lower()},
        {"$set": {"profile": data}},
        upsert=True
    )
