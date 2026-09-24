BASE_COST = 100.0
SPEED_INCREMENT = 25
BASE_MAX_SPEED = 150


def cost(level):
    return BASE_COST * (level + 1)


def max_speed(level):
    return BASE_MAX_SPEED + (level * SPEED_INCREMENT)
