import requests
import re

def get_latest_chapter(series_name):
    """
    Gets the latest English chapter number of a manga using:
    1. MangaDex API (primary)
    2. Viz.com scraping (fallback)
    """

    # 1. Try MangaDex API
    try:
        search_res = requests.get(
            "https://api.mangadex.org/manga",
            params={"title": series_name}
        ).json()

        if "data" in search_res and len(search_res["data"]) > 0:
            manga_id = search_res["data"][0]["id"]

            chapter_res = requests.get(
                "https://api.mangadex.org/chapter",
                params={
                    "manga": manga_id,
                    "translatedLanguage[]": "en",
                    "order[chapter]": "desc",
                    "limit": 1
                }
            ).json()

            latest = chapter_res["data"][0]["attributes"]["chapter"]
            if latest and latest.replace(".", "").isdigit():
                return int(float(latest))
    except Exception as e:
        print(f"[MangaDex] Failed for {series_name}: {e}")

    # 2. Fallback: Viz.com scraping
    try:
        slug = series_name.lower().replace(" ", "-")
        viz_url = f"https://www.viz.com/shonenjump/chapters/{slug}"
        html = requests.get(viz_url, timeout=5).text

        chapters = re.findall(r'Chapter\\s(\\d+)', html)
        chapter_numbers = [int(c) for c in chapters if c.isdigit()]
        return max(chapter_numbers) if chapter_numbers else 100
    except Exception as e:
        print(f"[Viz] Failed for {series_name}: {e}")

    return 100  # fallback default


def get_latest_episode(series_name):
    """
    Placeholder for real episode detection.
    Replace with AniList or Kitsunekko scraping if needed.
    """
    MOCK_LATEST = {
        "One Piece": 1102,
        "Bleach": 366,
        "Naruto": 500,
        "Jujutsu Kaisen": 47,
        "My Hero Academia": 150
    }
    return MOCK_LATEST.get(series_name, 100)
