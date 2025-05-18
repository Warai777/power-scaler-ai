def compare_stats(stats1, stats2):
    # Example logic; needs custom tuning
    score1 = len(stats1.split())
    score2 = len(stats2.split())
    if score1 > score2:
        return "Character 1 wins based on more detailed feats."
    elif score2 > score1:
        return "Character 2 wins based on more detailed feats."
    else:
        return "Equal match based on available data."
