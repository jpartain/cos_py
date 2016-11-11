import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput

import town
import seed


global towns
global current_town_map

towns = []
current_town_map = 0

class MainMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)

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

    def goToMapScreen(self):
        self.manager.current = 'map'


class MapScreen(Screen):

    map_box = StringProperty('')
    map_nums = ListProperty([])

    def __init__(self, **kwargs):
        self.generateTown()
        super(MapScreen, self).__init__(**kwargs)

    def generateTown(self):
        self.map_box = 'Generating new town..'

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

        towns.append(new_town)
        self.map_nums.append(str(towns.index(new_town)))
        self.map_box = 'Generating new town.. done.'

    def goToMainMenu(self):
        self.manager.current = 'main_menu'

    def showMap(self, instance, value):
        current_town_map = value
        self.map_box = towns[int(value)].printMapCorners()


class ArrowsEnterInput(TextInput):

    name_out = StringProperty('')

    def insert_text(self, substring, from_undo=False):
        if substring == '\n':
            self.getPeopleAtCursor()

        s = ''

        return super(ArrowsEnterInput, self).insert_text(s, from_undo=from_undo)

    def getPeopleAtCursor(self):
        pos = self.cursor

        try:
            people = towns[current_town_map].map_points[pos[1]][pos[0]].people
            self.name_out = '[b][u]{}\'s[/u][/b]\n'.format(people[0].family_name)
            for dude in people:
                self.name_out = self.name_out + dude.__str__()

        except IndexError:
            # probably an empty map spot
            pass


class CosApp(App):

    def build(self):
        Config.set( 'graphics', 'width', '800' )
        Config.set( 'graphics', 'height', '360' )

        screens = ScreenManager()
        screens.add_widget(MainMenuScreen(name='main_menu'))
        screens.add_widget(MapScreen(name='map'))
        screens.current = 'main_menu'

        return screens


if __name__ == '__main__':
    CosApp().run()
