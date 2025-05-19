import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
import re

BASE_URL = "https://kitsunekko.net"
SUB_DIR = "https://kitsunekko.net/dirlist.php?dir=subtitles%2Fenglish%2F"


def fetch_kitsunekko_subtitles(anime_title, episode_number):
    try:
        print(f"[Kitsunekko] Searching for subtitles for: {anime_title} ep{episode_number}")
        page = requests.get(SUB_DIR)
        soup = BeautifulSoup(page.text, "html.parser")

        # Find matching directory (e.g., Naruto, Bleach)
        links = soup.find_all("a")
        dir_link = None
        for link in links:
            name = link.get_text().strip().lower()
            if anime_title.lower() in name:
                dir_link = BASE_URL + link.get("href")
                break

        if not dir_link:
            print("[Kitsunekko] Series folder not found.")
            return None

        # Now open that folder and find a subtitle zip
        sub_page = requests.get(dir_link)
        sub_soup = BeautifulSoup(sub_page.text, "html.parser")
        sub_links = sub_soup.find_all("a")
        zip_link = None
        for link in sub_links:
            fname = link.get_text().lower()
            if ("ep" in fname or "episode" in fname) and fname.endswith(".zip") and str(episode_number) in fname:
                zip_link = BASE_URL + link.get("href")
                break

        if not zip_link:
            print("[Kitsunekko] Subtitle zip not found.")
            return None

        # Download zip file
        zip_data = requests.get(zip_link).content
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            for file in zip_file.namelist():
                if file.endswith(".srt") or file.endswith(".ass"):
                    with zip_file.open(file) as sub_file:
                        raw = sub_file.read().decode(errors='ignore')
                        return clean_subtitle_text(raw)

        print("[Kitsunekko] No subtitle file found in zip.")
        return None

    except Exception as e:
        print(f"[Kitsunekko Error] {e}")
        return None


def clean_subtitle_text(sub_raw):
    # Remove timestamps, tags, numbering
    cleaned = re.sub(r"\d+\n", "", sub_raw)  # Numbering
    cleaned = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> .*", "", cleaned)  # Timestamps
    cleaned = re.sub(r"<[^>]+>", "", cleaned)  # Tags
    cleaned = re.sub(r"{\\.*?}", "", cleaned)  # ASS format tags
    cleaned = re.sub(r"\n\n+", "\n", cleaned)  # Collapse multiple newlines
    return cleaned.strip()
