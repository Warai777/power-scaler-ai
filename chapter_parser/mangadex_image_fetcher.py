import os
import requests

MANGADEX_API = "https://api.mangadex.org"

def get_chapter_id(series_name, chapter_number):
    query = {
        "title": series_name,
        "limit": 1
    }
    res = requests.get(f"{MANGADEX_API}/manga", params=query)
    data = res.json()

    if not data["data"]:
        print(f"[MangaDex] ❌ Series not found: {series_name}")
        return None

    manga_id = data["data"][0]["id"]

    chapter_query = {
        "manga": manga_id,
        "chapter": str(chapter_number),
        "translatedLanguage[]": ["en"],
        "limit": 1,
        "order[chapter]": "asc"
    }

    ch_res = requests.get(f"{MANGADEX_API}/chapter", params=chapter_query)
    ch_data = ch_res.json()

    if not ch_data["data"]:
        print(f"[MangaDex] ❌ Chapter {chapter_number} not found.")
        return None

    return ch_data["data"][0]["id"]


def download_mangadex_images(series_name, chapter_number, output_base="ocr/mangadex"):
    chapter_id = get_chapter_id(series_name, chapter_number)
    if not chapter_id:
        return None

    # Get server URL + image paths
    server_info = requests.get(f"{MANGADEX_API}/at-home/server/{chapter_id}").json()
    base_url = server_info["baseUrl"]

    chapter_info = requests.get(f"{MANGADEX_API}/chapter/{chapter_id}").json()
    hash_val = chapter_info["data"]["attributes"]["hash"]
    page_list = chapter_info["data"]["attributes"]["data"]

    folder = f"{output_base}/{series_name.lower().replace(' ', '_')}/chapter_{chapter_number}"
    os.makedirs(folder, exist_ok=True)

    # Skip if already downloaded
    if len(os.listdir(folder)) >= len(page_list):
        print(f"[🔁] Already downloaded → {folder}")
        return folder

    # Download all images
    for i, filename in enumerate(page_list):
        url = f"{base_url}/data/{hash_val}/{filename}"
        save_path = os.path.join(folder, f"{i+1:03}.jpg")

        r = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(r.content)

        print(f"[📥] Page {i+1} saved")

    return folder
