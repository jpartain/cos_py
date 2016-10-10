from enum import Enum

BuildingType = Enum('BuildingType', 
                    'PoorHouse'
                    'MiddleHouse'
                    'NobleHouse'
                    'Barn'
                    'Windmill'
                    'Barracks'
                    'Mason'
                    'Blacksmith'
                    'Lumbermill'
                    'Cathedral'
                    'Weavery'
                    'Tavern'
                    'Colosseum'
                    'PublicPlumbing'
                    'Market'
                    'TradePost')

class Building:
    def __init__(self, seed):
        self.generateSize(seed[0])
        self.generateType(seed[1:3])
        self.generateOccupants(seed[3:20])
        self.health = 100

    def generateSize(self, string):
        pass

    def generateType(self, string):
        pass

    def generateOccupants(self, string):
        pass

    def setSize(self, size):
        self.size = size

    def setType(self, building_type):
        self.type = building_type

    def setOccupants(self, occupants):
        self.occupants = occupants

    def setHealth(self, health):
        self.health = health
        
    def setMenu(self, menu):
        self.menu = menu

    def getSize(self):
        return self.size

    def getType(self):
        return self.type

    def getOccupants(self):
        return self.occupants

    def getHealth(self):
        return self.health
        
    def getMenu(self):
        return self.menu
