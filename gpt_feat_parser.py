# gpt_feat_parser.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feats_with_gpt(text, source=None):
    """
    Parses feats from a given text using GPT, tagging them with the source.

    Parameters:
    - text (str): The raw string containing feats to parse
    - source (str): Optional label for where the feats came from (e.g., "wiki", "anime", "manga")

    Returns:
    - str: Formatted response with parsed feats
    """
    
    prompt = f"""
You are a power-scaling AI. Analyze the feats below and extract key stats in markdown format.
Include **bolded stat labels** (like **Speed**, **Tier**, etc.), use bullet points, and end with a summary.

Source: {source}

Feats:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT parsing failed: {str(e)}"
