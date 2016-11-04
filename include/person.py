import logging
import include.seed as seed

logger = logging.getLogger(__name__)


Age = ['Baby',
       'Child',
       'Teenager'
       'YoungAdult',
       'Adult',
       'Old']

Gender = ['Female',
          'Male']

Relations = ['Spouse',
             'Child',
             'Grandchild',
             'SiblingChild',
             'Parent',
             'Sibling',
             'ParentSibling',
             'Grandparent',
             'Cousin',
             'SideJob',
             'B_Child']

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

with open('names/last', 'r') as f:
    l_names = f.read().splitlines()
with open('names/female', 'r') as f:
    f_names = f.read().splitlines()
with open('names/male', 'r') as f:
    m_names = f.read().splitlines()

l_names_len = len(l_names)
f_names_len = len(f_names)
m_names_len = len(m_names)

def createFamilyName():
    num1 = seed.getRand() + 1
    num2 = seed.getRand() + 1
    num3 = seed.getRand() + 1
    num4 = seed.getRand() + 1
    num5 = seed.getRand() + 1
    num6 = seed.getRand() + 1

    name_idx = int(num1 * num2 * num3 * num4 * num5 * num6 /
                    1000000 * (l_names_len - 1))

    return l_names[name_idx]

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
        self.opinion_of_others = []
        self.job_title = ''
        self.inventory = []
        self.family_name = ''
        self.name = ''
        self.relation_persons = []
        self.relations = []

    def addRelation(self, person, relation):
        self.relation_persons.append(person)
        self.relations.append(relation)

    def alreadyHasRelation(self, person):
        for relation in self.relation_persons:
            if relation == person:
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
            name_file = f_names
            length = f_names_len
        elif self.gender == 'Male':
            name_file = m_names
            length = m_names_len
        else:
            name_file = f_names
            length = f_names_len
            logger.warning('Set name gender to female because Person.gender not set.')

        num1 = seed.getRand() + 1
        num2 = seed.getRand() + 1
        num3 = seed.getRand() + 1
        num4 = seed.getRand() + 1

        name_idx = int((num1 * num2 * num3 * num4) / 10000 * (length - 1))

        self.name = name_file[name_idx]

    def setOpinion(self, person, opinion):
        # self.opinion_of_others.person = opinion
        pass

    def takeItem(self, item):
        # self.inventory.decrease/delete(item
        pass

    def updateConsensus(self):
        pass

    def __str__(self):
        return '{0} {1}'.format(self.name, self.family_name)

    def __repr__(self):
        return '{0} {1}'.format(self.name, self.family_name)


class Relation:
    def __init__(self, name, relationship):
        self.name = name
        self.relation = relationship
