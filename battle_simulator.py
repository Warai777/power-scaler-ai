from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def simulate_battle(char1, char2):
    prompt = f"""Simulate a battle between {char1} and {char2}.
Base it on logic, powerscaling, win conditions, hax, and speed.
Give a win rate and reasoning. Be accurate.

Output format:
- Winner:
- Win Rate:
- Key Advantages:
- Battle Summary:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return {"result": response.choices[0].message.content}
