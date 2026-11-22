
def rank_candidates(candidates):

    ranked_candidates = sorted(
        candidates,
        key=lambda candidate: candidate["final_score"],
        reverse=True
    )

    return ranked_candidates
