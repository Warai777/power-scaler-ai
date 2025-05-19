import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_feats_with_gpt(raw_text, series_name, chapter_number, source="Unknown"):
    prompt = f"""
You are a power-scaling analyst AI.
Using the raw chapter or summary below from {source}, extract any feats, tier implications, scaling, or character powers.

Respond using clean markdown with:
- ✅ Emoji-labeled sections
- 📊 Power-scaling bullets
- 🔚 Summary with tier shifts (if any)

### 📖 Series: {series_name}
### 📄 Chapter: {chapter_number}

---

### 🔍 Raw Text:
{raw_text[:3500]}  # Limit to avoid overflow

---

Now parse and format the key power feats:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()
