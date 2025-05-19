import re

# Define keywords or phrases that usually signal feats
FEAT_KEYWORDS = [
    r"faster than (light|sound|the eye)",
    r"destroy(ed)? (a|the)? (mountain|city|planet|dimension)",
    r"(can|could|was able to) (punch|move|hit|teleport|dodge|react) .* (instantaneously|in (an|a)? (instant|blink))",
    r"(launched|threw|knocked).* (across|through).* (wall|building|sky)",
    r"(survived|tanked|endured).* (explosion|blast|attack)",
    r"(final form|transformation|ascended|awakening|evolved)",
    r"(Bankai|Kamehameha|Rasengan|Chidori|One For All|Gear [0-9])",
    r"(time stop|dimension travel|teleportation|reality warping)"
]

# Compile all regexes for performance
FEAT_REGEXES = [re.compile(k, re.IGNORECASE) for k in FEAT_KEYWORDS]

def parse_subtitles(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    feats = []

    for sentence in sentences:
        for pattern in FEAT_REGEXES:
            if pattern.search(sentence):
                feats.append(sentence.strip())
                break

    return feats
