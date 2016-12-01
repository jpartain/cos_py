from kivy.factory import Factory

from kivent_core.systems.gamesystem import GameSystem


class CharacterSystem(GameSystem):
    pass

Factory.register('CharacterSystem', cls=CharacterSystem)
