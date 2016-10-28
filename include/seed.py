from random import choice
from string import digits


def getRand():
    global rand_seed
    new_rand = choice(digits)
    rand_seed = rand_seed + new_rand
    return int(new_rand)

def createSeed():
    global rand_seed
    rand_seed = ''.join(choice(digits) for a in range(150))
