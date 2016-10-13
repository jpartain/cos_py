from random import choice
from string import digits

from include.town import *

def generateTown(random_seed):
    town = Town(random_seed)

    """
    print('')
    print('Wealth:\t\t', town.getWealth())
    print('Economy:\t', town.getEconomy())
    print('Danger:\t\t', town.getDanger())
    print('Settled:\t', town.getSettledRatio(), '%')
    print('Nobility:\t', town.getNobility(), '%')
    print('')

    town.printMapCorners()
    """

def main():
    random_string = ''.join(choice(digits) for a in range(150))
    generateTown(random_string)

    #input('Press enter to close this window.')

if __name__ == '__main__':
    main()
