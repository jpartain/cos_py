TownEconomy = ['Farm',
               'Mine',
               'Military',
               'Quarry',
               'Metalworks',
               'Lumber',
               'Church',
               'Textile',
               'Tavern',
               'Colosseum']

""" Town has the following attributes:
        wealth:     an integer from -5 to 4, indicating debt/wealth level
        economy:    a string chosen from a set of presets which determines special
                    buildings and employment oppotunities in town
        danger:     an integer from 0 to 9 indicating threat level
        nobility:   an integer from 0 to 9 indicating ratio of noble to poor (9 being 90% noble)
        settled:   an integer from 1 to 10 indicating ratio of housed to homeless,
                    also dependent on wealth
"""
class Town:
    def __init__(self, seed):
        self.generateWealth(seed[0])
        self.generateEconomy(seed[1])
        self.generateDanger(seed[2])
        self.generateNobility(seed[3])
        self.generateHomeless(seed[4])
        self.generateMap(seed[23:63])

    def generateWealth(self, string):
        self.wealth = int(string) - 5
        
    def generateEconomy(self, string):
        self.economy = TownEconomy[int(string)]
        
    def generateDanger(self, string):
        if self.economy == 'Military':
            self.danger_mod = 0.4
        elif self.economy == 'Church':
            self.danger_mod = 0.6
        elif self.economy == 'Colosseum':
            self.danger_mod = 0.6
        else:
            self.danger_mod = 1

        self.danger = int(self.danger_mod*int(string))
        
    def generateNobility(self, string):
        if self.economy == 'Church':
            self.nobility_mod = 0.5
        elif self.economy == 'Military':
            self.nobility_mod = 0.4
        else:
            self.nobility_mod = 0.35
            
        self.nobility = int(10*self.nobility_mod*int(string))
        
    def generateHomeless(self, string):
        self.settled_ratio = int(10*(int(string)/5 + self.getWealth() + 5))

    def generateMap(self, string):
        pass
        
    def generateMap(self, string):
        pass

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

    def getSettledRatio(self):
        return self.settled_ratio

    def buildMap(self, string):
        # generate size
        # generate building types for each square
        pass

    def createPerson(self, string):
        pass

    def generatePopulation(self, string):
        pass

    def linkRelationships(self, string):
        pass

    def createOpinions(self, string):
        pass
