from random import choice
from string import digits

from include.town import *

def generateTown(random_seed):
    town = Town(random_seed)

    print('')
    print('Wealth:\t\t', town.wealth)
    print('Economy:\t', town.economy)
    print('Danger:\t\t', town.danger)
    print('Settled:\t', town.settled_ratio, '%')
    print('Nobility:\t', town.nobility, '%')
    print('')

    town.printMapCorners()

def main():
    random_string = ''.join(choice(digits) for a in range(150))
    generateTown(random_string)

    #input('Press enter to close this window.')

if __name__ == '__main__':
    main()
