import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def fetch_reddit_summary(series_name, chapter_number):
    try:
        query = f"{series_name} chapter {chapter_number} discussion site:reddit.com"
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.find_all("a"):
            href = a.get("href")
            if href and "/url?q=https://www.reddit.com/r/" in href:
                reddit_url = href.split("/url?q=")[1].split("&")[0]
                post_resp = requests.get(reddit_url, headers=headers)
                post_soup = BeautifulSoup(post_resp.text, "html.parser")
                content = post_soup.find("div", {"data-test-id": "post-content"})
                if content:
                    return content.get_text(separator="\n").strip()

        print("[Reddit] No valid thread found.")
        return None

    except Exception as e:
        print(f"[Reddit Error] {e}")
        return None
