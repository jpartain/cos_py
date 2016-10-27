from include.building import Building
from include.block import Block

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


class Town:
    def __init__(self, seed):
        self.generatePopulation(seed[0])
        self.generateWealth(seed[1])
        self.generateEconomy(seed[2])
        self.generateDanger(seed[3])
        self.generateNobility(seed[4])
        self.generateHomeless(seed[5])

        self.buildMap()
        # self.generateMap(seed[6:25])

        self.generateBuildingRatios()
        self.getStreetBlocks()

        # self.createRoadsEquations(seed[25:126])

        # self.placeRoads()
        self.fillStreetBlocks(seed[6:6 + 16])
        self.placeBuildings(seed[22:22 + 16*2])

    def buildMap(self):
        self.height = 25
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
                if (x == int(width/2)) or (y == int(height/2)):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                if (x == int(width/4)) or (y == int(height/4)):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                if (x == int(3*width/4)) or (y == int(3*height/4)):
                    building.building_type = 'Road'
                    self.road_area = self.road_area + 1

                self.map_points[y][x] = building

    def createOpinions(self, string):
        pass

    def createPerson(self, string):
        pass

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

    def fillStreetBlocks(self, string):
        types_for_use = self.getAvailableBlocks()

        for i, block in enumerate(self.block_list):
            rand_select = int((len(types_for_use) - 1) * int(string[i])/9)
            block.wealth = types_for_use.pop(rand_select)

    def generateBuildingRatios(self):
        area_mod = self.wealth / 25
        map_unit_area = 5256

        self.tavern_area =      30  * (1 + area_mod) * (self.map_area/map_unit_area)
        self.plumbing_area =    20  * (1 + area_mod) * (self.map_area/map_unit_area)
        self.market_area =      100 * (1 + area_mod) * (self.map_area/map_unit_area)
        self.trade_area =       60  * (1 + area_mod) * (self.map_area/map_unit_area)
        self.inn_area =         30  * (1 + area_mod) * (self.map_area/map_unit_area)
        self.special_area =     100 * (1 + area_mod) * (self.map_area/map_unit_area)
        self.empty_area =       20 * (self.map_area/map_unit_area)

        housing_area =  int(self.map_area - self.tavern_area - self.plumbing_area -
                            self.market_area - self.trade_area - self.inn_area -
                            self.special_area - self.road_area -
                            self.empty_area)

        self.number_noble_house =  int(housing_area * (0.2 + self.wealth/25))
        self.number_middle_house = int(housing_area * (0.4 + self.wealth/25))
        self.number_poor_house =   (housing_area - self.number_noble_house -
                                    self.number_middle_house)

        """
        print()
        print('Noble area:\t', self.number_noble_house, '\t',
              int(self.number_noble_house/housing_area * 100), '%')

        print('Middle area:\t', self.number_middle_house, '\t',
              int(self.number_middle_house/housing_area * 100), '%')

        print('Poor area:\t', self.number_poor_house, '\t',
              int(self.number_poor_house/housing_area * 100), '%')
        print()
        """

    def generatePopulation(self, seed):
        pass

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

    def generateHomeless(self, string):
        self.settled_ratio = int(10*(int(string)/6 + self.wealth/2 + 7))

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
                                    print('ERROR: Unhandled draw_slope[] value')
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
                                    print('ERROR: Unhandled draw_slope[] value')
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
                                    print('ERROR: Unhandled draw_slope[] value')
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
                                    print('ERROR: Unhandled draw_slope[] value')
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

    def generateNobility(self, string):
        if self.economy == 'Church':
            self.nobility_mod = 0.5
        elif self.economy == 'Military':
            self.nobility_mod = 0.4
        else:
            self.nobility_mod = 0.35

        self.nobility = int(10*self.nobility_mod*int(string))

    def generateWealth(self, string):
        self.wealth = int(string) - 5

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

    def linkRelationships(self, string):
        pass

    def placeBuildings(self, string):
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

        for i, block in enumerate(self.block_list):
            begin_x = int(((block.bot_right_x - block.top_left_x) *
                          int(string[2*i])/9 + block.top_left_x))
            begin_y = int(((block.bot_right_y - block.top_left_y) *
                          int(string[2*i + 1])/9 + block.top_left_y))

            self.map_points[begin_y][begin_x] = Building(block.wealth)
            point_x = begin_x
            point_y = begin_y

            for j in range(int(house_per_block[block.wealth]) - 1):
                if self.pointGoodToUse(point_y + 1, point_x, block):
                    point_y = point_y + 1

                elif self.pointGoodToUse(point_y, point_x - 1, block):
                    point_x = point_x - 1

                elif self.pointGoodToUse(point_y - 1, point_x, block):
                    point_y = point_y - 1

                elif self.pointGoodToUse(point_y, point_x + 1, block):
                    point_x = point_x + 1

                else:
                    print('Didn\'t place a building on a map point!')
                    continue

                self.map_points[point_y][point_x] = Building(block.wealth)

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
        # print('Map corner points:')
        # print(self.draw_order[0], self.draw_order[1],
        #       self.draw_order[2], self.draw_order[3])

        # print('\nMap perimeter segment endpoints:')
        # print(self.draw_segs)

        # print('\nMap perimeter segment slopes:')
        # print(self.draw_slopes)

        # print('\nMap size modifier:', self.map_size_mod)

        # print('\nMap corners modifiers:')
        # print(self.map_corners_mod)

        print('\nMap area: ', self.map_area)

        # print('\nMap points: ', self.map_points)

        print('\nMap Visualization:')
        for row in self.map_points:
            for building in row:
                print(building, end = '')

            print()

        print()


class MapPoint:
    def __init__(self):
        self.building = '*'

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
