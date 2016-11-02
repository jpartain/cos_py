import logging
import include.town as town
import include.seed as seed

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'info.log', level = logging.DEBUG)


def generateTown():
    new_town = town.Town()

    '''
    print('')
    print('Nobles placed:\t', new_town.placed_nobles)
    print('Middle placed:\t', new_town.placed_middle)
    print('Poor placed:\t', new_town.placed_poor)
    print('Wealth:\t\t', new_town.wealth)
    print('Economy:\t', new_town.economy)
    print('Danger:\t\t', new_town.danger)
    print('Settled:\t', new_town.settled_ratio, '%')
    print('Nobility:\t', new_town.nobility, '%')
    print('')

    new_town.printMapCorners()
    '''

def main():
    seed.createSeed()
    generateTown()

    #input('Press enter to close this window.')

if __name__ == '__main__':
    main()
