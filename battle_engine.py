from gpt_feat_parser import parse_feats_with_gpt
from cache import load_cache, save_cache

def simulate_battle(char1, char2):
    matchup = f"battle_{char1}_vs_{char2}".lower().replace(" ", "_")
    cached = load_cache(matchup)
    if cached:
        print("[✓] Loaded cached battle result")
        return cached

    prompt = f"""
You are a battle simulation AI. Simulate a full analysis between **{char1}** and **{char2}** based on logic, feats, and power-scaling.

Instructions:
- Use markdown format
- Include emoji headers
- Provide win rate % (if possible)
- Highlight **Key Abilities**, **Advantages**, **Conclusion**

Now simulate the full matchup.
"""

    result = parse_feats_with_gpt(prompt, f"{char1} vs {char2}", 0, source="Battle Simulation")
    save_cache(matchup, result)
    return result
