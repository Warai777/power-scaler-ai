import requests
from bs4 import BeautifulSoup
import re

def fetch_omniversal_profile(character_name):
    try:
        query = character_name.replace(" ", "+") + "+site:omniversal-battlefield.fandom.com"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(search_url, headers=headers)
        matches = re.findall(r"https://omniversal-battlefield\.fandom\.com/wiki/[^"]+", resp.text)

        if not matches:
            print("[Omniversal] No page found.")
            return None

        profile_url = matches[0]
        page = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_text = soup.get_text(separator="\n")

        # Extract key stats and power sections
        tier = re.search(r"Tier\s*:\s*(.+)", raw_text)
        tier_str = tier.group(1).strip() if tier else "Unknown"

        # Search for a power/ability/stat block
        block = []
        capturing = False
        for line in raw_text.splitlines():
            if any(k in line for k in ["Attack Potency", "Powers", "Speed", "Abilities"]):
                capturing = True
            if capturing:
                if line.strip() == "" or "Standard Equipment" in line:
                    break
                block.append(line.strip())

        summary = f"**Character:** {character_name}\n\n"
        summary += f"**Tier:** {tier_str}\n\n"
        summary += "**Omniversal Battlefield Stats:**\n"
        summary += "\n".join(block)
        return summary

    except Exception as e:
        print(f"[Omniversal Parser Error] {e}")
        return None
