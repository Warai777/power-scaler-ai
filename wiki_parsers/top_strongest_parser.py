import requests
from bs4 import BeautifulSoup
import re

def fetch_top_strongest_profile(character_name):
    try:
        query = character_name.replace(" ", "+") + "+site:top-strongest.fandom.com"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(search_url, headers=headers)
        matches = re.findall(r"https://top-strongest\.fandom\.com/wiki/[^"]+", resp.text)

        if not matches:
            print("[TopStrongest] No profile found.")
            return None

        profile_url = matches[0]
        page = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_text = soup.get_text(separator="\n")

        # Try extracting Tier/Attack Potency block
        tier_match = re.search(r"Tier\s*:\s*(.+)", raw_text)
        tier = tier_match.group(1).strip() if tier_match else "Unknown"

        block = []
        recording = False
        for line in raw_text.splitlines():
            if any(k in line for k in ["Attack Potency", "Speed", "Lifting Strength", "Abilities"]):
                recording = True
            if recording:
                if line.strip() == "" or "Standard Equipment" in line:
                    break
                block.append(line.strip())

        summary = f"**Character:** {character_name}\n\n"
        summary += f"**Tier:** {tier}\n\n"
        summary += "**Top-Strongest Stats:**\n"
        summary += "\n".join(block)
        return summary

    except Exception as e:
        print(f"[TopStrongest Parser Error] {e}")
        return None
