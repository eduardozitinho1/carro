ARREST_CHANCE = 0.4
RECKLESSNESS_CHANCE = 0.002
BREATHALYZER_CHANCE = 0.75


def arrest_chance(lawyers):
    return ARREST_CHANCE / (1 + lawyers)
