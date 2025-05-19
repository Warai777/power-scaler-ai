import requests
import re

def get_latest_chapter(series_name):
    """
    Gets the latest English chapter of a manga using:
    1. MangaDex API
    2. Viz.com scraping (fallback)
    """
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
                return int(float(latest))
    except Exception as e:
        print(f"[MangaDex] Failed for {series_name}: {e}")

    try:
        slug = series_name.lower().replace(" ", "-")
        viz_url = f"https://www.viz.com/shonenjump/chapters/{slug}"
        html = requests.get(viz_url, timeout=5).text
        chapters = re.findall(r'Chapter\\s(\\d+)', html)
        chapter_numbers = [int(c) for c in chapters if c.isdigit()]
        return max(chapter_numbers) if chapter_numbers else 100
    except Exception as e:
        print(f"[Viz] Failed for {series_name}: {e}")

    return 100


def get_latest_episode(series_name):
    """
    Gets the latest number of anime episodes using:
    1. AniList GraphQL API
    2. Kitsunekko subtitle count (fallback)
    """
    # Try AniList
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
            return episodes
    except Exception as e:
        print(f"[AniList] Failed for {series_name}: {e}")

    # Fallback: Kitsunekko subtitle listing
    try:
        kitsu_slug = series_name.title().replace(" ", "%20")
        kitsu_url = f"https://kitsunekko.net/dirlist.php?dir=subtitles/English/{kitsu_slug}/"
        html = requests.get(kitsu_url, timeout=5).text
        matches = re.findall(r'href=".*?\.(ass|srt)"', html, flags=re.IGNORECASE)
        return len(matches) if matches else 100
    except Exception as e:
        print(f"[Kitsunekko] Failed for {series_name}: {e}")

    return 100
