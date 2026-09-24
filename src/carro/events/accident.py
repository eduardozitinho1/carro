BASE_CHANCE = 0.0005
MAX_REDUCTION = 0.95
REDUCTION_PER_AIRBAG = 0.25


def chance(airbag_level):
    reduction = min(
        airbag_level * REDUCTION_PER_AIRBAG,
        MAX_REDUCTION,
    )

    return BASE_CHANCE * (1 - reduction)
