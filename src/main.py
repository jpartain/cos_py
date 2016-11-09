import logging
from kivy.app import App
from kivy.uix.widget import Widget

import town
import seed


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


class CosGame(Widget):
    pass


class CosApp(App):
    def build(self):
        return CosGame()

    def init():
        # Logging stuff
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler('info.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -\
                                    %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # End logging stuff

        seed.initSeed()
        generateTown()

        #input('Press enter to close this window.')

if __name__ == '__main__':
    CosApp().run()
