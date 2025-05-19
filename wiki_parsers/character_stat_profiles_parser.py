import requests
from bs4 import BeautifulSoup
import re

def fetch_character_stat_profile(character_name):
    try:
        query = character_name.replace(" ", "+") + "+site:character-stat-profiles.fandom.com"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(search_url, headers=headers)
        matches = re.findall(r"https://character-stat-profiles\.fandom\.com/wiki/[^"]+", res.text)

        if not matches:
            print("[CharStatProfiles] No result.")
            return None

        page_url = matches[0]
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_text = soup.get_text(separator="\n")

        tier_match = re.search(r"Tier\s*:\s*(.+)", raw_text)
        tier = tier_match.group(1).strip() if tier_match else "Unknown"

        block = []
        start = False
        for line in raw_text.splitlines():
            if any(keyword in line for keyword in ["Attack Potency", "Speed", "Durability", "Stamina", "Abilities"]):
                start = True
            if start:
                if line.strip() == "" or "Standard Equipment" in line:
                    break
                block.append(line.strip())

        summary = f"**Character:** {character_name}\n\n"
        summary += f"**Tier:** {tier}\n\n"
        summary += "**Character & Stat Profiles Wiki Data:**\n"
        summary += "\n".join(block)
        return summary

    except Exception as e:
        print(f"[CharStatProfile Error] {e}")
        return None
