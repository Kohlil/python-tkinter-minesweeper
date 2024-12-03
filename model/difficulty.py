from enum import Enum

class DifficultyData:
    def __init__(self, x_size: int, y_size: int, max_mines: int, min_mines: int, max_treasures: int, min_treasures):
        self.x_size = x_size # num columns
        self.y_size = y_size # num rows
        self.max_mines = max_mines
        self.min_mines = min_mines
        self.max_treasures = max_treasures
        self.min_treasures = min_treasures

class Difficulty(Enum):
    BEGINNER = DifficultyData(8, 8, 10, 1, 5, 2)
    INTERMEDIATE = DifficultyData(16, 16, 40, 11, 4, 2)
    EXPERT = DifficultyData(30, 16, 99, 41, 3, 2)