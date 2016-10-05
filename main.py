from random import choice
from string import digits

from include.town import *
from include.building import *
from include.person import *

def generateTown(random_seed):
    town = Town(random_seed)

    print('')
    print('Wealth:\t\t', town.getWealth())
    print('Economy:\t', town.getEconomy())
    print('Danger:\t\t', town.getDanger())
    print('Settled:\t', town.getSettledRatio(), '%')
    print('Nobility:\t', town.getNobility(), '%')
    print('')

def main():
    random_string = ''.join(choice(digits) for a in range(63))
    generateTown(random_string)

if __name__ == '__main__':
    main()
