import requests
from bs4 import BeautifulSoup
import re

def fetch_superpower_profile(power_term):
    try:
        query = power_term.replace(" ", "+") + "+site:powerlisting.fandom.com"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(search_url, headers=headers)
        matches = re.findall(r"https://powerlisting\.fandom\.com/wiki/[^"]+", res.text)

        if not matches:
            print("[Superpower Wiki] No match found.")
            return None

        url = matches[0]
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_text = soup.get_text(separator="\n")

        intro = []
        capture = False
        for line in raw_text.splitlines():
            if "Power/Ability" in line or "Capabilities" in line:
                capture = True
            if capture:
                if line.strip() == "" or "Limitations" in line:
                    break
                intro.append(line.strip())

        summary = f"**Superpower Wiki – {power_term}**\n\n"
        summary += "\n".join(intro)
        return summary.strip()

    except Exception as e:
        print(f"[Superpower Wiki Parser Error] {e}")
        return None
