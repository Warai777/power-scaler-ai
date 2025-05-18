from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_feat(feat_text):
    prompt = f"""Extract power-scaling info from this feat:\n\nFeat: \"{feat_text}\"\n\nOutput format:\n- Destructive Capacity:\n- Speed:\n- Hax/Abilities:\n- Tier (estimation):\n- Feat Summary:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return {"parsed": response.choices[0].message.content}
