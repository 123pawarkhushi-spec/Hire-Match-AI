
def calculate_final_score(skill_score, text_similarity):

    final_score = (
        (0.70 * skill_score) +
        (0.30 * text_similarity)
    )

    return round(final_score, 2)
