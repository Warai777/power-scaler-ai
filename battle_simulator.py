import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def simulate_battle(char1, char2):
    prompt = f"""Simulate a battle between {char1} and {char2}.\nBase it on logic, powerscaling, win conditions, hax, and speed.\nGive a win rate and reasoning. Be accurate.\n\nOutput format:\n- Winner:\n- Win Rate:\n- Key Advantages:\n- Battle Summary:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return {"result": response['choices'][0]['message']['content']}
