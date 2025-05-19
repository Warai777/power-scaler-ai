import json
import os

TRACKER_FILE = "data/series_progress.json"

def _load_tracker():
    if not os.path.exists(TRACKER_FILE):
        return {}
    with open(TRACKER_FILE, "r") as f:
        return json.load(f)

def _save_tracker(data):
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_last_parsed(series_name):
    data = _load_tracker()
    return data.get(series_name, {"last_chapter": 1, "last_episode": 1})

def update_last_parsed(series_name, chapter=None, episode=None):
    data = _load_tracker()
    entry = data.get(series_name, {"last_chapter": 1, "last_episode": 1})
    if chapter is not None:
        entry["last_chapter"] = max(entry.get("last_chapter", 1), chapter)
    if episode is not None:
        entry["last_episode"] = max(entry.get("last_episode", 1), episode)
    data[series_name] = entry
    _save_tracker(data)

def reset_progress(series_name):
    data = _load_tracker()
    if series_name in data:
        del data[series_name]
        _save_tracker(data)

def get_all_series():
    return list(_load_tracker().keys())

def get_all_progress():
    return _load_tracker()
