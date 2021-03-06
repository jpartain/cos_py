import random
from more_itertools import unique_everseen

from building import *
from block import Block
from block import Point
import person


TownEconomy = ['Farm',
               'Mine',
               'Military',
               'Quarry',
               'Metalworks',
               'Lumber',
               'Church',
               'Textile',
               'Colosseum']

with open('assets/names/town', 'r') as f:
    t_names = f.read().splitlines()

t_names_len = len(t_names)

global placement_radius

def createPointPlacementRadius():
    global placement_radius
    radius = []

    for r in range(0, 101):
        x = r
        y = 0
        err = 0

        while x >= y:
            radius.append(Point(x, y))
            radius.append(Point(y, x))
            radius.append(Point(-y, x))
            radius.append(Point(-x, y))
            radius.append(Point(-x, -y))
            radius.append(Point(-y, -x))
            radius.append(Point(y, -x))
            radius.append(Point(x, -y))

            y = y + 1
            err = err + 1 + 2*y
            if (2*(err - x) + 1) > 0:
                x = x - 1
                err = err + 1 - 2*x

    placement_radius = list(unique_everseen(radius))
    #seen = list()
    #seen_add = seen.append
    #self.placement_radius = [x for x in radius if not (x in seen or seen_add(x))]

createPointPlacementRadius()


