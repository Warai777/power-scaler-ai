import os
from kitsunekko_scraper import fetch_kitsunekko_subtitles
from youtube_transcript import fetch_youtube_summary
from gpt_feat_parser import parse_feats_with_gpt

def fetch_subtitle_text(anime_title, episode_number):
    # 1. Try Kitsunekko subtitles
    subtitle_text = fetch_kitsunekko_subtitles(anime_title, episode_number)
    if subtitle_text:
        print("[✓] Found subtitle from Kitsunekko")
        return subtitle_text

    # 2. Fallback to YouTube summaries
    print("[!] Kitsunekko failed, falling back to YouTube summary")
    return fetch_youtube_summary(anime_title, episode_number)


def parse_anime_episode(anime_title, episode_number):
    print(f"[+] Starting anime feat parser for {anime_title} Episode {episode_number}...")
    raw_text = fetch_subtitle_text(anime_title, episode_number)

    if not raw_text:
        return "❌ No subtitles or summaries found for this episode."

    return parse_feats_with_gpt(
        raw_text,
        anime_title,
        episode_number,
        source="Anime (Subs/YouTube)"
    )
