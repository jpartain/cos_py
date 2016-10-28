from random import choice
from string import digits

from include.town import *
import include.seed as seed

def generateTown(random_seed):
    town = Town(random_seed)

    print('')
    print('Nobles placed:\t', town.placed_nobles)
    print('Middle placed:\t', town.placed_middle)
    print('Poor placed:\t', town.placed_poor)
    print('Wealth:\t\t', town.wealth)
    print('Economy:\t', town.economy)
    print('Danger:\t\t', town.danger)
    print('Settled:\t', town.settled_ratio, '%')
    print('Nobility:\t', town.nobility, '%')
    print('')

    town.printMapCorners()

def main():
    seed.createSeed()
    generateTown(seed.rand_seed)

    #input('Press enter to close this window.')

if __name__ == '__main__':
    main()