class Town:
    def __init__(self):
        self.mayor = None
        self.officials = []

        self.population = 0
        self.workable = 0
        # self.createPointPlacementRadius()

        self.assignName()
        self.generateWealth()
        self.generateEconomy()
        self.generateDanger()
        self.generateNobility()
        self.generateHomeless()

        self.buildMap()
        self.generateBuildingRatios()
        self.getStreetBlocks()
        self.fillStreetBlocks()
        self.placeBuildings()

        self.createPopulation()
        self.getWorkPlaces()
        self.assignJobs()
        self.assignOfficials()
        self.createOpinions()

        self.buildPlayMap()

    def addToBuildingPoints(self, building_type, point):
        self.work_places_dict = {'Tavern':           self.tavern,
                                 'PublicPlumbing':   self.publicplumbing,
                                 'Market':           self.market,
                                 'TradePost':        self.tradepost,
                                 'Doctor':           self.doctor,
                                 'Inn':              self.inn,
                                 'Special':          self.special,
                                 'Barn':             self.special,
                                 'Mine':             self.special,
                                 'Butcher':          self.special,
                                 'Mason':            self.special,
                                 'Blacksmith':       self.special,
                                 'Weavery':          self.special,
                                 'Barracks':         self.special,
                                 'Lumbermill':       self.special,
                                 'Cathedral':        self.special,
                                 'Colosseum':        self.special}
        try:
            self.work_places_dict[building_type].append(self.map_points[point.y][point.x])

        except KeyError:
            print('{} not a valid building type in addToBuildingPoints'.format(building_type))

    def addNewEmployee(self, place, dude):
        if place.building_type == 'Tavern':
            owners = 0

            for other_blocks in self.tavern:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    else:
                        pass

            if owners == 0:
                dude.job_title = 'Owner'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'NobleHouse':
            dude.job_title = 'Servant'

        elif place.building_type == 'PublicPlumbing':
            dude.job_title = 'Janitor'

        elif place.building_type == 'Market':
            sellers = 0

            for other_blocks in self.market:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Seller':
                        sellers = sellers + 1
                    else:
                        pass

            if sellers < 10:
                dude.job_title = 'Seller'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'TradePost':
            traders = 0

            for other_blocks in self.tradepost:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Trader':
                        traders = traders + 1
                    else:
                        pass

                if traders < 10:
                    dude.job_title = 'Trader'
                else:
                    dude.job_title = 'Worker'

        elif place.building_type == 'Doctor':
            doctors = 0

            for other_blocks in self.doctor:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Doctor':
                        traders = traders + 1
                    else:
                        pass

                if traders < 5:
                    dude.job_title = 'Doctor'
                else:
                    dude.job_title = 'Nurse'

        elif place.building_type == 'Inn':
            owners = 0

            for other_blocks in self.inn:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    else:
                        pass

                if owners == 0:
                    dude.job_title = 'Owner'
                else:
                    dude.job_title = 'Worker'

        # There's currently only one special building per map right now, as per
        # the Town.economy
        elif place.building_type == 'Barn':
            owners = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    else:
                        pass

            if owners == 0:
                dude.job_title = 'Owner'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Mine':
            foremen = 0

            for other_blocks in self.inn:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Foreman':
                        foremen = foremen + 1
                    else:
                        pass

            if foremen < 5:
                dude.job_title = 'Foreman'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Butcher':
            butchers = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Butcher':
                        butchers = butchers + 1
                    else:
                        pass

            if butchers < 8:
                dude.job_title = 'Butcher'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Mason':
            foremen = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Foreman':
                        foremen = foremen + 1
                    else:
                        pass

            if foremen < 5:
                dude.job_title = 'Foreman'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Blacksmith':
            smiths = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Smith':
                        smiths = smiths + 1
                    else:
                        pass

            if smiths < 5:
                dude.job_title = 'Smith'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Weavery':
            owners = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    else:
                        pass

            if owners == 0:
                dude.job_title = 'Owner'
            else:
                dude.job_title = 'Weaver'

        elif place.building_type == 'Barracks':
            sergeants = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Sergeant':
                        sergeants = sergeants + 1
                    else:
                        pass

            if sergeants < 5:
                dude.job_title = 'Sergeant'
            else:
                dude.job_title = 'Soldier'

        elif place.building_type == 'Lumbermill':
            owners = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    else:
                        pass

            if owners == 0:
                dude.job_title = 'Owner'
            else:
                dude.job_title = 'Worker'

        elif place.building_type == 'Cathedral':
            priests = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Priest':
                        priests = priests + 1
                    else:
                        pass

            if priests < 5:
                dude.job_title = 'Priest'
            else:
                dude.job_title = 'Acolyte'

        elif place.building_type == 'Colosseum':
            owners = 0
            entertainers = 0

            for other_blocks in self.special:
                for peep in other_blocks.employees:
                    if peep.job_title == 'Owner':
                        owners = owners + 1
                    elif peep.job_title == 'Entertainer':
                        entertainers = entertainers + 1
                    else:
                        pass

            if owners == 0:
                dude.job_title = 'Owner'
            elif entertainers < 5:
                dude.job_title = 'Entertainer'
            else:
                dude.job_title = 'Worker'

        else:
            # print('Not a valid building type in addToBuildingPoints')
            pass

        place.employees.append(dude)
        dude.employed = True
        dude.workplace = place
        # print('Added {} {} to {}.'.format(dude.name, dude.family_name,
        #                                   dude.workplace.building_type))

    def assignJobs(self):
        num_to_employ = int(self.workable * self.employment / 100)
        # print('{} - {}'.format(num_to_employ / len(self.workplaces),
        #                        self.employment))
        every_place_has_one = False
        every_one_list = []

        for place in self.workplaces:
            every_one_list.append(place)

        # print('Number to employ: {}'.format(num_to_employ))

        employed = 0
        for dude in self.people:
            if employed == num_to_employ:
                # print('Employed {} people.'.format(employed))
                break

            num_workplaces = len(self.workplaces)
            if not dude.employed:
                if dude.age == 'Adult' or dude.age == 'YoungAdult':

                    if not every_place_has_one:
                        if len(every_one_list) != 0:
                            workplace_idx = random.randint(0, len(every_one_list) - 1)
                            workplace = every_one_list.pop(workplace_idx)

                            self.addNewEmployee(workplace, dude)

                        else:
                            every_place_has_one = True

                    else:
                        workplace_idx = random.randint(0, num_workplaces - 1)
                        workplace = self.workplaces[workplace_idx]

                        self.addNewEmployee(workplace, dude)

                        # Scales with wealth to make sure we have enough places
                        # for workers
                        if len(workplace.employees) >= (random.randint(1, 3)
                                                        + num_to_employ / len(self.workplaces)):
                            self.workplaces.remove(workplace)

                    employed = employed + 1
                    # print('{} - Employed {} {} at {}.'.format(employed, dude.name,
                    #                                           dude.family_name,
                    #                                           workplace.building_type))

    def assignName(self):
        name_idx = random.randint(0, t_names_len - 1)
        self.name = t_names[name_idx]

    def assignOfficials(self):
        all_assigned = False
        num_officials_to_go = 10
        num_mayor_to_go = 1

        while not all_assigned:
            new_rand_idx = random.randint(0, len(self.people) - 1)
            dude = self.people[new_rand_idx]

            if (not dude.employed) and (dude.wealth != 'Poor') and\
            (dude.age != 'Baby'):
                    if num_mayor_to_go == 1:
                        dude.job_title = 'Mayor'
                        dude.employed = True
                        self.mayor = dude
                        num_mayor_to_go = 0
                    elif num_officials_to_go > 0:
                        dude.job_title = 'Official'
                        dude.employed = True
                        self.officials.append(dude)
                        num_officials_to_go = num_officials_to_go - 1
                    else:
                        all_assigned = True

            else:
                continue

        # print('Mayor: {} {}'.format(self.mayor.name, self.mayor.family_name))

        # print('Officials:\n', end='')
        # for dude in self.officials:
        #     print('\t{} {}'.format(dude.name, dude.family_name))

    def assignWorkplace(self, person, building):
        pass

    def buildFamilyTree(self, l_name, wealth):
        family_list = []

        old_generation = []
        mid_generation = []
        yng_generation = []

        # Generate old_generation
        for i in range(10):
            old = person.Person()
            old.age = 'Old'

            if random.randint(0, 1) > 0:
                old.gender = 'Male'
            else:
                old.gender = 'Female'

            old.setName()
            old.family_name = l_name
            old.wealth = wealth

            old_generation.append(old)

        # Generate mid_generation
        for i in range(15):
            mid = person.Person()

            if random.randint(0, 1) > 0:
                mid.age = 'Adult'
            else:
                mid.age = 'YoungAdult'

            if random.randint(0, 1) > 0:
                mid.gender = 'Male'
            else:
                mid.gender = 'Female'

            mid.setName()
            mid.family_name = l_name
            mid.wealth = wealth

            mid_generation.append(mid)

        # Generate yng_generation
        for i in range(20):
            yng = person.Person()

            if random.randint(0, 1) > 0:
                yng.age = 'Child'
            else:
                yng.age = 'Baby'

            if random.randint(0, 1) > 0:
                yng.gender = 'Male'
            else:
                yng.gender = 'Female'

            yng.setName()
            yng.family_name = l_name
            yng.wealth = wealth

            yng_generation.append(yng)

        family_list.append(old_generation)
        family_list.append(mid_generation)
        family_list.append(yng_generation)

        family_list = self.linkFamilyRelations(family_list)

        return family_list

    def buildMap(self):
        self.height = 20
        self.width = 20
        self.road_area = 0

        height = self.height
        width = self.width

        self.map_points = [[None for i in range(width)] for j in range(height)]
        self.map_area = height * width

        for y, row in enumerate(self.map_points):
            for x, cell in enumerate(row):
                building = Building('none', x, y)

                # Place roads on map edge
                if (x == 0) or (x == width - 1):
                    if y == 0 and x == 0:
                        building.building_type = 'TLCRoad'
                    elif y == 0 and x == width - 1:
                        building.building_type = 'TRCRoad'
                    elif y == height - 1 and x == 0:
                        building.building_type = 'BLCRoad'
                    elif y == height - 1 and x == width - 1:
                        building.building_type = 'BRCRoad'
                    elif (y == int(height/3) or y == int(2*height/3)) and x == 0:
                        building.building_type = 'RIRoad'
                    elif (y == int(height/3) or y == int(2*height/3)) and x == width - 1:
                        building.building_type = 'LIRoad'
                    else:
                        building.building_type = 'VRoad'

                    self.road_area = self.road_area + 1

                # A couple simple straight roads
                elif (x == int(width/3)) or (x == int(2*width/3)):
                    if y == 0:
                        building.building_type = 'DIRoad'
                    elif y == height - 1:
                        building.building_type = 'UIRoad'
                    elif y == int(height/3) or y == int(2*height/3):
                        building.building_type = 'IRoad'
                    else:
                        building.building_type = 'VRoad'

                    self.road_area = self.road_area + 1

                elif (y == 0 or y == height - 1 or y == int(height/3) or y ==
                      int(2*height/3)):
                    building.building_type = 'HRoad'

                    self.road_area = self.road_area + 1

                self.map_points[y][x] = building

    def buildPlayMap(self):
        pass

    def createFamily(self, wealth, house):
        family = []
        family_name = person.createFamilyName()
        family_size = random.randint(1, 10)

        self.increasePopulation(family_size)
        unpruned_family_list = self.buildFamilyTree(family_name, wealth)

        serial_family_list = (unpruned_family_list[0] + unpruned_family_list[1]
                              + unpruned_family_list[2])

        for dude in serial_family_list:
            if dude.relations == []:
                if random.randint(0, 9) > 2:
                    serial_family_list.remove(dude)

        for i in range(family_size):
            length = len(serial_family_list) - 1
            rand = random.randint(0, length)
            family.append(serial_family_list.pop(rand))

        # Assemble relations_in_house
        for dude in family:
            if dude.age == 'YoungAdult' or dude.age == 'Adult':
                self.workable = self.workable + 1
            for i, other_dude in enumerate(dude.relation_persons):
                if other_dude in family:
                    dude.relation_persons_in_house.append(other_dude)
                    dude.relations_in_house.append(dude.relations[i])

        # self.logger.debug('Family - {}'.format(family_name))
        # for dude in family:
            # print('Name - {0} - {1}'.format(dude, dude.age))

        for dude in family:
            dude.house = house

        return family

    def createOpinions(self):
        for dude in self.people:

            # Family opinions
            # print('Creating family member opinions')
            for member in dude.relation_persons_in_house:
                dude.opinion_of_others[member] = random.randint(-2, 2)
                # print('{} {}\'s opinion of {} {} is {}'.format(dude.name,
                #                                                dude.family_name,
                #                                                member.name,
                #                                                member.family_name,
                #                                                dude.opinion_of_others[member]))

            # Coworker opinions
            if dude.employed and dude.job_title != 'Mayor' and dude.job_title != 'Official':
                # print('\nCreating coworker opinions')
                if dude.workplace.building_type == 'NobleHouse':
                    for coworker in dude.workplace.employees:
                        dude.opinion_of_others[coworker] = random.randint(-2, 2)
                        # print('{} {}\'s opinion of {} {} is {}'.format(dude.name,
                        #                                                dude.family_name,
                        #                                                coworker.name,
                        #                                                coworker.family_name,
                        #                                                dude.opinion_of_others[coworker]))

                else:
                    try:
                        for point in self.work_places_dict[dude.workplace.building_type]:
                            for coworker in point.employees:
                                dude.opinion_of_others[coworker] = random.randint(-2, 2)
                                # print('{} {}\'s opinion of {} {} is {}'.format(dude.name,
                                #                                                dude.family_name,
                                #                                                coworker.name,
                                #                                                coworker.family_name,
                                #                                                dude.opinion_of_others[coworker]))
                    except KeyError:
                        # Either an unhandled builing_type or dude is not actually
                        # employed
                        print('{} not a valid building type in dude.workplace in createOpinions'.format(dude.workplace.building_type))

            # Neighbor opinions
            # print('\nCreating neighbor opinions')
            for y_pos in range(dude.house.y - 5, dude.house.y + 5):
                for x_pos in range(dude.house.x - 5, dude.house.x + 5):

                    if x_pos < 0 or x_pos > self.width - 1 or y_pos < 0 or y_pos > self.height - 1:
                        continue

                    neighbor_house = self.map_points[y_pos][x_pos]
                    for neighbor in neighbor_house.people:
                        dude.opinion_of_others[neighbor] = random.randint(-2, 2)
                        # print('{} {}\'s opinion of {} {} is {}'.format(dude.name,
                        #                                                dude.family_name,
                        #                                                neighbor.name,
                        #                                                neighbor.family_name,
                        #                                                dude.opinion_of_others[neighbor]))

    def createPopulation(self):
        self.people = []
        for house in self.noble_houses:
            family = self.createFamily('Noble', house)
            house.people = family

            for dude in family:
                # print('Adding {} {} to town population.'.format(dude.name,
                #                                                 dude.family_name))
                self.people.append(dude)

        for house in self.middle_houses:
            family = self.createFamily('Middle', house)
            house.people = family

            for dude in family:
                # print('Adding {} {} to town population.'.format(dude.name,
                #                                                 dude.family_name))
                self.people.append(dude)

        for house in self.poor_houses:
            family = self.createFamily('Poor', house)
            house.people = family

            for dude in family:
                # print('Adding {} {} to town population.'.format(dude.name,
                #                                                 dude.family_name))
                self.people.append(dude)

    def createPointPlacementRadius(self):
        radius = []

        for r in range(0, 101):
            x = r
            y = 0
            err = 0

            while x >= y:
                radius.append(Point(x, y))
                radius.append(Point(y, x))
                radius.append(Point(-y, x))
                radius.append(Point(-x, y))
                radius.append(Point(-x, -y))
                radius.append(Point(-y, -x))
                radius.append(Point(y, -x))
                radius.append(Point(x, -y))

                y = y + 1
                err = err + 1 + 2*y
                if (2*(err - x) + 1) > 0:
                    x = x - 1
                    err = err + 1 - 2*x

        self.placement_radius = list(unique_everseen(radius))
        #seen = list()
        #seen_add = seen.append
        #self.placement_radius = [x for x in radius if not (x in seen or seen_add(x))]

    def createRoadsEquations(self, string):
        self.horizontal_roads_m = []
        self.horizontal_roads_b = []
        self.vertical_roads_m = []
        self.vertical_roads_b = []

        map_width = self.y_max - self.y_min
        map_height = self.x_max - self.x_min

        median_map_width = 72
        median_map_height = 72
        median_road_num = 5

        horizontal_roads_num = int(map_height / median_map_height *
                                   median_road_num - ((int(string[0]) - 4.5) / 3))
        vertical_roads_num =   int(map_width / median_map_width *
                                   median_road_num - ((int(string[1]) - 4.5) / 3))

        horizontal_road_space = int(map_height / (horizontal_roads_num + 1))
        vertical_road_space =   int(map_width / (vertical_roads_num + 1))

        for i in range(0, horizontal_roads_num - 2):
            horizontal_slope =     ((int(string[i + 2]) - 4.5) / 18)
            horizontal_intercept = (((int(string[i + 2 + horizontal_roads_num - 1])
                                      - 4.5) / 36) + (i + 1) *
                                    horizontal_road_space - map_height/2)

            self.horizontal_roads_m.append(horizontal_slope)
            self.horizontal_roads_b.append(horizontal_intercept)

        for i in range(0, vertical_roads_num - 2):
            inv_vertical_slope = ((int(string[i + 2 + horizontal_roads_num * 2 - 1])
                                   - 4.5) / 18)
            vertical_x_intercept = (((int(string[i + 2 + horizontal_roads_num * 2 -
                                   1 + vertical_roads_num - 1]) - 4.5) / 36) +
                                   (i + 1) * vertical_road_space - map_width/2)

            if inv_vertical_slope == 0:
                inv_vertical_slope = 0.1

            vertical_slope = pow(inv_vertical_slope, -1)
            vertical_intercept = -1 * vertical_x_intercept * vertical_slope

            self.vertical_roads_m.append(vertical_slope)
            self.vertical_roads_b.append(vertical_intercept)

    def fillStreetBlocks(self):
        types_for_use = self.getAvailableBlocks()

        for block in self.block_list:
            rand_select = random.randint(0, len(types_for_use) - 1)
            block.wealth = types_for_use.pop(rand_select)

    def generateBuildingRatios(self):
        area_mod = self.wealth / 25
        map_unit_area = 5256

        self.tavern_area =   int(30  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.plumbing_area = int(20  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.market_area =   int(100 * (1 + area_mod) * (self.map_area/map_unit_area))
        self.trade_area =    int(60  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.doctor_area =   int(30  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.inn_area =      int(30  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.special_area =  int(100 * (1 + area_mod) * (self.map_area/map_unit_area))
        self.empty_area =    int(20  * (self.map_area/map_unit_area))

        free_area =  int(self.map_area - self.tavern_area - self.plumbing_area -
                         self.market_area - self.trade_area - self.inn_area -
                         self.special_area - self.road_area - self.empty_area -
                         self.doctor_area)

        self.number_noble_house =  int(free_area * (0.03 + self.wealth/100))
        self.number_middle_house = int(free_area * (0.1 + self.wealth/100))
        self.number_poor_house =   int((free_area - self.number_noble_house -
                                        self.number_middle_house)*0.25)

        '''
        self.logger.debug('Noble area:\t', self.number_noble_house, '\t',
                    int(self.number_noble_house/free_area * 100), '%')

        self.logger.debug('Middle area:\t', self.number_middle_house, '\t',
                    int(self.number_middle_house/free_area * 100), '%')

        self.logger.debug('Poor area:\t', self.number_poor_house, '\t',
                    int(self.number_poor_house/free_area * 100), '%')
        '''

    def generateEconomy(self):
        self.economy = TownEconomy[random.randint(0, 8)]

    def generateDanger(self):
        if self.economy == 'Military':
            self.danger_mod = 0.4
        elif self.economy == 'Church':
            self.danger_mod = 0.6
        elif self.economy == 'Colosseum':
            self.danger_mod = 0.6
        else:
            self.danger_mod = 1

        self.danger = int(self.danger_mod*random.randint(0, 9))

    def generateHomeless(self):
        self.settled_ratio = int(10*(random.randint(0, 9)/6 + self.wealth/2 + 7))

    def generateMap(self, string):
        def grouped(iterable, n):
            return zip(*[iter(iterable)]*n)

        map_unit_size = [-25, 25, 25, 25, 25, -25, -25, -25]
        raw_map_corners = []
        self.map_corners = []
        self.map_points = []
        self.x_coordinates = []
        self.y_coordinates = []
        self.draw_order = []
        self.draw_segs = []
        scale = 10

        self.map_size_mod = int(string[0])/(scale + 30) + 1
        self.map_corners_mod = [int(string[1])/scale + 1,
                                int(string[2])/scale + 1,
                                int(string[3])/scale + 1,
                                int(string[4])/scale + 1,
                                int(string[5])/scale + 1,
                                int(string[6])/scale + 1,
                                int(string[7])/scale + 1,
                                int(string[8])/scale + 1]

        for i in range(0, len(self.map_corners_mod)):
            raw_map_corners.append(int(self.map_corners_mod[i] *
                                       map_unit_size[i] *
                                       self.map_size_mod))

        for x, y in grouped(raw_map_corners, 2):
            self.x_coordinates.append(x)
            self.y_coordinates.append(y)

            point = MapPoint(x, y)
            self.map_corners.append(point)

        self.x_min = min(self.x_coordinates)
        self.x_max = max(self.x_coordinates)
        self.y_min = min(self.y_coordinates)
        self.y_max = max(self.y_coordinates)

        y_coords = self.y_coordinates

        self.draw_order.append(self.map_corners[y_coords.index(max(y_coords))])
        y_coords[y_coords.index(max(y_coords))] = -1000

        self.draw_order.append(self.map_corners[y_coords.index(max(y_coords))])
        y_coords[y_coords.index(max(y_coords))] = -1000

        self.draw_order.append(self.map_corners[y_coords.index(max(y_coords))])
        y_coords[y_coords.index(max(y_coords))] = -1000

        self.draw_order.append(self.map_corners[y_coords.index(max(y_coords))])
        y_coords[y_coords.index(max(y_coords))] = -1000

        if self.draw_order[2].x > self.draw_order[3].x:
            first_draw = 'bottom'
            self.draw_segs.append([self.draw_order[3],
                                   self.draw_order[2]])

            if self.draw_order[0].x > self.draw_order[1].x:
                self.draw_segs.append([self.draw_order[2],
                                       self.draw_order[0]])
                self.draw_segs.append([self.draw_order[0],
                                       self.draw_order[1]])
                self.draw_segs.append([self.draw_order[1],
                                       self.draw_order[3]])
            else:
                self.draw_segs.append([self.draw_order[2],
                                       self.draw_order[1]])
                self.draw_segs.append([self.draw_order[1],
                                       self.draw_order[0]])
                self.draw_segs.append([self.draw_order[0],
                                       self.draw_order[3]])

        elif self.draw_order[0].x > self.draw_order[1].x:
            first_draw = 'right'
            self.draw_segs.append([self.draw_order[3],
                                   self.draw_order[0]])
            self.draw_segs.append([self.draw_order[0],
                                   self.draw_order[1]])
            self.draw_segs.append([self.draw_order[1],
                                   self.draw_order[2]])
            self.draw_segs.append([self.draw_order[2],
                                   self.draw_order[3]])

        else:
            first_draw = 'right'
            self.draw_segs.append([self.draw_order[3],
                                   self.draw_order[1]])
            self.draw_segs.append([self.draw_order[1],
                                   self.draw_order[0]])
            self.draw_segs.append([self.draw_order[0],
                                   self.draw_order[2]])
            self.draw_segs.append([self.draw_order[2],
                                   self.draw_order[3]])

        # Anti-clockwise from the bottom
        self.draw_slopes = [0, 0, 0, 0]
        self.draw_intercepts = [0, 0, 0, 0]
        for i in range(0, 4):
            try:
                self.draw_slopes[i] = ((self.draw_segs[i][0].y - self.draw_segs[i][1].y)/
                                       (self.draw_segs[i][0].x - self.draw_segs[i][1].x))

                self.draw_intercepts[i] = (self.draw_segs[i][0].y -
                                           self.draw_slopes[i]*self.draw_segs[i][0].x)

            except ZeroDivisionError:
                self.draw_slopes[i] = 1000

        for y in range(self.y_max, self.y_min - 1, -1):
            for x in range(self.x_min, self.x_max + 1):
                point = MapPoint(x, y)

                if first_draw == 'bottom':
                    for i in range(-1, 3):
                        if i == -1:
                            if self.draw_slopes[i] != 'inf':
                                if self.draw_slopes[i] < 0:
                                    if point.y >= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                elif self.draw_slopes[i] > 0:
                                    if point.y <= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                else:
                                    self.logger.warning('Unhandled draw_slope[] value')
                            else:
                                if point.x >= self.draw_segs[i][0].x:
                                    continue
                                else:
                                    break

                        elif i == 0:
                            if self.draw_slopes[i] == 0:
                                if point.y >= self.draw_segs[i][0].y:
                                    continue
                                else:
                                    break
                            else:
                                if point.y >= (point.x * self.draw_slopes[i] +
                                               self.draw_intercepts[i]):
                                    continue
                                else:
                                    break
                        elif i == 1:
                            if self.draw_slopes[i] != 'inf':
                                if self.draw_slopes[i] < 0:
                                    if point.y <= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                elif self.draw_slopes[i] > 0:
                                    if point.y >= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                else:
                                    self.logger.warning('Unhandled draw_slope[] value')
                            else:
                                if point.x <= self.draw_segs[i][0].x:
                                    continue
                                else:
                                    break
                        elif i == 2:
                            if self.draw_slopes[i] == 0:
                                if point.y <= self.draw_segs[i][0].y:
                                    continue
                                else:
                                    break
                            else:
                                if point.y <= (point.x * self.draw_slopes[i] +
                                               self.draw_intercepts[i]):
                                    continue
                                else:
                                    break
                    else:
                        self.map_points.append(point)
                else:
                    for i in range(-2, 2):
                        if i == -2:
                            if self.draw_slopes[i] != 'inf':
                                if self.draw_slopes[i] < 0:
                                    if point.y >= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                elif self.draw_slopes[i] > 0:
                                    if point.y <= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                else:
                                    self.logger.warning('Unhandled draw_slope[] value')
                            else:
                                if point.x >= self.draw_segs[i][0].x:
                                    continue
                                else:
                                    break

                        elif i == -1:
                            if self.draw_slopes[i] == 0:
                                if point.y >= self.draw_segs[i][0].y:
                                    continue
                                else:
                                    break
                            else:
                                if point.y >= (point.x * self.draw_slopes[i] +
                                               self.draw_intercepts[i]):
                                    continue
                                else:
                                    break
                        elif i == 0:
                            if self.draw_slopes[i] != 'inf':
                                if self.draw_slopes[i] < 0:
                                    if point.y <= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                elif self.draw_slopes[i] > 0:
                                    if point.y >= (point.x * self.draw_slopes[i] +
                                                   self.draw_intercepts[i]):
                                        continue
                                    else:
                                        break
                                else:
                                    self.logger.warning('Unhandled draw_slope[] value')
                            else:
                                if point.x <= self.draw_segs[i][0].x:
                                    continue
                                else:
                                    break
                        elif i == 1:
                            if self.draw_slopes[i] == 0:
                                if point.y <= self.draw_segs[i][0].y:
                                    continue
                                else:
                                    break
                            else:
                                if point.y <= (point.x * self.draw_slopes[i] +
                                               self.draw_intercepts[i]):
                                    continue
                                else:
                                    break
                    else:
                        self.map_points.append(point)
        self.map_area = len(self.map_points)

    def generateNobility(self):
        if self.economy == 'Church':
            self.nobility_mod = 0.5
        elif self.economy == 'Military':
            self.nobility_mod = 0.4
        else:
            self.nobility_mod = 0.35

        self.nobility = int(10*self.nobility_mod*random.randint(0, 9))

    def generateWealth(self):
        self.wealth = random.randint(1, 9) - 5
        self.employment = (self.wealth + 6) * 10

    def getAvailableBlocks(self):
        self.noble_blocks =  int(len(self.block_list) * self.number_noble_house /
                                 (self.number_noble_house + self.number_middle_house
                                 + self.number_poor_house))

        self.middle_blocks = int(len(self.block_list) * self.number_middle_house /
                                (self.number_noble_house + self.number_middle_house
                                + self.number_poor_house))

        self.poor_blocks = len(self.block_list) - self.noble_blocks - self.middle_blocks

        available_block_types = []
        for i in range(self.noble_blocks):
            available_block_types.append('NobleHouse')

        for i in range(self.middle_blocks):
            available_block_types.append('MiddleHouse')

        for i in range(self.poor_blocks):
            available_block_types.append('PoorHouse')

        return available_block_types

    def getHousePerBlock(self):
        try:
            n_house_per_block = self.number_noble_house / self.noble_blocks
        except ZeroDivisionError:
            n_house_per_block = 0

        try:
            m_house_per_block = self.number_middle_house / self.middle_blocks
        except ZeroDivisionError:
            m_house_per_block = 0

        try:
            p_house_per_block = self.number_poor_house / self.poor_blocks
        except ZeroDivisionError:
            p_house_per_block = 0

        house_per_block = {'NobleHouse':n_house_per_block,
                           'MiddleHouse':m_house_per_block,
                           'PoorHouse':p_house_per_block}

        return house_per_block

    def getNewPoint(self, start, i):
        global placement_radius
        move_x = placement_radius[i].x
        move_y = placement_radius[i].y

        if start.x + move_x >= self.width or start.y + move_y >= self.height:
            return start

        return Point(start.x + move_x, start.y + move_y)

    def getStreetBlocks(self):
        self.block_list = []

        height = self.height
        width = self.width

        for j in range(3):
            for i in range(3):
                top_left_x  = int(i*width/3)        + 1
                top_left_y  = int(j*height/3)       + 1
                bot_right_x = int((i + 1)*width/3)  - 1
                bot_right_y = int((j + 1)*height/3) - 1

                block = Block(top_left_x, top_left_y, bot_right_x, bot_right_y)
                self.block_list.append(block)

    def getWorkPlaces(self):
        self.workplaces = []

        for row in self.map_points:
            for place in row:
                if place.building_type in Work_Places:
                    self.workplaces.append(place)

    def increasePopulation(self, num):
        self.population = self.population + num

    def linkFamilyRelations(self, family):
        possible_indices = [i for i in range(10)]
        pair = []
        num_old_relations = 4

        # Old person marriages
        for i in range(num_old_relations * 2):
            pair.append(possible_indices.pop(random.randint(0, len(possible_indices) - 1)))

            if i % 2 != 0:
                if True:
                    l_person = family[0][pair[0]]
                    r_person = family[0][pair[1]]

                    l_person.addRelation(r_person, 'Spouse')
                    r_person.addRelation(l_person, 'Spouse')
                    # print(r_person, l_person, ' - Old Spouses')

                pair.pop()
                pair.pop()

        possible_indices = [i for i in range(15)]
        possible_old_indices = [i for i in range(10)]
        num_mid_to_old_relations = 10

        # Father/Mother -> Son/Daughter from Old to Mid
        for i in range(num_mid_to_old_relations):
            # Mid generation person
            first = possible_indices.pop(random.randint(0, len(possible_indices) - 1))
            # Old person
            second = possible_old_indices[random.randint(0, len(possible_old_indices) - 1)]
            if True:
                l_person = family[1][first]
                r_person = family[0][second]

                l_person.addRelation(r_person, 'Parent')
                r_person.addRelation(l_person, 'Child')
                # print(l_person, r_person, ' - Child -> Parent')

        # Link shared children
        for old in family[0]:
            if 'Spouse' in old.relations:
                spouse = old.relation_persons[old.relations.index('Spouse')]

                for i, relation in enumerate(old.relations):
                    if relation == 'Child':
                        child = old.relation_persons[i]

                        if not spouse.alreadyHasRelation(child):
                            spouse.addRelation(child, 'Child')
                            child.addRelation(spouse, 'Parent')
                            # print('Added {0} to {1}\'s relations as child'.format(child, spouse))

        # Link brother/sisters based on last two link loops
        for mid in family[1]:
            if 'Parent' in mid.relations:

                for i, parent in enumerate(range(mid.relations.count('Parent'))):
                    # Get the i'th occurance of Parent
                    parent_person_idx = -1
                    for j in range(i + 1):
                        parent_person_idx = mid.relations.index('Parent', parent_person_idx + 1)

                    parent_person = mid.relation_persons[parent_person_idx]
                    for second_mid in family[1]:
                        # Skip the person we're matching with
                        if second_mid == mid:
                            continue
                        if not mid.alreadyHasRelation(second_mid):
                            if parent_person in second_mid.relation_persons:
                                second_mid.addRelation(mid, 'Sibling')
                                mid.addRelation(second_mid, 'Sibling')
                                # print(mid, second_mid, ' - Mid Siblings')

        l_spouses = []
        r_spouses = []

        # Mid person marriages
        for person in family[1]:
            # In other words, if not already part of the family
            if 'Parent' not in person.relations:
                l_spouses.append(person)
            else:
                r_spouses.append(person)

        for person in l_spouses:
            if random.randint(0, 9) > 2:
                try:
                    pair = r_spouses.pop(random.randint(0, len(r_spouses) - 1))
                except IndexError:
                    # r_spouses is empty
                    for possible_match in l_spouses:
                        if 'Spouse' not in l_spouses:
                            if possible_match != person:
                                if possible_match not in person.relation_persons:
                                    pair = possible_match

                person.addRelation(pair, 'Spouse')
                pair.addRelation(person, 'Spouse')
                # print(person, pair, ' - Mid Spouses')

        possible_yng_indices = [i for i in range(20)]
        possible_mid_indices = [i for i in range(15)]
        num_yng_to_mid_relations = 10

        # Father/Mother -> Son/Daughter from Mid to Yng
        for i in range(num_yng_to_mid_relations):
            # Yng generation person
            first = possible_yng_indices.pop(random.randint(0, len(possible_yng_indices) - 1))
            # Mid person
            second = possible_mid_indices[random.randint(0, len(possible_mid_indices) - 1)]
            if True:
                l_person = family[2][first]
                r_person = family[1][second]

                l_person.addRelation(r_person, 'Parent')
                r_person.addRelation(l_person, 'Child')
                # print(l_person, r_person, ' - Child -> Parent')

        # Link shared children
        for mid in family[1]:
            if 'Spouse' in mid.relations:
                spouse = mid.relation_persons[mid.relations.index('Spouse')]

                for i, relation in enumerate(mid.relations):
                    if relation == 'Child':
                        child = mid.relation_persons[i]

                        if not spouse.alreadyHasRelation(child):
                            if random.randint(0, 9) > 2:
                                spouse.addRelation(child, 'Child')
                                child.addRelation(spouse, 'Parent')
                                # print('Added {0} to {1}\'s relations as child'.format(child, spouse))

        # Link parent siblings with sibling children
        for yng in family[2]:
            if 'Parent' in yng.relations:
                for i, parent_num in enumerate(range(yng.relations.count('Parent'))):
                    # Get the i'th occurance of Parent
                    parent_person_idx = -1
                    for j in range(i + 1):
                        parent_person_idx = yng.relations.index('Parent', parent_person_idx + 1)

                    parent = yng.relation_persons[parent_person_idx]

                    # Aunts and uncles
                    if 'Sibling' in parent.relations:
                        for k, sibling_num in enumerate(range(parent.relations.count('Sibling'))):
                            # Get the i'th occurance of Sibling
                            sibling_person_idx = -1
                            for m in range(k + 1):
                                sibling_person_idx = parent.relations.index('Sibling', sibling_person_idx + 1)

                            sibling = parent.relation_persons[sibling_person_idx]

                            if not yng.alreadyHasRelation(sibling):
                                if 'Spouse' in sibling.relations:
                                    sib_spouse = sibling.relation_persons[sibling.relations.index('Spouse')]
                                    yng.addRelation(sib_spouse, 'ParentSibling')
                                    sib_spouse.addRelation(yng, 'SiblingChild')
                                    # print(yng, sib_spouse, ' - SiblingChild -> ParentSibling')

                                yng.addRelation(sibling, 'ParentSibling')
                                sibling.addRelation(yng, 'SiblingChild')
                                # print(yng, sibling, ' - SiblingChild -> ParentSibling')

                            # Cousins
                            if 'Child' in sibling.relations:
                                for l, child_num in enumerate(range(sibling.relations.count('Child'))):
                                    # Get the i'th occurance of Child
                                    child_person_idx = -1
                                    for n in range(l + 1):
                                        child_person_idx = sibling.relations.index('Child', child_person_idx + 1)

                                    child = sibling.relation_persons[child_person_idx]
                                    if not yng.alreadyHasRelation(child):
                                        yng.addRelation(child, 'Cousin')
                                        child.addRelation(yng, 'Cousin')
                                        # print(yng, child, ' - Cousins')


                    # Siblings
                    if 'Child' in parent.relations:
                        for k, child_num in enumerate(range(parent.relations.count('Child'))):
                            # Get the i'th occurance of Child
                            child_person_idx = -1
                            for m in range(k + 1):
                                child_person_idx = parent.relations.index('Child', child_person_idx + 1)

                            child = parent.relation_persons[child_person_idx]

                            if yng != child:
                                if not yng.alreadyHasRelation(child):
                                    yng.addRelation(child, 'Sibling')
                                    child.addRelation(yng, 'Sibling')
                                    # print(yng, child, ' - Yng Siblings')

                    # Grandparents
                    if 'Parent' in parent.relations:
                        for k, gparent_num in enumerate(range(parent.relations.count('Parent'))):
                            # Get the i'th occurance of Parent
                            gparent_person_idx = -1
                            for m in range(k + 1):
                                gparent_person_idx = parent.relations.index('Parent', gparent_person_idx + 1)

                            gparent = parent.relation_persons[gparent_person_idx]

                            if not yng.alreadyHasRelation(gparent):
                                yng.addRelation(gparent, 'Grandparent')
                                gparent.addRelation(yng, 'Grandchild')
                                # print(yng, gparent, ' - Grandchild -> Grandparent')

        return family

    def placeBuildings(self):
        # List of MapPoints pointing to self.map_points[] which contains
        # buildings and empty space
        self.noble_houses = []
        self.middle_houses = []
        self.poor_houses = []

        self.tavern = []
        self.publicplumbing = []
        self.market = []
        self.tradepost = []
        self.doctor = []
        self.inn = []
        self.special = []

        self.placed_nobles = 0
        self.placed_middle = 0
        self.placed_poor = 0
        self.special_building_dict = {'tavern_idx':None, 'plumbing_idx':None,
                                      'market_idx':None, 'trade_idx':None,
                                      'inn_idx':None, 'special_idx':None}

        house_per_block = self.getHousePerBlock()

        # Assigning unique self.block_list indexes to special buildings
        idx_list = []
        while len(idx_list) < 6:
            new_idx = random.randint(0, len(self.block_list) - 1)
            if new_idx not in idx_list:
                idx_list.append(new_idx)

        for i, building in enumerate(self.special_building_dict):
            self.special_building_dict[building] = idx_list[i]

        # Placing special buildings
        for building, block_idx in self.special_building_dict.items():
            block = self.block_list[block_idx]

            if building == 'tavern_idx':
                num_points = self.tavern_area
                point_building = 'Tavern'
            elif building == 'plumbing_idx':
                num_points = self.plumbing_area
                point_building = 'PublicPlumbing'
            elif building == 'market_idx':
                num_points = self.market_area
                point_building = 'Market'
            elif building == 'trade_idx':
                num_points = self.trade_area
                point_building = 'TradePost'
            elif building == 'inn_idx':
                num_points = self.inn_area
                point_building = 'Inn'
            elif building == 'special_idx':
                num_points = self.special_area
                if self.economy == 'Farm':
                    point_building = 'Barn'
                elif self.economy == 'Military':
                    point_building = 'Barracks'
                elif self.economy == 'Quarry':
                    point_building = 'Mason'
                elif self.economy == 'Metalworks':
                    point_building = 'Blacksmith'
                elif self.economy == 'Lumber':
                    point_building = 'Lumbermill'
                elif self.economy == 'Church':
                    point_building = 'Cathedral'
                elif self.economy == 'Textile':
                    point_building = 'Weavery'
                elif self.economy == 'Colosseum':
                    point_building = 'Colosseum'
                elif self.economy == 'Mine':
                    point_building = 'Mine'
                else:
                    point_building = 'none'
                    self.logger.warning('Set building to {0} because town.economy {1} is not recognized.'
                                   .format(point_building, self.economy))
            else:
                num_points = 0
                point_building = 'none'
                self.logger.warning('Set building to {0}, building type not recognized.'
                               .format(point_building))

            # Get start point for special building
            placed = False
            while(not placed):
                rand_idx = random.randint(0, len(block.points) - 1)
                start_point = block.points[rand_idx]

                if self.pointGoodToUse(start_point, block):
                    placed = True

            # print('1', self.map_points[start_point.y][start_point.x])
            self.map_points[start_point.y][start_point.x] = Building(point_building,
                                                                     start_point.x,
                                                                     start_point.y)

            if (point_building == 'Barn' or point_building == 'Barracks' or
                point_building == 'Mason' or point_building == 'Blacksmith' or
                point_building == 'Lumbermill' or point_building == 'Cathedral' or
                point_building == 'Weavery' or point_building == 'Colosseum' or
                point_building == 'Mine'):
                self.addToBuildingPoints('Special', start_point)
            else:
                self.addToBuildingPoints(point_building, start_point)

            for i in range(num_points - 1):
                placed = False
                point_num = 0
                while(not placed):
                    point = self.getNewPoint(start_point, point_num)
                    if self.pointGoodToUse(point, block):
                        placed = True

                    point_num = point_num + 1

                # print('2', self.map_points[point.y][point.x])
                self.map_points[point.y][point.x] = Building(point_building,
                                                             point.x, point.y)

                if (point_building == 'Barn' or point_building == 'Barracks' or
                    point_building == 'Mason' or point_building == 'Blacksmith' or
                    point_building == 'Lumbermill' or point_building == 'Cathedral' or
                    point_building == 'Weavery' or point_building == 'Colosseum' or
                    point_building == 'Mine'):
                    self.addToBuildingPoints('Special', point)
                else:
                    self.addToBuildingPoints(point_building, point)

        # Placing housing
        for i, block in enumerate(self.block_list):
            placed = False
            while not placed:
                begin = block.points[random.randint(0, len(block.points) - 1)]
                # print('3', self.map_points[begin.y][begin.x])
                if self.pointGoodToUse(begin, block):
                    self.map_points[begin.y][begin.x] = Building(block.wealth, begin.x, begin.y)
                    point = begin
                    placed = True

            for j in range(int(house_per_block[block.wealth]) - 1):
                point = self.placePoint(point, begin, block)

        # print(self.number_noble_house)
        if self.noble_blocks == 0:
            if self.number_noble_house != 0:
                # print('Placing {} extra noble houses that don\'t belong to a block.'.format(self.number_noble_house))
                placed = 0
                while placed < self.number_noble_house:
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)

                    if self.map_points[y][x].building_type == 'none':
                        # print('4', self.map_points[y][x])
                        self.map_points[y][x] = Building('NobleHouse', x, y)
                        self.noble_houses.append(self.map_points[y][x])
                        placed = placed + 1

    def placePoint(self, current, begin, block):
        up = Point(current.x, current.y + 1)
        lf = Point(current.x - 1, current.y)
        dn = Point(current.x, current.y - 1)
        rt = Point(current.x + 1, current.y)

        if self.pointGoodToUse(up, block):
            place = up

        elif self.pointGoodToUse(lf, block):
            place = lf

        elif self.pointGoodToUse(dn, block):
            place = dn

        elif self.pointGoodToUse(rt, block):
            place = rt

        else:
            moved_current = False
            iteration = 0

            while(not moved_current):
                if iteration > 100:
                    return current

                point = block.points[random.randint(0, len(block.points) - 1)]

                if self.pointGoodToUse(point, block):
                    place = current = point
                    moved_current = True

                iteration = iteration + 1

        # print('5', self.map_points[place.y][place.x])
        self.map_points[place.y][place.x] = Building(block.wealth, place.x,
                                                     place.y)

        if block.wealth == 'NobleHouse':
            self.placed_nobles = self.placed_nobles + 1
            self.noble_houses.append(self.map_points[place.y][place.x])
        elif block.wealth == 'MiddleHouse':
            self.placed_middle = self.placed_middle + 1
            self.middle_houses.append(self.map_points[place.y][place.x])
        elif block.wealth == 'PoorHouse':
            self.placed_poor = self.placed_poor + 1
            self.poor_houses.append(self.map_points[place.y][place.x])

        return current

    def placeRoads(self):
        for point in self.map_points:
            for h_slope, h_int in zip(self.horizontal_roads_m, self.horizontal_roads_b):
                if (point.y == int(point.x * h_slope + h_int)):
                    point.building = 'Road'
                    break

            else:
                for v_slope, v_int in zip(self.vertical_roads_m, self.vertical_roads_b):
                    if (point.x == int((point.y - v_int) / v_slope)):
                        point.building = 'Road'
                        break

    def pointGoodToUse(self, point, block):
        try:
            if self.map_points[point.y][point.x].building_type == 'none':
                return True
            else:
                return False
        except:
            print('({}, {}) not a valid point in map_points.'.format(point.x,
                                                                     point.y))
            return False

    def printMapCorners(self):
        text = ''
        for y, row in enumerate(self.map_points):
            for x, building in enumerate(row):
                text = text + '[ref={0} {1}]{2}[/ref]'.format(x, y, building.__str__())

            text = text + '\n'

        return text

