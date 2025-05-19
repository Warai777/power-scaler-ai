import requests
from bs4 import BeautifulSoup
import re

def fetch_vs_battle_profile(character_name):
    try:
        search_query = character_name.replace(" ", "+") + "+site:vsbattles.fandom.com"
        search_url = f"https://www.google.com/search?q={search_query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(search_url, headers=headers)

        # Find the first valid VSBattles link
        matches = re.findall(r"https://vsbattles\.fandom\.com/wiki/[^"]+", res.text)
        if not matches:
            print("[VSBattles] No profile found.")
            return None

        profile_url = matches[0]
        page = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Extract raw content
        text = soup.get_text(separator="\n")

        # Try to extract Tier and Stats block manually
        tier_match = re.search(r"Tier:\s*(.+)", text)
        tier = tier_match.group(1).strip() if tier_match else "Unknown"

        stats_block = []
        collecting = False
        for line in text.split("\n"):
            if "Attack Potency" in line:
                collecting = True
            if collecting:
                if line.strip() == "" or "Standard Equipment" in line:
                    break
                stats_block.append(line.strip())

        result = f"**Character:** {character_name}\n\n"
        result += f"**Tier:** {tier}\n"
        result += "\n**Stats & Abilities:**\n"
        result += "\n".join(stats_block)

        return result

    except Exception as e:
        print(f"[VSBattles Error] {e}")
        return None
