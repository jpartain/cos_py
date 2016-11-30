from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.uix.screenmanager import FallOutTransition, RiseInTransition
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory

import kivent_core
import kivent_cymunk
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.gamesystem import GameSystem
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.gameworld import GameWorld

from cymunk import Body
from cymunk import PivotJoint

from math import radians

import town


global current_town_map
global towns

current_town_map = 0
towns = []
texture_manager.load_atlas('./assets/fonts/cogmind_font.atlas')
texture_manager.load_image('./assets/pngs/BLCRoad.png')
texture_manager.load_image('./assets/pngs/BRCRoad.png')
texture_manager.load_image('./assets/pngs/DIRoad.png')
texture_manager.load_image('./assets/pngs/HRoad.png')
texture_manager.load_image('./assets/pngs/IRoad.png')
texture_manager.load_image('./assets/pngs/LIRoad.png')
texture_manager.load_image('./assets/pngs/RIRoad.png')
texture_manager.load_image('./assets/pngs/TLCRoad.png')
texture_manager.load_image('./assets/pngs/TRCRoad.png')
texture_manager.load_image('./assets/pngs/UIRoad.png')
texture_manager.load_image('./assets/pngs/VRoad.png')
texture_manager.load_image('./assets/pngs/empty.png')


class CosGame(Widget):

    player_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(CosGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics', 'rotate_renderer',
                                       'position', 'rotate', 'camera'],
                                      callback = self.initGame)

    def initGame(self):
        global player_id

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)

        self.setupStates()
        self.setState()
        self.loadModels()
        self.drawPlayMap()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        player_control_keys = 'l h j k y u b n'.split()

        if keycode[1] == 'escape':
            if self.gameworld.state == 'cos_game':
                self.goToMainMenuScreen()

            elif self.gameworld.state == 'main_menu':
                self.goToCosScreen()

            elif self.gameworld.state == 'map_generation':
                self.goToMainMenuScreen()

            else:
                pass

        elif keycode[1] in player_control_keys:
            player = self.gameworld.entities[self.player_id]
            apply_impulse = player.cymunk_physics.body.apply_impulse

            if keycode[1] == 'l':
                r = (1, 0)
                apply_impulse(s, r)
                print(player.cymunk_physics.body.velocity)

            elif keycode[1] == 'h':
                pass

            elif keycode[1] == 'j':
                pass

            elif keycode[1] == 'k':
                pass

            elif keycode[1] == 'y':
                pass

            elif keycode[1] == 'u':
                pass

            elif keycode[1] == 'b':
                pass

            elif keycode[1] == 'n':
                pass

            else:
                pass

        else:
            pass

    def loadModels(self):
        model_string = ('! dq # $ % & sq ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 ' +
                        ': ; < = > ? @ [ fs ] ^ _ \' { | } A B C D E F G H I ' +
                        'J K L M N O P Q R S T U V W X Y Z esq sq a b c d e ' +
                        'f g h i j k l m n o p q r s t u v w x y z vertl ' +
                        'horizl crossl lcrossl ucrossl rcrossl dcrossl ' +
                        'trcornerl brcornerl blcornerl tlcornerl square')
        road_string = ('BLCRoad BRCRoad DIRoad HRoad IRoad LIRoad RIRoad ' +
                       'TLCRoad TRCRoad UIRoad VRoad empty')

        models = model_string.split()
        roads = road_string.split()
        model_manager = self.gameworld.model_manager

        for model in models:
            model_manager.load_textured_rectangle('vertex_format_4f', 12., 12.,
                                                  model, model)

        for model in roads:
            model_manager.load_textured_rectangle('vertex_format_4f', 144., 144.,
                                                model, model)

    def setupStates(self):
        self.gameworld.add_state(state_name='main_menu',
                                 systems_added=['rotate_renderer'],
                                 systems_removed=['camera'],
                                 systems_paused=['position', 'camera'],
                                 systems_unpaused=['rotate_renderer'],
                                 screenmanager_screen='main_menu_screen')

        self.gameworld.add_state(state_name='map_generation', systems_added=[],
                                 systems_removed=['rotate_renderer', 'position',
                                                  'camera'],
                                 systems_paused=['rotate_renderer', 'position',
                                                 'camera'],
                                 systems_unpaused=[],
                                 screenmanager_screen='map_screen')

        self.gameworld.add_state(state_name='cos_game',
                                 systems_added=['rotate_renderer', 'position',
                                                'camera'],
                                 systems_removed=[], systems_paused=[],
                                 systems_unpaused=['rotate_renderer', 'position',
                                                   'camera'],
                                 screenmanager_screen='cos_screen')

    def setState(self):
        self.gameworld.state = 'main_menu'

    def drawPlayMap(self):
        gameview = self.gameworld.system_manager['camera']
        x, y = int(-gameview.camera_pos[0]), int(-gameview.camera_pos[1])
        w, h = int(gameview.size[0] + x), int(gameview.size[1] + y)

        town = towns[current_town_map]
        for y, row in enumerate(town.map_points):
            for x, cell in enumerate(row):
                pos = (x * 144 + 72, y * 144 + 72)
                building_type = cell.building_type

                ent_id = self.createMapArea(pos, building_type)

        # Player
        self.player_id = self.createPlayer()
        player = self.gameworld.entities[self.player_id]

        # Touch object player will walk to
        self.walking_to = Body('INF', 'INF')
        start_pos = (player.position.pos[0], player.position.pos[1])
        self.walking_to.position = start_pos

        # Joint that pulls the two together
        joint = PivotJoint(self.walking_to, player.cymunk_physics.body, (0, 0), (0, 0))
        joint.max_force = 200.
        joint.max_bias = 5000.
        self.ids.physics.space.add_constraint(joint)

    def createMapArea(self, pos, building):
        if 'Road' not in building:
            building = 'empty'

        component_dict = {'position': pos,
                          'rotate_renderer': {'texture': building,
                                              'size': (144, 144),
                                              'model_key': building,
                                              'render': True},
                          'rotate': 0}

        component_order = ['position','rotate', 'rotate_renderer']

        return self.gameworld.init_entity(component_dict, component_order)

    def createPlayer(self):
        shape_dict = {'inner_radius': 0, 'outer_radius': 8,
                      'mass': 2, 'offset': (0, 0)}
        col_shape = {'shape_type': 'circle', 'elasticity': .1,
                     'collision_type': 1, 'shape_info': shape_dict,
                     'friction': 1.0}
        col_shapes = [col_shape]
        physics_component = {'main_shape': 'circle',
                             'velocity': (0, 0),
                             'position': (72, 72), 'angle': 0,
                             'angular_velocity': 0,
                             'vel_limit': 50,
                             'ang_vel_limit': radians(200),
                             'mass': 2, 'col_shapes': col_shapes}
        component_dict = {'position': (72, 72),
                          'rotate_renderer': {'texture': '@',
                                              'size': (12, 12),
                                              'model_key': '@',
                                              'render': True},
                          'cymunk_physics': physics_component,
                          'rotate': 0}

        component_order = ['position', 'rotate', 'rotate_renderer',
                           'cymunk_physics']

        return self.gameworld.init_entity(component_dict, component_order)

    def goToMainMenuScreen(self):
        gw = self.gameworld

        if gw.state == 'map_generation':
            gw.gamescreenmanager.transition = SlideTransition()
            gw.gamescreenmanager.transition.direction = 'right'
        else:
            gw.gamescreenmanager.transition = RiseInTransition()

        gw.state = 'main_menu'

    def goToMapScreen(self):
        self.gameworld.gamescreenmanager.transition = SlideTransition()
        self.gameworld.gamescreenmanager.transition.direction = 'left'
        self.gameworld.state = 'map_generation'

    def goToCosScreen(self):
        self.gameworld.gamescreenmanager.transition = FallOutTransition()
        self.gameworld.state = 'cos_game'

    def on_touch_down(self, touch):
        state = self.gameworld.state

        if state == 'cos_game':
            b = self.walking_to
            b.position = touch.pos

            bodies = self.ids.physics.space.bodies
            if b not in bodies:
                self.ids.physics.space.add_body(b)

        else:
            super(CosGame, self).on_touch_down(touch)


class MainMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)


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

    def labelPress(self, instance, value):
        global current_town_map

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
                                    '    {0} {1} - {2}\n'.format(dude.name,
                                                                 dude.family_name,
                                                                 dude.job_title)
                # print(dude.name, dude.job_title)
        else:
            self.names_box = self.names_box + '    None'

    def showMap(self, instance, value):
        global current_town_map

        for i, place in enumerate(towns):
            if place.name == value:
                current_town_map = i

        self.map_box = towns[current_town_map].printMapCorners()


class CosScreen(Screen):

    def __init__(self, **kwargs):
        super(CosScreen, self).__init__(**kwargs)


class CosApp(App):

    def build(self):
        Config.set('kivy', 'exit_on_escape', '0')
        Config.set( 'graphics', 'width', '900' )
        Config.set( 'graphics', 'height', '360' )

        self.game = CosGame()

        return self.game


if __name__ == '__main__':
    CosApp().run()
