from gpt_feat_parser import parse_feats_with_gpt
from chapter_parser.anime_parser import parse_anime_episode
from chapter_parser.chapter_parser import parse_chapter
from wiki_parsers.vs_battle_wiki_parser import fetch_vs_battle_profile
from wiki_parsers.omniversalbattle_parser import fetch_omniversal_profile
from wiki_parsers.top_strongest_parser import fetch_top_strongest_profile
from wiki_parsers.character_stat_profiles_parser import fetch_character_stat_profile
from wiki_parsers.vs_debating_parser import fetch_vs_debating_profile
from wiki_parsers.superpower_profile_parser import fetch_superpower_profile  # adjust if typo

def unified_scaling_data(name, episode=None, chapter=None):
    print(f"[+] Gathering all sources for {name}...")

    # --- Fetch wiki profiles ---
    wiki_raw = {
        "vs_battle": fetch_vs_battle_profile(name),
        "omniversal": fetch_omniversal_profile(name),
        "top_strongest": fetch_top_strongest_profile(name),
        "stat_profiles": fetch_character_stat_profile(name),
        "vs_debating": fetch_vs_debating_profile(name),
        "superpower": fetch_superpower_profile(name)
    }

    # --- Combine wiki stats into a simplified dict for GPT ---
    wiki_stats = {}
    for source, block in wiki_raw.items():
        if isinstance(block, dict):
            for key, value in block.items():
                wiki_stats[key.lower()] = value

    # --- Gather feat data from all chapter/anime sources ---
    print("[*] Collecting manga/anime feats...")

    feat_sources = []

    if chapter:
        chapter_result = parse_chapter(name, chapter)
        if chapter_result:
            feat_sources.append(f"[Chapter {chapter}] {chapter_result}")

    if episode:
        anime_result = parse_anime_episode(name, episode)
        if anime_result:
            feat_sources.append(f"[Episode {episode}] {anime_result}")

    # Optional YouTube/Reddit support
    try:
        from chapter_parser.reddit_fetcher import fetch_reddit_thread
        reddit_result = fetch_reddit_thread(name)
        if reddit_result:
            feat_sources.append(f"[Reddit Thread] {reddit_result}")
    except:
        pass

    try:
        from chapter_parser.youtube_transcript import fetch_youtube_summary
        yt_result = fetch_youtube_summary(name)
        if yt_result:
            feat_sources.append(f"[YouTube Summary] {yt_result}")
    except:
        pass

    raw_text = "\n\n".join(feat_sources)

    print("[*] Sending combined feats + wiki data to GPT for scaling...")
    result = parse_feats_with_gpt(
        raw_text=raw_text,
        series_name=name,
        chapter_number=chapter or episode,
        source="Unified",
        wiki_stats=wiki_stats
    )

    return result
