import logging

from building import Building
from block import Block
import seed
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


class Town:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.population = 0
        self.createPointPlacementRadius()

        self.generateWealth()
        self.generateEconomy()
        self.generateDanger()
        self.generateNobility()
        self.generateHomeless()
        self.buildMap()
        # self.generateMap(seed[6:25])
        self.generateBuildingRatios()
        self.getStreetBlocks()
        # self.createRoadsEquations(seed[25:126])
        # self.placeRoads()
        self.fillStreetBlocks()
        self.placeBuildings()
        self.createPopulation()

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

            if seed.getRand() > 4:
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

            if seed.getRand() > 4:
                mid.age = 'Adult'
            else:
                mid.age = 'YoungAdult'

            if seed.getRand() > 4:
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

            dice_roll = seed.getRand()
            if dice_roll > 6:
                yng.age = 'Teenager'
            elif dice_roll > 3:
                yng.age = 'Child'
            else:
                yng.age = 'Baby'

            if seed.getRand() > 4:
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
        self.height = 40
        self.width = 40
        self.road_area = 0

        height = self.height
        width = self.width

        self.map_points = [[Building('none') for i in range(width)] for j in range(height)]
        self.map_area = height * width

        for y, row in enumerate(self.map_points):
            for x, cell in enumerate(row):
                building = Building('none')

                # Place roads on map edge
                if (x == 0) or (x == width - 1) or (y == 0) or (y == height - 1):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                # A couple simple straight roads
                if (x == int(width/3)) or (y == int(height/3)):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                if (x == int(2*width/3)) or (y == int(2*height/3)):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                self.map_points[y][x] = building

    def createFamily(self, wealth):
        family = []
        family_name = person.createFamilyName()
        family_size = seed.getRand() + 1

        self.increasePopulation(family_size)
        unpruned_family_list = self.buildFamilyTree(family_name, wealth)

        serial_family_list = (unpruned_family_list[0] + unpruned_family_list[1]
                              + unpruned_family_list[2])

        for i in range(family_size):
            length = len(serial_family_list) - 1
            rand = seed.getRand() * seed.getRand()
            max_rand = 81

            family.append(serial_family_list.pop(int(rand / max_rand *
                                                     length)))

        # Assemble relations_in_house
        for dude in family:
            for i, other_dude in enumerate(dude.relation_persons):
                if other_dude in family:
                    dude.relation_persons_in_house.append(other_dude)
                    dude.relations_in_house.append(dude.relations[i])

        # self.logger.debug('Family - {}'.format(family_name))
        # for dude in family:
            # print('Name - {0} - {1}'.format(dude, dude.age))

        return family

    def createOpinions(self, string):
        pass

    def createPopulation(self):
        for house in self.noble_houses:
            family = self.createFamily('noble')
            self.map_points[house.y][house.x].people = family

        for house in self.middle_houses:
            family = self.createFamily('middle')
            self.map_points[house.y][house.x].people = family

        for house in self.poor_houses:
            family = self.createFamily('poor')
            self.map_points[house.y][house.x].people = family

    def createPointPlacementRadius(self):
        self.placement_radius = []

        for r in range(0, 101):
            x = r
            y = 0
            err = 0

            while x >= y:
                self.placement_radius.append([x, y])
                self.placement_radius.append([y, x])
                self.placement_radius.append([-y, x])
                self.placement_radius.append([-x, y])
                self.placement_radius.append([-x, -y])
                self.placement_radius.append([-y, -x])
                self.placement_radius.append([y, -x])
                self.placement_radius.append([x, -y])

                y = y + 1
                err = err + 1 + 2*y
                if (2*(err - x) + 1) > 0:
                    x = x - 1
                    err = err + 1 - 2*x

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
            rand_select = int((len(types_for_use) - 1) * int(seed.getRand())/9)
            block.wealth = types_for_use.pop(rand_select)

    def generateBuildingRatios(self):
        area_mod = self.wealth / 25
        map_unit_area = 5256

        self.tavern_area =   int(30  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.plumbing_area = int(20  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.market_area =   int(100 * (1 + area_mod) * (self.map_area/map_unit_area))
        self.trade_area =    int(60  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.inn_area =      int(30  * (1 + area_mod) * (self.map_area/map_unit_area))
        self.special_area =  int(100 * (1 + area_mod) * (self.map_area/map_unit_area))
        self.empty_area =    int(20 * (self.map_area/map_unit_area))

        free_area =  int(self.map_area - self.tavern_area - self.plumbing_area -
                         self.market_area - self.trade_area - self.inn_area -
                         self.special_area - self.road_area - self.empty_area)

        self.number_noble_house =  int(free_area * (0.05 + self.wealth/100))
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
        dice_roll = seed.getRand()
        if dice_roll == 9:
            dice_roll = 5

        self.economy = TownEconomy[dice_roll]

    def generateDanger(self):
        if self.economy == 'Military':
            self.danger_mod = 0.4
        elif self.economy == 'Church':
            self.danger_mod = 0.6
        elif self.economy == 'Colosseum':
            self.danger_mod = 0.6
        else:
            self.danger_mod = 1

        self.danger = int(self.danger_mod*int(seed.getRand()))

    def generateHomeless(self):
        self.settled_ratio = int(10*(int(seed.getRand())/6 + self.wealth/2 + 7))

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

        self.nobility = int(10*self.nobility_mod*int(seed.getRand()))

    def generateWealth(self):
        self.wealth = int(seed.getRand()) - 5

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

    def getNewPoint(self, start_y, start_x, i):
        move_x = self.placement_radius[i][0]
        move_y = self.placement_radius[i][1]

        return start_y + move_y, start_x + move_x

    def getStreetBlocks(self):
        self.block_list = []

        height = self.height
        width = self.width

        for j in range(4):
            for i in range(4):
                top_left_x  = int(i*width/4)        + 1
                top_left_y  = int(j*height/4)       + 1
                bot_right_x = int((i + 1)*width/4)  - 1
                bot_right_y = int((j + 1)*height/4) - 1

                block = Block(top_left_x, top_left_y, bot_right_x, bot_right_y)
                self.block_list.append(block)

    def increasePopulation(self, num):
        self.population = self.population + num

    def linkFamilyRelations(self, family):
        possible_indices = [i for i in range(10)]
        pair = []
        num_old_relations = 5

        # Old person marriages
        for i in range(num_old_relations * 2):
            pair.append(possible_indices.pop(int(seed.getRand() / 9 *
                                                 (len(possible_indices) - 1))))

            if i % 2 != 0:
                if seed.getRand() > 3:
                    l_person = family[0][pair[0]]
                    r_person = family[0][pair[1]]

                    l_person.addRelation(r_person, 'Spouse')
                    r_person.addRelation(l_person, 'Spouse')
                    # print(r_person, l_person, ' - Old Spouses')

                pair.pop()
                pair.pop()

        possible_indices = [i for i in range(15)]
        possible_old_indices = [i for i in range(10)]
        num_mid_to_old_relations = 15

        # Father/Mother -> Son/Daughter from Old to Mid
        for i in range(num_mid_to_old_relations):
            # Mid generation person
            first = possible_indices.pop(int(seed.getRand() / 9 *
                                             (len(possible_indices) - 1)))
            # Old person
            second = possible_old_indices[int(seed.getRand() / 9 *
                                              (len(possible_old_indices) - 1))]
            if seed.getRand() > 4:
                l_person = family[1][first]
                r_person = family[0][second]

                l_relation_type = 'Child'
                r_relation_type = 'Parent'

                l_person.addRelation(r_person, r_relation_type)
                r_person.addRelation(l_person, l_relation_type)
                # print(l_person, r_person, ' - Child -> Parent')

        # Link shared children
        for old in family[0]:
            if 'Spouse' in old.relations:
                spouse = old.relation_persons[old.relations.index('Spouse')]

                for i, relation in enumerate(old.relations):
                    if relation != 'Spouse':
                        child = old.relation_persons[i]

                        if not spouse.alreadyHasRelation(child):
                            spouse.addRelation(child, relation)
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
            if seed.getRand() > 2:
                try:
                    pair = r_spouses.pop(int(seed.getRand() / 9 *
                                                    (len(r_spouses) - 1)))
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
        num_yng_to_mid_relations = 15

        # Father/Mother -> Son/Daughter from Mid to Yng
        for i in range(num_yng_to_mid_relations):
            # Yng generation person
            first = possible_yng_indices.pop(int(seed.getRand() / 9 *
                                                 (len(possible_yng_indices) - 1)))
            # Mid person
            second = possible_mid_indices[int(seed.getRand() / 9 *
                                              (len(possible_mid_indices) - 1))]
            if seed.getRand() > 4:
                l_person = family[2][first]
                r_person = family[1][second]

                l_relation_type = 'Child'
                r_relation_type = 'Parent'

                l_person.addRelation(r_person, r_relation_type)
                r_person.addRelation(l_person, l_relation_type)
                # print(l_person, r_person, ' - Child -> Parent')

        # Link shared children
        for mid in family[1]:
            if 'Spouse' in mid.relations:
                spouse = mid.relation_persons[mid.relations.index('Spouse')]

                for i, relation in enumerate(mid.relations):
                    if relation != 'Spouse':
                        child = mid.relation_persons[i]

                        if not spouse.alreadyHasRelation(child):
                            if seed.getRand() > 2:
                                spouse.addRelation(child, relation)
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
            new_idx = int(seed.getRand()/9 * len(self.block_list) - 1)
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
                else:
                    point_building = 'none'
                    self.logger.warning('Set building to {0} because town.economy {1} is not recognized.'
                                   .format(point_building, self.economy))
                num_points = self.special_area
            else:
                num_points = 0
                point_building = 'none'
                self.logger.warning('Set building to {0}, building type not recognized.'
                               .format(point_building))

            # Get start point for special building
            placed = False
            while(not placed):
                start_x = int((block.bot_right_x - block.top_left_x) *
                            int(seed.getRand())/10 + block.top_left_x)
                start_y = int((block.bot_right_y - block.top_left_y) *
                            int(seed.getRand())/10 + block.top_left_y)

                if self.pointGoodToUse(start_y, start_x, block):
                    placed = True

            self.map_points[start_y][start_x] = Building(point_building)

            for i in range(num_points - 1):
                placed = False
                point_num = 0
                while(not placed):
                    point_y, point_x = self.getNewPoint(start_y, start_x, point_num)
                    if self.pointGoodToUse(point_y, point_x, block):
                        placed = True

                    point_num = point_num + 1

                self.map_points[point_y][point_x] = Building(point_building)

        # Placing housing
        for i, block in enumerate(self.block_list):
            begin_x = int(((block.bot_right_x - block.top_left_x) *
                          int(seed.getRand())/10 + block.top_left_x))
            begin_y = int(((block.bot_right_y - block.top_left_y) *
                          int(seed.getRand())/10 + block.top_left_y))

            self.map_points[begin_y][begin_x] = Building(block.wealth)
            point_x = begin_x
            point_y = begin_y

            for j in range(int(house_per_block[block.wealth]) - 1):
                point_y, point_x = self.placePoint(point_y, point_x,
                                                   begin_y, begin_x, block)

    def placePoint(self, current_y, current_x, begin_x, begin_y, block):
        if self.pointGoodToUse(current_y + 1, current_x, block):
            place_x = current_x
            place_y = current_y + 1

        elif self.pointGoodToUse(current_y, current_x - 1, block):
            place_x = current_x - 1
            place_y = current_y

        elif self.pointGoodToUse(current_y - 1, current_x, block):
            place_x = current_x
            place_y = current_y - 1

        elif self.pointGoodToUse(current_y, current_x + 1, block):
            place_x = current_x + 1
            place_y = current_y

        else:
            moved_current = False
            iteration = 0

            while(not moved_current):
                if iteration > 100:
                    return current_y, current_x

                point_x = int((block.bot_right_x - block.top_left_x) *
                            int(seed.getRand())/10 + block.top_left_x)
                point_y = int((block.bot_right_y - block.top_left_y) *
                            int(seed.getRand())/10 + block.top_left_y)

                if self.pointGoodToUse(point_y, point_x, block):
                    place_y = current_y = point_y
                    place_x = current_x = point_x
                    moved_current = True

                iteration = iteration + 1

        self.map_points[place_y][place_x] = Building(block.wealth)

        if block.wealth == 'NobleHouse':
            self.placed_nobles = self.placed_nobles + 1
            self.noble_houses.append(MapPoint(place_x, place_y))
        elif block.wealth == 'MiddleHouse':
            self.placed_middle = self.placed_middle + 1
            self.middle_houses.append(MapPoint(place_x, place_y))
        elif block.wealth == 'PoorHouse':
            self.placed_poor = self.placed_poor + 1
            self.poor_houses.append(MapPoint(place_x, place_y))

        return current_y, current_x

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

    def pointGoodToUse(self, point_y, point_x, block):
        if ((block.top_left_y <= point_y) and (point_y <= block.bot_right_y) and
            (block.top_left_x <= point_x) and (point_x <= block.bot_right_x)):
            if self.map_points[point_y][point_x].building_type == 'none':
                return True
            else:
                return False
        else:
            return False

    def printMapCorners(self):
        text = ''
        for row in self.map_points:
            for building in row:
                text = text + building.__str__()

            text = text + '\n'

        return text


class MapPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
