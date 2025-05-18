import schedule
import time
from multi_scraper import scrape_vs_battle_wiki
from feat_parser import parse_feat
from character_db import update_character_profile

def job():
    characters = ["Goku", "Naruto", "Ichigo"]
    for char in characters:
        raw_text = scrape_vs_battle_wiki(char)
        feat = parse_feat(raw_text)
        update_character_profile(char, feat)

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
