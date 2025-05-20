import re
from collections import defaultdict

def extract_section(markdown, section):
    pattern = rf"\*\*{re.escape(section)}:\*\*\s*(.*?)\n(?=\*\*|$)"
    match = re.search(pattern, markdown, re.DOTALL)
    return match.group(1).strip() if match else ""

def merge_power_profiles(chunks):
    """
    Takes a list of markdown power profiles (from multiple GPT chunks)
    and merges them into a clean, unified profile.
    """
    merged = defaultdict(set)
    highest_tier = "Unknown"
    feats = set()
    abilities = set()
    discrepancies = set()

    for chunk in chunks:
        tier = extract_section(chunk, "Tier")
        if tier:
            if "" in highest_tier or compare_tiers(tier, highest_tier):
                highest_tier = tier

        feats_text = extract_section(chunk, "Feats")
        for line in feats_text.split("\n"):
            if line.strip().startswith("-"):
                feats.add(line.strip())

        abil_text = extract_section(chunk, "Notable Abilities")
        for line in abil_text.split("\n"):
            if line.strip():
                abilities.add(line.strip())

        wiki_text = extract_section(chunk, "Wiki Discrepancy")
        for line in wiki_text.split("\n"):
            if line.strip():
                discrepancies.add(line.strip())

    output = f"""
**Tier:** {highest_tier}  

**Notable Abilities:**
{chr(10).join(f"- {a}" for a in sorted(abilities))}

**Feats:**
{chr(10).join(sorted(feats))}

**Wiki Discrepancy:**
{chr(10).join(f"- {d}" for d in sorted(discrepancies))}
"""
    return output.strip()

def compare_tiers(tier_a, tier_b):
    """
    Compares VS Battle Wiki tiers and returns True if A > B
    Simplified version using a hardcoded scale.
    """
    scale = [
        "10-C", "10-B", "10-A",
        "9-C", "9-B", "9-A",
        "8-C", "8-B", "8-A",
        "7-C", "7-B", "7-A",
        "6-C", "6-B", "6-A",
        "5-C", "5-B", "5-A",
        "4-C", "4-B", "4-A",
        "3-C", "3-B", "3-A",
        "2-C", "2-B", "2-A",
        "1-C", "1-B", "1-A",
        "High 1-C", "1-B+", "1-A+", "0"
    ]
    try:
        return scale.index(tier_a) > scale.index(tier_b)
    except:
        return False
