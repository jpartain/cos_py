import logging

logger = logging.getLogger(__name__)

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
        self.people = []

    def generateSize(self, string):
        pass

    def generateType(self, string):
        pass

    def generateOccupants(self, string):
        pass

    '''
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
            char = '\033[96mT'
        elif typ == 'PublicPlumbing':
            char = '\033[96mB'
        elif typ == 'Market':
            char = '\033[96mK'
        elif typ == 'TradePost':
            char = '\033[96mD'
        elif typ == 'Inn':
            char = '\033[96mI'
        elif typ == 'Barn':
            char = '\033[97mA'
        elif typ == 'Barracks':
            char = '\033[97mX'
        elif typ == 'Mason':
            char = '\033[97mS'
        elif typ == 'Blacksmith':
            char = '\033[97mL'
        elif typ == 'Lumbermill':
            char = '\033[97mE'
        elif typ == 'Cathedral':
            char = '\033[97m+'
        elif typ == 'Weavery':
            char = '\033[97mY'
        elif typ == 'Colosseum':
            char = '\033[97mO'
        else:
            char = '\033[92m*'
        return char
    '''
    def __str__(self):
        typ = self.building_type
        if typ == 'Road':
            char = '[color=eeb09c]R[/color]'
        elif typ == 'PoorHouse':
            char = '[color=317873]P[/color]'
        elif typ == 'MiddleHouse':
            char = '[color=5f9ea0]M[/color]'
        elif typ == 'NobleHouse':
            char = '[color=a0d6b4]N[/color]'
        elif typ == 'Tavern':
            char = '[color=275749]T[/color]'
        elif typ == 'PublicPlumbing':
            char = '[color=275749]B[/color]'
        elif typ == 'Market':
            char = '[color=275749]K[/color]'
        elif typ == 'TradePost':
            char = '[color=275749]D[/color]'
        elif typ == 'Inn':
            char = '[color=275749]I[/color]'
        elif typ == 'Barn':
            char = '[color=275749]A[/color]'
        elif typ == 'Barracks':
            char = '[color=275749]X[/color]'
        elif typ == 'Mason':
            char = '[color=275749]S[/color]'
        elif typ == 'Blacksmith':
            char = '[color=275749]L[/color]'
        elif typ == 'Lumbermill':
            char = '[color=275749]E[/color]'
        elif typ == 'Cathedral':
            char = '[color=275749]+[/color]'
        elif typ == 'Weavery':
            char = '[color=275749]Y[/color]'
        elif typ == 'Colosseum':
            char = '[color=275749]O[/color]'
        else:
            char = '[color=a3c1ad]*[/color]'
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
            char = '\033[96mT'
        elif typ == 'PublicPlumbing':
            char = '\033[96mB'
        elif typ == 'Market':
            char = '\033[96mK'
        elif typ == 'TradePost':
            char = '\033[96mD'
        elif typ == 'Inn':
            char = '\033[96mI'
        elif typ == 'Barn':
            char = '\033[97mA'
        elif typ == 'Barracks':
            char = '\033[97mX'
        elif typ == 'Mason':
            char = '\033[97mS'
        elif typ == 'Blacksmith':
            char = '\033[97mL'
        elif typ == 'Lumbermill':
            char = '\033[97mE'
        elif typ == 'Cathedral':
            char = '\033[97m+'
        elif typ == 'Weavery':
            char = '\033[97mY'
        elif typ == 'Colosseum':
            char = '\033[97mO'
        else:
            char = '\033[92m*'
        return char
