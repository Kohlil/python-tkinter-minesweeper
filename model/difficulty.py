from enum import Enum

class Difficulty(Enum):
    BEGINNER = (8, 8, 10, 6, 5, 2)
    INTERMEDIATE = (16, 16, 40, 11, 4, 2)
    EXPERT = (30, 16, 99, 41, 3, 2)

    @property
    def x_size(self):
        return self.value[0]

    @property
    def y_size(self):
        return self.value[1]

    @property
    def max_mines(self):
        return self.value[2]

    @property
    def min_mines(self):
        return self.value[3]

    @property
    def max_treasures(self):
        return self.value[4]

    @property
    def min_treasures(self):
        return self.value[5]
