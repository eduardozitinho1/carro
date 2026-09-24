import random
from time import sleep


CHANCE = 0.015
MIN_DURATION = 2
MAX_DURATION = 8


def traffic():
    duration = random.uniform(MIN_DURATION, MAX_DURATION)
    sleep(duration)
    return duration
