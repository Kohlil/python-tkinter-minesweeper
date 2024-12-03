from enum import Enum

class DifficultyData:
    def __init__(self, x_size: int, y_size: int, max_mines: int, max_treasures: int, min_treasures):
        self.x_size = x_size
        self.y_size = y_size
        self.mines = mines
        self.treasures = treasures

class Difficulty(Enum):
    BEGINNER = DifficultyData(8, 8, 10, 5, 2)
    INTERMEDIATE = DifficultyData(16, 16, 40, 4, 2)
    EXPERT = DifficultyData(30, 16, 99, 3, 2)