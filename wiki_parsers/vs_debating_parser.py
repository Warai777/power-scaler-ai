import requests
from bs4 import BeautifulSoup
import re

def fetch_vs_debating_profile(term_or_character):
    try:
        query = term_or_character.replace(" ", "+") + "+site:vsdebating.fandom.com"
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(search_url, headers=headers)
        matches = re.findall(r"https://vsdebating\.fandom\.com/wiki/[^"]+", res.text)

        if not matches:
            print("[VSDebating] No page found.")
            return None

        page_url = matches[0]
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_text = soup.get_text(separator="\n")

        # Focus on cosmology, definitions, logic, examples
        capture_lines = []
        capture = False
        for line in raw_text.splitlines():
            if any(k in line for k in ["Cosmology", "Explanation", "Definition", "Tiers", "Scaling", "Examples"]):
                capture = True
            if capture:
                if line.strip() == "" or "Navigation" in line:
                    break
                capture_lines.append(line.strip())

        summary = f"**VS Debating Wiki Reference: {term_or_character}**\n\n"
        summary += "\n".join(capture_lines)
        return summary.strip()

    except Exception as e:
        print(f"[VS Debating Parser Error] {e}")
        return None
