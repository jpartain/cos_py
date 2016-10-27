class Block:
    def __init__(self, top_left_x, top_left_y, bot_right_x, bot_right_y):
        self.wealth = 'none'

        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bot_right_x = bot_right_x
        self.bot_right_y = bot_right_y

        height = bot_right_y - top_left_y
        width = bot_right_x - top_left_x

        self.buildings = [[0 for x in range(width)] for y in range(height)]


    def __str__(self):
        return ('Top left:\t({0}, {1})\t\tBot right:\t({2}, {3})'.
                format(self.top_left_x, self.top_left_y,
                       self.bot_right_x, self.bot_right_y))

    def __repr__(self):
        return ('Top left:\t({0}, {1})\t\tBot right:\t({2}, {3})'.
                format(self.top_left_x, self.top_left_y,
                       self.bot_right_x, self.bot_right_y))
