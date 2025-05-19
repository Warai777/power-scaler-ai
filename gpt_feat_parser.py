import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feats_with_gpt(raw_text, series_name=None, chapter_number=None, source="Unknown", wiki_stats=None):
    """
    Parses feats from a given text using GPT, tagging them with the source and comparing against wiki data.

    Parameters:
    - raw_text (str): The raw string containing feats to parse
    - series_name (str): Optional label for the anime/manga/game series
    - chapter_number (str): Optional chapter or episode reference
    - source (str): Source label (e.g., 'Viz', 'MangaDex', 'Anime', 'YouTube')
    - wiki_stats (dict): Parsed wiki stats to compare against (e.g., tier, durability, attack potency)

    Returns:
    - str: Formatted markdown response with parsed feats in VS Battle Wiki format
    """

    wiki_context = ""
    if wiki_stats:
        wiki_context += "Use the following wiki stats as historical reference. If feats show a higher tier, override them:\n"
        for key, value in wiki_stats.items():
            wiki_context += f"- {key.title()}: {value}\n"

    prompt = f"""
You are a power-scaling analyst AI trained in the Versus Battle Wiki format.

Given the following raw feat descriptions from the manga, anime, and community summaries, extract the character's power stats using VS Battle Wiki's tiering system (e.g., 7-A, 5-C, etc.). Prioritize new feats if they show higher scaling than existing wiki entries.

If the feat shows a stronger tier than the wiki entry, override it and note the discrepancy.

Respond in this exact markdown format:

**Name:** [Character]  
**Verse:** [Series]  
**Tier:** [Final Tier]  
**Attack Potency:** [Summary]  
**Speed:** [Summary]  
**Lifting Strength:** [Summary]  
**Striking Strength:** [Summary]  
**Durability:** [Summary]  
**Stamina:** [Summary]  
**Range:** [Summary]  
**Standard Equipment:** [Summary]  
**Intelligence:** [Summary]  
**Notable Abilities:** [List of Abilities]  
**Feats:**  
- [Short bullet list of actual feat summaries with source]

**Wiki Discrepancy:**  
- If any wiki tier was overridden, explain it here.

{wiki_context}

--- BEGIN FEATS ---
{raw_text}
--- END FEATS ---
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a power-scaling AI trained in VS Battle Wiki standards."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()
