import os
import requests
from PIL import Image
from io import BytesIO

API_URL = "https://api.mangadex.org"

def clean_name(name):
    return name.lower().replace(" ", "-").replace(".", "").replace(":", "")

def download_mangadex_images(series_name, chapter_number):
    try:
        safe_name = clean_name(series_name)
        target_folder = f"ocr/mangadex/{safe_name}/chapter_{chapter_number}"
        os.makedirs(target_folder, exist_ok=True)

        # Skip download if already exists
        if os.listdir(target_folder):
            print(f"[🔁] Skipping download: Already exists → {target_folder}")
            return [os.path.join(target_folder, f) for f in sorted(os.listdir(target_folder))]

        # Step 1: Search manga
        res = requests.get(f"{API_URL}/manga", params={"title": series_name, "limit": 1})
        res.raise_for_status()
        manga_id = res.json()["data"][0]["id"]

        # Step 2: Find chapter
        res = requests.get(f"{API_URL}/chapter", params={
            "manga": manga_id,
            "chapter": str(chapter_number),
            "translatedLanguage[]": "en",
            "limit": 1
        })
        res.raise_for_status()
        chapters = res.json()["data"]
        if not chapters:
            print(f"[❌] Chapter {chapter_number} not found on MangaDex")
            return None

        chapter_id = chapters[0]["id"]

        # Step 3: Get image data
        res = requests.get(f"{API_URL}/at-home/server/{chapter_id}")
        res.raise_for_status()
        data = res.json()
        base_url = data["baseUrl"]
        hash_val = data["chapter"]["hash"]
        images = data["chapter"]["data"]

        # Step 4: Download images
        saved_files = []
        for idx, file_name in enumerate(images):
            img_url = f"{base_url}/data/{hash_val}/{file_name}"
            img_res = requests.get(img_url)
            img_res.raise_for_status()

            image = Image.open(BytesIO(img_res.content)).convert("RGB")
            save_path = os.path.join(target_folder, f"{idx + 1:03d}.jpg")
            image.save(save_path)
            saved_files.append(save_path)

        print(f"[✅] Downloaded {len(saved_files)} pages to {target_folder}")
        return saved_files

    except Exception as e:
        print(f"[❌] MangaDex Download Error: {e}")
        return None
