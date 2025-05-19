import requests
import re
from cache_latest import get_cached_latest, set_cached_latest  # ✅ NEW

def get_latest_chapter(series_name):
    """
    Gets the latest chapter using:
    1. Cache (if valid)
    2. MangaDex API
    3. Viz.com fallback
    """
    cached = get_cached_latest(series_name, "chapter")
    if cached:
        return cached

    # 1. MangaDex API
    try:
        search_res = requests.get(
            "https://api.mangadex.org/manga",
            params={"title": series_name}
        ).json()

        if "data" in search_res and search_res["data"]:
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
                final = int(float(latest))
                set_cached_latest(series_name, "chapter", final)
                return final
    except Exception as e:
        print(f"[MangaDex] Failed for {series_name}: {e}")

    # 2. Viz fallback
    try:
        slug = series_name.lower().replace(" ", "-")
        viz_url = f"https://www.viz.com/shonenjump/chapters/{slug}"
        html = requests.get(viz_url, timeout=5).text
        chapters = re.findall(r'Chapter\s(\d+)', html)
        chapter_numbers = [int(c) for c in chapters if c.isdigit()]
        if chapter_numbers:
            final = max(chapter_numbers)
            set_cached_latest(series_name, "chapter", final)
            return final
    except Exception as e:
        print(f"[Viz] Failed for {series_name}: {e}")

    return 100


def get_latest_episode(series_name):
    """
    Gets the latest anime episode using:
    1. Cache (if valid)
    2. AniList GraphQL API
    3. Kitsunekko fallback
    """
    cached = get_cached_latest(series_name, "episode")
    if cached:
        return cached

    # 1. AniList API
    try:
        query = '''
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            episodes
          }
        }
        '''
        variables = {"search": series_name}
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        episodes = result["data"]["Media"]["episodes"]
        if episodes and isinstance(episodes, int):
            set_cached_latest(series_name, "episode", episodes)
            return episodes
    except Exception as e:
        print(f"[AniList] Failed for {series_name}: {e}")

    # 2. Kitsunekko fallback
    try:
        kitsu_slug = series_name.title().replace(" ", "%20")
        kitsu_url = f"https://kitsunekko.net/dirlist.php?dir=subtitles/English/{kitsu_slug}/"
        html = requests.get(kitsu_url, timeout=5).text
        matches = re.findall(r'href=".*?\.(ass|srt)"', html, flags=re.IGNORECASE)
        if matches:
            final = len(matches)
            set_cached_latest(series_name, "episode", final)
            return final
    except Exception as e:
        print(f"[Kitsunekko] Failed for {series_name}: {e}")

    return 100
