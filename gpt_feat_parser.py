# gpt_feat_parser.py

import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feats_with_gpt(raw_text, series_name=None, chapter_number=None, source="Unknown"):
    """
    Parses feats from a given text using GPT, tagging them with the source.

    Parameters:
    - raw_text (str): The raw string containing feats to parse
    - series_name (str): Optional label for the anime/manga/game series
    - chapter_number (str): Optional chapter or episode reference
    - source (str): Source label (e.g., 'Viz', 'MangaDex', 'Anime', 'YouTube')

    Returns:
    - str: Formatted markdown response with parsed feats
    """

    prompt = f"""
You are a power-scaling analyst AI. Analyze the feats below and extract key stats in markdown format.
Use emoji-labeled stat sections (💪 Strength, ⚡ Speed, 🧠 Intelligence, 🔮 Abilities, 🔥 Durability, etc.).
Use bullet points and finish with a short summary.

📚 Series: {series_name}
📖 Chapter/Episode: {chapter_number}
🔎 Source: {source}

📝 Raw Text:
{raw_text[:3500]}  # Trimmed to avoid overflow
---
Now extract and organize key power feats:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT parsing failed: {str(e)}"
