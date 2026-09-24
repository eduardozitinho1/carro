BASE_COST = 100.0
CHANCE_REDUCTION = 0.25


def cost(level):
    return BASE_COST * (level + 1)


def reduction(level):
    return min(level * CHANCE_REDUCTION, 0.95)
