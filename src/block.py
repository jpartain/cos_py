class Block:
    def __init__(self, top_left_x, top_left_y, bot_right_x, bot_right_y):
        self.wealth = 'none'

        self.points = []
        self.tlx = top_left_x
        self.tly = top_left_y
        self.brx = bot_right_x
        self.bry = bot_right_y

        # print('Points in block:')
        for x in range(top_left_x, bot_right_x + 1):
            for y in range(top_left_y, bot_right_y + 1):
                # print('({}, {}) '.format(x, y), end = '')
                self.points.append(Point(x, y))

        # print()

    def __str__(self):
        return ('Top left:\t({0}, {1})\t\tBot right:\t({2}, {3})'.
                format(self.top_left_x, self.top_left_y,
                       self.bot_right_x, self.bot_right_y))

    def __repr__(self):
        return ('Top left:\t({0}, {1})\t\tBot right:\t({2}, {3})'.
                format(self.top_left_x, self.top_left_y,
                       self.bot_right_x, self.bot_right_y))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
