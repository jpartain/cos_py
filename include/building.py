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
            char = 'R'
        elif typ == 'PoorHouse':
            char = 'P'
        elif typ == 'MiddleHouse':
            char = 'M'
        elif typ == 'NobleHouse':
            char = 'N'
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
            char = '*'
        return char

    def __repr__(self):
        typ = self.building_type
        if typ == 'Road':
            char = 'R'
        elif typ == 'PoorHouse':
            char = 'P'
        elif typ == 'MiddleHouse':
            char = 'M'
        elif typ == 'NobleHouse':
            char = 'N'
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
            char = '*'
        return char
