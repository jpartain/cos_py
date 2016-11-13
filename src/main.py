import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import town
import seed


global current_town_map
global towns

current_town_map = 0
towns = []

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

    def goToMapScreen(self):
        self.manager.current = 'map'


class MapScreen(Screen):

    map_box = StringProperty('')
    map_nums = ListProperty([])
    names_box = StringProperty('')

    def __init__(self, **kwargs):
        self.generateTown()
        super(MapScreen, self).__init__(**kwargs)

    def createNewTown(self, dt):
        new_town = town.Town()
        towns.append(new_town)
        self.map_nums.append(new_town.name)
        self.map_box = 'Generating new town.. done.'

    def generateTown(self):
        self.map_box = 'Generating new town..'

        Clock.schedule_once(self.createNewTown)

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

    def goToMainMenu(self):
        self.manager.current = 'main_menu'

    def labelPress(self, instance, value):
        pos_x = int(value.split()[0])
        pos_y = int(value.split()[1])

        place = towns[current_town_map].map_points[pos_y][pos_x]
        b_type = place.building_type
        self.names_box = '[b]{0}[/b]\n\n'.format(b_type)

        if len(place.people) != 0:
            people = place.people
            self.names_box = self.names_box + \
                                '[b][u]Family - {}[/u][/b]\n'.format(people[0].family_name)
            for dude in people:
                self.names_box = self.names_box + dude.__str__()

            self.names_box = self.names_box + '\n'

        else:
            self.names_box = self.names_box + '[b][u]Family - None[/u][/b]\n\n'

        emp_str = '[b][u]Employees[/u][/b]\n'
        self.names_box = self.names_box + emp_str
        if len(place.employees) != 0:
            employees = place.employees
            for dude in employees:
                self.names_box = self.names_box + \
                                    '    {0} {1}\n'.format(dude.name, dude.family_name)
        else:
            self.names_box = self.names_box + '    None'

    def showMap(self, instance, value):
        current_town_map = value
        for i, place in enumerate(towns):
            if place.name == value:
                current_town_map = i

        self.map_box = towns[current_town_map].printMapCorners()


class CosApp(App):

    def build(self):
        Config.set( 'graphics', 'width', '900' )
        Config.set( 'graphics', 'height', '360' )

        screens = ScreenManager()
        screens.add_widget(MainMenuScreen(name='main_menu'))
        screens.add_widget(MapScreen(name='map'))
        screens.current = 'main_menu'

        return screens


if __name__ == '__main__':
    CosApp().run()
