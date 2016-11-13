from random import choice
from string import digits


def getRand():
    new_rand = choice(digits)
    return int(new_rand)
