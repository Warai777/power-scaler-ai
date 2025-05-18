import requests
from bs4 import BeautifulSoup

def scrape_vs_battle_wiki(character):
    url = f"https://vsbattles.fandom.com/wiki/{character.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.get_text()
