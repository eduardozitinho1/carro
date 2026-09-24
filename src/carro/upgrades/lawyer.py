BASE_COST = 150.0


def cost(level):
    return BASE_COST * (level + 1)


def arrest_chance(base_chance, lawyers):
    return base_chance / (1 + lawyers)
