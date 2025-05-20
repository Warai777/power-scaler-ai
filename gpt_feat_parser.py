import os
from openai import OpenAI
from config import OPENAI_API_KEY
from smart_chunker import chunk_text  # ✅ NEW

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feats_with_gpt(raw_text, series_name=None, chapter_number=None, source="Unknown", wiki_stats=None):
    """
    Parses feats from a given text using GPT, comparing against wiki stats if available.

    Parameters:
    - raw_text (str): Combined raw feat text from chapters, anime, Reddit, etc.
    - series_name (str): Optional series label
    - chapter_number (int): Optional chapter or episode number
    - source (str): Where this came from (e.g. "Auto Power Profile", "Unified Scaling")
    - wiki_stats (dict): Optional dictionary of stats pulled from wikis

    Returns:
    - str: Markdown-formatted VS Battle Wiki power profile
    """

    wiki_context = ""
    if wiki_stats:
        wiki_context += "Use the following wiki stats as reference, but override them if the feats below suggest a higher tier:\n"
        for key, value in wiki_stats.items():
            wiki_context += f"- {key.title()}: {value}\n"

    all_chunks = chunk_text(raw_text, max_tokens=7000)
    outputs = []

    for idx, chunk in enumerate(all_chunks):
        prompt = f"""
You are a power-scaling analyst AI trained to use the Versus Battle Wiki tiering system.

Using the feats and stats below, generate a full character profile in markdown.
If new feats show stronger scaling than existing wiki tiers, override the wiki tier and explain why.

Respond in this format:

**Name:** [Character Name]  
**Verse:** [Series]  
**Tier:** [Tier]  
**Attack Potency:**  
**Speed:**  
**Durability:**  
**Striking Strength:**  
**Lifting Strength:**  
**Stamina:**  
**Range:**  
**Standard Equipment:**  
**Intelligence:**  
**Notable Abilities:**  
**Feats:**  
- Bullet summary of key feats
**Wiki Discrepancy:**  
- If you overrode any outdated wiki tiers, explain why

{wiki_context}

--- FEAT DATA BEGIN ---
{chunk}
--- FEAT DATA END ---
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a power-scaling AI following the Versus Battle Wiki format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )

        outputs.append(response.choices[0].message.content.strip())

    return "\n\n---\n\n".join(outputs)
