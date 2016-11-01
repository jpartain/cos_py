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
       'Old']

Gender = ['Female',
          'Male']

Relations = ['Wife',
             'Husband',
             'Daughter',
             'Son',
             'Granddaughter',
             'Grandson',
             'Niece',
             'Nephew',
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

M_Match_Relations = ['Husband',
                     'Husband',
                     'Father',
                     'Father',
                     'Grandfather',
                     'Grandfather',
                     'Uncle',
                     'Uncle',
                     'Son',
                     'Son',
                     'Brother',
                     'Brother',
                     'Nephew',
                     'Nephew',
                     'Grandson',
                     'Grandson',
                     'Cousin',
                     'Mister',
                     'Mister',
                     'Father',
                     'Father']

F_Match_Relations = ['Wife',
                     'Wife',
                     'Mother',
                     'Mother',
                     'Grandmother',
                     'Grandmother',
                     'Aunt',
                     'Aunt',
                     'Daughter',
                     'Daughter',
                     'Sister',
                     'Sister',
                     'Niece',
                     'Niece',
                     'Granddaughter',
                     'Granddaughter',
                     'Cousin',
                     'Mistress',
                     'Mistress',
                     'Mother',
                     'Mother']

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

def createFamilyName():
    with open('names/last', 'r') as f:
        names_length = len(f.readlines())

    name_idx = int((seed.getRand() * seed.getRand() * seed.getRand() *
                    seed.getRand() * seed.getRand() * seed.getRand()) /
                    531441 * names_length)

    name = linecache.getline('names/last', name_idx)
    linecache.clearcache()

    return name


class Person:
    def __init__(self):
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

    def alreadyHasRelation(self, person, match):
        for relation in person.relations:
            if relation.name == match.name:
                return True
            else:
                continue

        else:
            return False

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

    def setAge(self, low, high):
        return Age[int((high - low) * seed.getRand() / 9 + low)]

    def setName(self):
        if self.gender == 'Female':
            name_file = 'names/female'
        elif self.gender == 'Male':
            name_file = 'names/male'
        else:
            name_file = 'names/female'
            logger.warning('Set name gender to female because Person.gender not set.')

        with open(name_file, 'r') as f:
            names_length = len(f.readlines())

        name_idx = int((seed.getRand() * seed.getRand() * seed.getRand() *
                        seed.getRand()) / 6561 * names_length)

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


class Relation:
    def __init__(self, name, relationship):
        self.name = name
        self.relation = relationship
