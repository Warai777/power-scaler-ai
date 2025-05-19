from gpt_feat_parser import parse_feats_with_gpt
from chapter_parser.anime_parser import parse_anime_episode
from chapter_parser.chapter_parser import parse_chapter
from chapter_parser.chapter_tracker import get_last_parsed, update_last_parsed
from chapter_parser.latest_fetcher import get_latest_chapter, get_latest_episode  # ✅ NEW
from wiki_parsers.vs_battle_wiki_parser import fetch_vs_battle_profile
from wiki_parsers.omniversalbattle_parser import fetch_omniversal_profile
from wiki_parsers.top_strongest_parser import fetch_top_strongest_profile
from wiki_parsers.character_stat_profiles_parser import fetch_character_stat_profile
from wiki_parsers.vs_debating_parser import fetch_vs_debating_profile
from wiki_parsers.superpower_wiki_parser import fetch_superpower_profile
from name_resolver import resolve_character_name  # ✅ NEW

def unified_scaling_data(name):
    name = resolve_character_name(name)  # ✅ Normalize nickname
    print(f"[+] Gathering all sources for {name}...")

    # --- Wiki Profiles ---
    wiki_raw = {
        "vs_battle": fetch_vs_battle_profile(name),
        "omniversal": fetch_omniversal_profile(name),
        "top_strongest": fetch_top_strongest_profile(name),
        "stat_profiles": fetch_character_stat_profile(name),
        "vs_debating": fetch_vs_debating_profile(name),
        "superpower": fetch_superpower_profile(name)
    }

    wiki_stats = {}
    for source, block in wiki_raw.items():
        if isinstance(block, dict):
            for key, value in block.items():
                wiki_stats[key.lower()] = value

    # --- Load scan progress
    progress = get_last_parsed(name)
    last_chapter = progress.get("last_chapter", 1)
    last_episode = progress.get("last_episode", 1)

    # ✅ Get latest available chapter and episode dynamically
    latest_chapter = get_latest_chapter(name)
    latest_episode = get_latest_episode(name)

    print(f"[*] Scanning chapters {last_chapter + 1} to {latest_chapter}...")
    print(f"[*] Scanning episodes {last_episode + 1} to {latest_episode}...")

    feat_sources = []

    # Chapters
    for ch in range(last_chapter + 1, latest_chapter + 1):
        try:
            ch_result = parse_chapter(name, ch)
            if ch_result:
                print(f"[✓] Chapter {ch}")
                feat_sources.append(f"[Chapter {ch}] {ch_result}")
                update_last_parsed(name, chapter=ch)
        except Exception as e:
            print(f"[✗] Chapter {ch} skipped: {e}")

    # Episodes
    for ep in range(last_episode + 1, latest_episode + 1):
        try:
            ep_result = parse_anime_episode(name, ep)
            if ep_result:
                print(f"[✓] Episode {ep}")
                feat_sources.append(f"[Episode {ep}] {ep_result}")
                update_last_parsed(name, episode=ep)
        except Exception as e:
            print(f"[✗] Episode {ep} skipped: {e}")

    # Optional sources
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
    if not raw_text.strip():
        return f"⚠️ No new feats found for {name}."

    print("[*] Sending new data to GPT...")
    result = parse_feats_with_gpt(
        raw_text=raw_text,
        series_name=name,
        chapter_number=0,
        source="Smart Incremental Scaling",
        wiki_stats=wiki_stats
    )

    return result
