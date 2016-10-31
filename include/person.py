import linecache
import logging
import include.seed as seed

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'person.log', level = logging.DEBUG)


Age = ['Baby',
       'Child',
       'Teenager'
       'YoungAdult',
       'Adult',
       'MiddleAge',
       'Old']

Gender = ['Female',
          'Male']

Relationship = ['Wife',
                'Husband',
                'Daughter',
                'Son',
                'Father',
                'Mother',
                'Sister'
                'Brother',
                'Aunt',
                'Uncle',
                'Grandmother',
                'Grandfather',
                'Cousin',
                'Mistress',
                'Mister',
                'B_Son',
                'B_Daughter']

Title = ['Mayor'
         'Official',
         'Prince',
         'Princess',
         'Servant',
         'Priest',
         'Acolyte',
         'Knight',
         'Squire',
         'Soldier',
         'Farmer',
         'RockMason'
         'Smithy',
         'Lumberjack',
         'Weaver',
         'Bartender',
         'Waiter',
         'Waitress',
         'Janitor',
         'Trader',
         'Seller',
         'Manager',
         'Foreman']

def createFamilyName(self):
    name_idx = int((seed.getRand() * seed.getRand() * seed.getRand() *
                    seed.getRand() * seed.getRand() * seed.getRand()) /
                    531441 * len(names))

    name = linecache.getline('names/last', name_idx)
    linecache.clearcache()

    return name


class Person:
    def __init__(self, wealth, approval, fulfillment, fame, consensus,
                       age, integrity, toughness, gender, relations, opinion_of_others,
                       job_title, inventory):
        self.wealth = 0
        self.approval = 0
        self.fulfillment = 0
        self.fame = 0
        self.consensus = 0
        self.age = ''
        self.integrity = 0
        self.toughness = 0
        self.gender = ''
        self.relations = []
        self.opinion_of_others = []
        self.job_title = ''
        self.inventory = []
        self.family_name = ''
        self.name = ''

    def addRelation(self, relationship, person):
        # self.relations.append(relationship, person) tuple probably
        pass

    def getFame(self):
        pass

    def getInventory(self):
        pass

    def getOpinion(self, person):
        return self.opinion_of_others.person

    def putItem(self, item):
        # self.inventory.append(item)
        pass

    def removeRelation(self, person):
        # self.relations.delete(person)
        pass

    def setName(self):
        if self.gender == 'Female':
            name_file = 'names/female'
        elif self.gender == 'Male':
            name_file = 'names/male'
        else:
            name_file = 'names/female'
            logger.warning('Set name gender to female because Person.gender not set.')

        name_idx = int((seed.getRand() * seed.getRand() * seed.getRand() *
                        seed.getRand()) / 6561 * len(names))

        self.name = linecache.getline(name_file, name_idx)
        linecache.clearcache()

    def setOpinion(self, person, opinion):
        # self.opinion_of_others.person = opinion
        pass

    def takeItem(self, item):
        # self.inventory.decrease/delete(item
        pass

    def updateConsensus(self):
        pass

