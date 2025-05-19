from chapter_parser.anime_parser import parse_anime_episode
from chapter_parser.chapter_parser import parse_chapter
from wiki_parsers.vs_battle_wiki_parser import fetch_vs_battle_profile


def unified_scaling_data(name, episode=None, chapter=None):
    print(f"[+] Gathering all sources for {name}...")

    wiki_block = fetch_vs_battle_profile(name) or "❌ Wiki profile not found."
    anime_block = parse_anime_episode(name, episode) if episode else "⏭ No anime episode given."
    manga_block = parse_chapter(name, chapter) if chapter else "⏭ No manga chapter given."

    combined = f"""
## 📘 Manga Feats (Chapter {chapter})
{manga_block}

## 📺 Anime Feats (Episode {episode})
{anime_block}

## 🧾 VS Battle Wiki Summary
{wiki_block}
"""
    return combined
