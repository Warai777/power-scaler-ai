import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def parse_feat(feat_text):
    prompt = f"""Extract power-scaling info from this feat:

Feat: "{feat_text}"

Output format:
- Destructive Capacity:
- Speed:
- Hax/Abilities:
- Tier (estimation):
- Feat Summary:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return {"parsed": response['choices'][0]['message']['content']}
