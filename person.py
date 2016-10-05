from enum import Enum

Age = Enum('Age',
           'Baby
            Child
            Teenager
            YoungAdult
            Adult
            MiddleAge
            Old')

Gender = Enum('Gender',
              'Female
               Male')

Relationship = Enum('Relationship',
                    'Wife
                     Husband
                     Daughter
                     Son
                     Father
                     Mother
                     Sister
                     Brother
                     Aunt
                     Uncle
                     Grandmother
                     Grandfather
                     Cousin
                     Mistress
                     Mister
                     B_Son
                     B_Daughter')

Title = Enum('Title',
             'King
              Queen
              Prince
              Princess
              Servant
              Priest
              Acolyte
              Knight
              Squire
              Soldier
              Farmer
              RockMason
              Smithy
              Lumberjack
              Weaver
              Bartender
              Waiter
              Waitress
              Janitor
              Trader
              Seller
              Manager
              Foreman')

class Person(self):
    def __init__(self, happiness, hunger, approval, fulfillment, fame, consensus, 
                       age, honesty, toughness, gender, relations, opinion_of_others,
                       job_title, inventory):
        self.happiness = happiness
        self.hunger = hunger
        self.approval = approval
        self.fulfillment = fulfillment
        self.fame = fame
        self.consensus = consensus
        self.age = age
        self.honesty = honesty
        self.toughness = toughness
        self.gender = gender
        self.relations = relations
        self.opinion_of_others = opinion_of_others
        self.job_title = job_title
        self.inventory = inventory
        
    def setHappiness(self, happiness):
        self.happiness = happiness

    def setHunger(self, hunger):
        self.hunger = hunger

    def setApproval(self, approval):
        self.approval = approval

    def setFulfillment(self, fulfillment):
        self.fulfillment = fulfillment

    def setFame(self, fame):
        self.fame = fame

    def setConsensus(self, consensus):
        self.consensus = consensus

    def setAge(self, age):
        self.age = age

    def setHonesty(self, honesty):
        self.honesty = honesty

    def setToughness(self, toughness):
        self.toughness = toughness

    def setGender(self, gender):
        self.gender = gender

    def addRelation(self, relationship, person):
        # self.relations.append(relationship, person) tuple probably
        pass

    def removeRelation(self, person):
        # self.relations.delete(person)
        pass

    def setOpinion(self, person, opinion):
        # self.opinion_of_others.person = opinion

    def setTitle(self, title):
        self.title = title

    def putItem(self, item):
        # self.inventory.append(item)
        pass

    def takeItem(self, item):
        # self.inventory.decrease/delete(item
        pass

    def getHappiness(self):
        return self.happiness

    def getHunger(self):
        return self.hunger

    def getApproval(self):
        return self.approval

    def getFulfillment(self):
        return self.fulfillment

    def getFame(self):
        return self.fame

    def getConsensus(self):
        return self.consensus

    def getAge(self):
        return self.age

    def getHonesty(self):
        return self.honesty

    def getToughness(self):
        return self.toughness

    def getRelations(self):
        return self.relations

    def getOpinion(self, person):
        return self.opinion_of_others.person

    def getTitle(self):
        return self.title

    def getInventory(self):
        return self.inventory
