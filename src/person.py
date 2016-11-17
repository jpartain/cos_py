import logging
import random

logger = logging.getLogger(__name__)


Age = ['Baby',
       'Child',
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
         'Doctor',
         'Nurse',
         'Weaver',
         'Bartender',
         'Worker',
         'Janitor',
         'Trader',
         'Seller',
         'Manager',
         'Foreman']

with open('assets/names/last', 'r') as f:
    l_names = f.read().splitlines()
with open('assets/names/female', 'r') as f:
    f_names = f.read().splitlines()
with open('assets/names/male', 'r') as f:
    m_names = f.read().splitlines()

l_names_len = len(l_names)
f_names_len = len(f_names)
m_names_len = len(m_names)

def createFamilyName():
    name_idx = random.randint(0, l_names_len - 1)
    return l_names[name_idx]

class Person:
    def __init__(self):
        self.age = ''
        self.approval = 0
        self.consensus = 0
        self.employed = False
        self.fame = 0
        self.family_name = ''
        self.fulfillment = 0
        self.gender = ''
        self.house = None
        self.integrity = 0
        self.inventory = []
        self.job_title = ''
        self.name = ''
        self.opinion_of_others = {}
        self.relation_persons = []
        self.relation_persons_in_house = []
        self.relations = []
        self.relations_in_house = []
        self.toughness = 0
        self.wealth = 0
        self.workplace = None

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
        return Age[int((high - low) * random.randint(0, 9) / 9 + low)]

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

        name_idx = random.randint(0, length - 1)
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
        relation_string = ''
        for dude, relation in zip(self.relation_persons_in_house,
                                  self.relations_in_house):
            relation_string = (relation_string + '        ' + dude.name + ' - ' +
                               relation + '\n')

        return '    {0} - {1}\n{2}'.format(self.name, self.age, relation_string)

    def __repr__(self):
        return '{0} {1}'.format(self.name, self.family_name)


class Relation:
    def __init__(self, name, relationship):
        self.name = name
        self.relation = relationship
