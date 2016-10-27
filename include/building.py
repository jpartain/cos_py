CommonBuildings = ['Road',
                   'PoorHouse',
                   'MiddleHouse',
                   'NobleHouse',
                   'Tavern',
                   'PublicPlumbing',
                   'Market',
                   'TradePost',
                   'Inn']

SpecialBuildings = ['Barn',
                    'Butcher',
                    'Mason',
                    'Blacksmith',
                    'Weavery',
                    'Barracks',
                    'Lumbermill',
                    'Cathedral',
                    'Colosseum']


class Building:
    def __init__(self, building_type):
        # self.generateSize(seed[0])
        # self.generateOccupants(seed[3:20])
        self.building_type = building_type
        self.health = 100

    def generateSize(self, string):
        pass

    def generateType(self, string):
        pass

    def generateOccupants(self, string):
        pass

    def __str__(self):
        typ = self.building_type
        if typ == 'Road':
            char = '\033[91mR'
        elif typ == 'PoorHouse':
            char = '\033[90mP'
        elif typ == 'MiddleHouse':
            char = '\033[94mM'
        elif typ == 'NobleHouse':
            char = '\033[95mN'
        elif typ == 'Tavern':
            char = 'T'
        elif typ == 'PublicPlumbing':
            char = 'B'
        elif typ == 'Market':
            char = 'K'
        elif typ == 'TradePost':
            char = 'D'
        elif typ == 'Inn':
            char = 'I'
        else:
            char = '\033[92m*'
        return char

    def __repr__(self):
        typ = self.building_type
        if typ == 'Road':
            char = '\033[91mR'
        elif typ == 'PoorHouse':
            char = '\033[90mP'
        elif typ == 'MiddleHouse':
            char = '\033[94mM'
        elif typ == 'NobleHouse':
            char = '\033[95mN'
        elif typ == 'Tavern':
            char = 'T'
        elif typ == 'PublicPlumbing':
            char = 'B'
        elif typ == 'Market':
            char = 'K'
        elif typ == 'TradePost':
            char = 'D'
        elif typ == 'Inn':
            char = 'I'
        else:
            char = '\033[92m*'
        return char
