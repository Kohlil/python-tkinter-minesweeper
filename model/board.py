from difficulty import DifficultyData
from cell import Cell, CellType
from utility import Utility
import datetime


class Board:

    def __init__(self, difficulty: DifficultyData):
        self.dif = difficulty
        self.restart()
        
    def setup(self):
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        # Create initial board
        self.place_items()
        self.count_mines()
        
    def restart(self):
        self.setup()

    def get_neighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x - 1, "y": y - 1},  # top right
            {"x": x - 1, "y": y},  # top middle
            {"x": x - 1, "y": y + 1},  # top left
            {"x": x, "y": y - 1},  # left
            {"x": x, "y": y + 1},  # right
            {"x": x + 1, "y": y - 1},  # bottom right
            {"x": x + 1, "y": y},  # bottom middle
            {"x": x + 1, "y": y + 1},  # bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def place_items(self):
        # Create initial board
        self.tiles: list[list[Cell]] = []
        self.actual_mines = 0

        # Randomly place mines / treasures from min up to max
        mines = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size), self.dif.max_mines, self.dif.min_mines
        )
        treasures = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size),
            self.dif.max_treasures,
            self.dif.min_treasures,
        )
        for x in range(0, self.dif.x_size):
            for y in range(0, self.dif.y_size):
                if y == 0:
                    self.tiles[x] = []

                # Set cell type
                cell_type = CellType.EMPTY
                if treasures[x][y] == 1:
                    cell_type = CellType.TREASURE
                elif mines[x][y] == 1:
                    cell_type = CellType.MINE
                    mines += 1

                tile = Cell(cell_type)
                self.tiles[x][y] = tile

    def count_mines(self):
        # loop to find nearby mines and display number on tile
        for x in range(0, self.dif.x_size):
            for y in range(0, self.dif.y_size):
                mc = 0
                n: Cell
                for n in self.get_neighbors(x, y):
                    if n.type == CellType.MINE:
                        mc += 1 if n else 0
                self.tiles[x][y].nearby_mines(mc)

    def update_timer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split(".")[0]  # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # zero-pad
        return ts
