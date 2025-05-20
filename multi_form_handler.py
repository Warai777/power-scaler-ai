import re
from collections import defaultdict

def detect_forms(raw_text):
    """
    Scans feat text and attempts to split data into forms like:
    - Base Form
    - Gear 2 / Gear 5
    - Super Saiyan / Bankai / Sage Mode etc.
    """
    form_patterns = [
        r"\b(base form|base|normal|human)\b",
        r"\b(gear \d|gear five|gear 5)\b",
        r"\b(super saiyan(?: \d)?|ssj(?:\d)?)\b",
        r"\b(bankai|shikai|hollow)\b",
        r"\b(sage mode|baryon mode|six paths)\b",
        r"\b(awakening|ultimate|transcendent|true form|final form)\b",
    ]

    form_data = defaultdict(list)
    lines = raw_text.split("\n")

    for line in lines:
        found = False
        for pattern in form_patterns:
            match = re.search(pattern, line.lower())
            if match:
                key = match.group(1).title()
                form_data[key].append(line.strip())
                found = True
                break
        if not found:
            form_data["Base"].append(line.strip())

    return form_data

def format_multi_form_profile(form_data, wiki_stats=None):
    """
    Accepts separated form data and returns one large markdown profile
    with section headers for each form.
    """
    wiki_block = ""
    if wiki_stats:
        wiki_block += "\n\n**Wiki Stats Reference:**\n"
        for k, v in wiki_stats.items():
            wiki_block += f"- {k.title()}: {v}\n"

    output = ""
    for form, feats in form_data.items():
        output += f"\n### {form} Form\n"
        output += "\n**Feats:**\n"
        for line in feats:
            if not line.startswith("-"):
                output += f"- {line}\n"

    return output.strip() + wiki_block
