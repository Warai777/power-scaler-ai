import requests

API_URL = "https://api.mangadex.org"

def fetch_mangadex_chapter(series_name, chapter_number):
    try:
        # Step 1: Search manga by title
        search = requests.get(f"{API_URL}/manga", params={"title": series_name, "limit": 1})
        search.raise_for_status()
        manga = search.json()["data"][0]
        manga_id = manga["id"]

        # Step 2: Find the desired chapter
        chap = requests.get(f"{API_URL}/chapter", params={
            "manga": manga_id,
            "chapter": str(chapter_number),
            "translatedLanguage[]": "en",
            "order[chapter]": "asc",
            "limit": 1
        })
        chap.raise_for_status()
        chapters = chap.json()["data"]
        if not chapters:
            print("[MangaDex] Chapter not found.")
            return None

        chapter_id = chapters[0]["id"]

        # Step 3: Get page URLs
        page_data = requests.get(f"{API_URL}/at-home/server/{chapter_id}").json()
        base_url = page_data["baseUrl"]
        page_paths = page_data["chapter"]["data"]
        image_urls = [f"{base_url}/data/{page_data['chapter']['hash']}/{img}" for img in page_paths]

        # Return page links (to be parsed by OCR if needed)
        return "\n".join(image_urls)

    except Exception as e:
        print(f"[MangaDex Error] {e}")
        return None
