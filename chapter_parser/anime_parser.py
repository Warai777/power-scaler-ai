import requests
import re
import os
from gpt_feat_parser import parse_feats_with_gpt

# Simulated subtitle fetcher (Kitsunekko or OpenSubtitles would be implemented here)
def fetch_subtitle_text(anime_title, episode_number):
    # Simulated stub (replace with actual .srt file parser if hosting subtitles)
    try:
        # For now, fallback to YouTube summaries (e.g., "Bleach episode 58 summary")
        from youtube_transcript import fetch_youtube_summary
        return fetch_youtube_summary(anime_title, episode_number)
    except Exception as e:
        print(f"[AnimeParser Error] {e}")
        return None


def parse_anime_episode(anime_title, episode_number):
    print(f"[+] Starting anime feat parser for {anime_title} Episode {episode_number}...")
    raw_text = fetch_subtitle_text(anime_title, episode_number)

    if not raw_text:
        return "❌ No subtitles or summaries found for this episode."

    return parse_feats_with_gpt(raw_text, anime_title, episode_number, source="Anime")
