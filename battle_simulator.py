import re
from battle_engine import simulate_battle

def simulate_battle(char1, char2):
    try:
        prompt = f"""
You are a battle simulation AI.
Simulate a fight between **{char1}** and **{char2}** using feats, logic, stats, and real matchups from manga/anime/game sources.

Respond in this markdown format:
- **Winner**: 
- **Speed**: 
- **Strength**: 
- **Durability**: 
- **Key Abilities**: 
- **Battle Summary**: Short summary with tactics or strategies.
"""
        return simulate_battle(char1, char2)
    except Exception as e:
        print(f"[Battle Error] {e}")
        return {"result": "Battle simulation failed."}
