from viz_scraper import fetch_viz_chapter
from mangadex_scraper import fetch_mangadex_chapter
from youtube_transcript import fetch_youtube_summary
from reddit_fetcher import fetch_reddit_summary
from gpt_feat_parser import parse_feats_with_gpt
from logger import log_source_used
from cache import load_cache, save_cache

def parse_chapter(series_name, chapter_number):
    print(f"[+] Starting feat parser for {series_name} Chapter {chapter_number}...")

    cache_key = f"manga_{series_name}_{chapter_number}".lower()
    cached = load_cache(cache_key)
    if cached:
        print("[✓] Loaded cached result")
        return cached

    # 1. Try Viz
    viz_text = fetch_viz_chapter(series_name, chapter_number)
    if viz_text:
        log_source_used(series_name, chapter_number, "Viz")
        result = parse_feats_with_gpt(viz_text, series_name, chapter_number, source="Viz")
        save_cache(cache_key, result)
        return result

    # 2. Try MangaDex
    md_text = fetch_mangadex_chapter(series_name, chapter_number)
    if md_text:
        log_source_used(series_name, chapter_number, "MangaDex")
        result = parse_feats_with_gpt(md_text, series_name, chapter_number, source="MangaDex")
        save_cache(cache_key, result)
        return result

    # 3. Try YouTube
    yt_text = fetch_youtube_summary(series_name, chapter_number)
    if yt_text:
        log_source_used(series_name, chapter_number, "YouTube")
        result = parse_feats_with_gpt(yt_text, series_name, chapter_number, source="YouTube")
        save_cache(cache_key, result)
        return result

    # 4. Try Reddit
    reddit_text = fetch_reddit_summary(series_name, chapter_number)
    if reddit_text:
        log_source_used(series_name, chapter_number, "Reddit")
        result = parse_feats_with_gpt(reddit_text, series_name, chapter_number, source="Reddit")
        save_cache(cache_key, result)
        return result

    print("[✗] Failed to retrieve chapter text from all sources.")
    return "❌ No valid data found from Viz, MangaDex, YouTube, or Reddit. Please try again later or with a different chapter."
