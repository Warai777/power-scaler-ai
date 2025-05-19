import os
from chapter_parser.kitsunekko_scraper import fetch_kitsunekko_subtitles
from chapter_parser.youtube_transcript import fetch_youtube_summary
from gpt_feat_parser import parse_feats_with_gpt
from chapter_parser.logger import log_source_used
from cache import load_cache, save_cache


def fetch_subtitle_text(anime_title, episode_number):
    # 1. Try Kitsunekko subtitles
    subtitle_text = fetch_kitsunekko_subtitles(anime_title, episode_number)
    if subtitle_text:
        log_source_used(anime_title, episode_number, "Kitsunekko")
        return subtitle_text

    # 2. Fallback to YouTube summaries
    yt_text = fetch_youtube_summary(anime_title, episode_number)
    if yt_text:
        log_source_used(anime_title, episode_number, "YouTube")
        return yt_text

    return None


def parse_anime_episode(anime_title, episode_number):
    key = f"anime_{anime_title}_{episode_number}"
    cached = load_cache(key)
    if cached:
        print("[✓] Loaded cached result")
        return cached

    print(f"[+] Starting anime feat parser for {anime_title} Episode {episode_number}...")
    raw_text = fetch_subtitle_text(anime_title, episode_number)

    if not raw_text:
        return "❌ No subtitles or summaries found for this episode."

    result = parse_feats_with_gpt(
        raw_text,
        anime_title,
        episode_number,
        source="Anime (Subs/YouTube)"
    )
    save_cache(key, result)
    return result

