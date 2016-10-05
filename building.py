from enum import Enum

BuildingType = Enum('BuildingType', 
                    'PoorHouse
                     MiddleHouse
                     NobleHouse
                     Barn
                     Windmill
                     Barracks
                     Mason
                     Blacksmith
                     Lumbermill
                     Cathedral
                     Weavery
                     Tavern
                     Colosseum
                     PublicPlumbing
                     Market
                     TradePost')

class Building(self):
    def __init__(self, size, building_type, occupants, health, menu):
        self.size = size
        self.type = building_type
        self.occupants = occupants
        self.health = health
        self.menu = menu

    def setType(self, building_type):
        self.type = building_type

    def setOccupants(self, occupants):
        self.occupants = occupants

    def setHealth(self, health):
        self.health = health
        
    def setMenu(self, menu):
        self.menu = menu

    def getType(self):
        return self.type

    def getOccupants(self):
        return self.occupants

    def getHealth(self):
        return self.health
        
    def getMenu(self):
        return self.menu
