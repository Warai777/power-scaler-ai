# gpt_feat_parser.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feats_with_gpt(text, source=None):
    prompt = f"""
You are a power-scaling AI. Parse the following scene and extract all relevant power feats. 
Use bullet points. Bold important stats (e.g., **Speed**, **Strength**, **Tier**). 

Scene:
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
        print("[GPT Parsing Error]", e)
        return "Error parsing feats."
