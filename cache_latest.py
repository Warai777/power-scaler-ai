import json
import os
from datetime import datetime, timedelta

# File where latest chapter/episode cache will be stored
CACHE_FILE = "data/latest_cache.json"

# Cache expiry duration in minutes
CACHE_DURATION_MINUTES = 60  # Adjust as needed

def _load_cache():
    """Load the cached data from disk."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def _save_cache(data):
    """Save cache data to disk."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_cached_latest(series_name, key):
    """
    Get the cached latest value (chapter or episode) for a series.
    Only returns the value if the cache is still valid.
    """
    data = _load_cache()
    series_entry = data.get(series_name, {})
    entry = series_entry.get(key)

    if not entry:
        return None

    timestamp = datetime.fromisoformat(entry["timestamp"])
    if datetime.now() - timestamp > timedelta(minutes=CACHE_DURATION_MINUTES):
        return None  # Expired
    return entry["value"]

def set_cached_latest(series_name, key, value):
    """
    Store the latest chapter/episode value in the cache with a timestamp.
    """
    data = _load_cache()
    if series_name not in data:
        data[series_name] = {}
    data[series_name][key] = {
        "value": value,
        "timestamp": datetime.now().isoformat()
    }
    _save_cache(data)

def get_cache_timestamp(series_name, key):
    """
    Get the timestamp when the latest value for a series was cached.
    """
    data = _load_cache()
    series_entry = data.get(series_name, {})
    entry = series_entry.get(key)
    if entry:
        return entry.get("timestamp")
    return None
