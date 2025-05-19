from chapter_parser.anime_parser import parse_anime_episode
from chapter_parser.chapter_parser import parse_chapter
from wiki_parsers.vs_battle_wiki_parser import fetch_vs_battle_profile
from wiki_parsers.omniversalbattle_parser import fetch_omniversal_profile
from wiki_parsers.top_strongest_parser import fetch_top_strongest_profile
from wiki_parsers.character_stat_profiles_parser import fetch_character_stat_profile
from wiki_parsers.vs_debating_parser import fetch_vs_debating_profile
from wiki_parsers.superpower_wiki_parser import fetch_superpower_profile

def unified_scaling_data(name, episode=None, chapter=None):
    print(f"[+] Gathering all sources for {name}...")

    wiki_block = fetch_vs_battle_profile(name) or "❌ VS Battle Wiki not found."
    omni_block = fetch_omniversal_profile(name) or "❌ Omniversal Wiki not found."
    top_block = fetch_top_strongest_profile(name) or "❌ Top-Strongest Wiki not found."
    stat_block = fetch_character_stat_profile(name) or "❌ CharStat Wiki not found."
    debate_block = fetch_vs_debating_profile(name) or "❌ VS Debating entry not found."
    ability_block = fetch_superpower_profile(name) or "❌ Superpower Wiki entry not found."

    anime_block = parse_anime_episode(name, episode) if episode else "⏭ No anime episode given."
    manga_block = parse_chapter(name, chapter) if chapter else "⏭ No manga chapter given."

    combined = f"""
## 📘 Manga Feats (Chapter {chapter})
{manga_block}

## 📺 Anime Feats (Episode {episode})
{anime_block}

## 🧾 VS Battle Wiki
{wiki_block}

## 🌌 Omniversal Battlefield Wiki
{omni_block}

## 🔱 Top-Strongest Wiki
{top_block}

## 🛡 Character & Stat Profiles
{stat_block}

## 🧠 VS Debating Wiki
{debate_block}

## 🧬 Superpower Wiki (Ability Labeling)
{ability_block}
"""
    return combined.strip()
