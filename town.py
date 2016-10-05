from enum import Enum

TownEconomy = Enum('TownEconomy',
                   'Farm
                    Mine
                    Military
                    Quarry
                    Metalworks
                    Lumber
                    Church
                    Textile
                    Tavern
                    Colosseum')

class Town(self):
    def __init__(self, wealth, economy, danger, nobility, town_map, homeless):
        self.wealth = wealth
        self.economy = economy
        self.danger = danger
        self.nobility = nobility
        self.map = town_map
        self.homeless = homeless

    def setWealth(self, wealth):
        self.wealth = wealth
        
    def setEconomy(self, economy):
        self.economy = economy
        
    def setDanger(self, danger):
        self.danger = danger
        
    def setNobility(self, nobility):
        self.nobility = nobility
        
    def setMap(self, town_map):
        self.map = town_map
        
    def addHomeless(self, person):
        self.homeless.append(person)

    def removeHomeless(self, person):
        self.homeless.delete(person)

    def getWealth(self):
        return self.wealth
        
    def getEconomy(self):
        return self.economy
        
    def getDanger(self):
        return self.danger
        
    def getNobility(self):
        return self.nobility
        
    def getMap(self):
        return self.map

    def getHomeless(self):
        return self.homeless

    def buildMap(self, random_string):
        # generate size
        # generate building types for each square
        pass

    def createPerson(self, random_string):
        pass

    def generatePopulation(self, random_string):
        pass

    def linkRelationships(self, random_string):
        pass

    def createOpinions(self, random_string):
        pass
