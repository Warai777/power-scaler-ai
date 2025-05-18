import re

def parse_subtitles(text):
    feats = re.findall(r"[A-Z][^.?!]*[.?!]", text)
    return feats
