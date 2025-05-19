import json
import os

# File path where series progress will be stored
TRACKER_FILE = "data/series_progress.json"

def _load_tracker():
    """Load the tracker JSON file into memory."""
    if not os.path.exists(TRACKER_FILE):
        return {}
    with open(TRACKER_FILE, "r") as f:
        return json.load(f)

def _save_tracker(data):
    """Save the in-memory tracker data to file."""
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_last_parsed(series_name):
    """
    Get the last parsed chapter and episode for a given series.

    Returns:
        dict: { "last_chapter": int, "last_episode": int }
    """
    data = _load_tracker()
    return data.get(series_name, {"last_chapter": 1, "last_episode": 1})

def update_last_parsed(series_name, chapter=None, episode=None):
    """
    Update the last parsed chapter/episode for a given series.

    Args:
        series_name (str): Name of the series
        chapter (int): Newest chapter parsed
        episode (int): Newest episode parsed
    """
    data = _load_tracker()
    entry = data.get(series_name, {"last_chapter": 1, "last_episode": 1})

    if chapter is not None:
        entry["last_chapter"] = max(entry.get("last_chapter", 1), chapter)
    if episode is not None:
        entry["last_episode"] = max(entry.get("last_episode", 1), episode)

    data[series_name] = entry
    _save_tracker(data)
