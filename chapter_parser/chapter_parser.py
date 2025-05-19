from viz_scraper import fetch_viz_chapter
from mangadex_scraper import fetch_mangadex_chapter
from youtube_transcript import fetch_youtube_summary
from reddit_fetcher import fetch_reddit_summary
from gpt_faeat_parser import parse_feats_with_gpt


def parse_chapter(series_name, chapter_number):
    print(f"[+] Starting feat parser for {series_name} Chapter {chapter_number}...")

    # 1. Try Viz
    viz_text = fetch_viz_chapter(series_name, chapter_number)
    if viz_text:
        from logger import log_source_used
log_source_used(series_name, chapter_number, "Viz")

        return parse_feats_with_gpt(viz_text, series_name, chapter_number, source="Viz")

    # 2. Try MangaDex
    md_text = fetch_mangadex_chapter(series_name, chapter_number)
    if md_text:
        print("[✓] Parsed chapter from MangaDex")
        return parse_feats_with_gpt(md_text, series_name, chapter_number, source="MangaDex")

    # 3. Try YouTube Transcript
    yt_text = fetch_youtube_summary(series_name, chapter_number)
    if yt_text:
        print("[✓] Parsed chapter summary from YouTube")
        return parse_feats_with_gpt(yt_text, series_name, chapter_number, source="YouTube")

    # 4. Try Reddit
    reddit_text = fetch_reddit_summary(series_name, chapter_number)
    if reddit_text:
        print("[✓] Parsed chapter summary from Reddit")
        return parse_feats_with_gpt(reddit_text, series_name, chapter_number, source="Reddit")

    print("[✗] Failed to retrieve chapter text from all sources.")
    return "❌ No valid data found from Viz, MangaDex, YouTube, or Reddit. Please try again later or with a different chapter."
