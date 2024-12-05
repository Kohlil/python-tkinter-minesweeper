from model.difficulty import Difficulty
from model.cell import Cell, CellType
from model.utility import Utility
import datetime


class Board:

    def __init__(self, difficulty: Difficulty):
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
        
    def handle_update(self, x: int, y: int):
        if self.startTime == None:
            self.startTime = datetime.now()
        
        tile = self.tiles[x][y]

        if tile.type == CellType.MINE:
            # end game
            self.game_over(won=False)
            return

        # change image
        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
        # if not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (self.X_SIZE * self.Y_SIZE) - self.mines:
            self.game_over(won=False)
            
    def game_over(self, won: bool):
        pass

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
            except IndexError:
                pass
        return neighbors

    def place_items(self):
        # Create initial board
        self.tiles: list[list[Cell]] = []
        self.actual_mines = 0

        # Randomly place mines / treasures from min up to max
        mines = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size), self.dif.min_mines, self.dif.max_mines
        )
        treasures = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size),
            self.dif.min_treasures,
            self.dif.max_treasures,
        )
        for x in range(0, self.dif.x_size):
            for y in range(0, self.dif.y_size):
                if y == 0:
                    self.tiles.append([])

                # Set cell type
                cell_type = CellType.EMPTY
                if treasures[x][y] == 1:
                    cell_type = CellType.TREASURE
                elif mines[x][y] == 1:
                    cell_type = CellType.MINE
                    self.actual_mines += 1

                tile = Cell(cell_type, x, y)
                self.tiles[x].append(tile)

    def count_mines(self):
        # loop to find nearby mines and display number on tile
        for x in range(0, self.dif.x_size):
            for y in range(0, self.dif.y_size):
                mc = 0
                n: Cell
                for n in self.get_neighbors(x, y):
                    mc += 1 if n.type == CellType.MINE else 0
                self.tiles[x][y].nearby_mines = mc

    def update_timer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split(".")[0]  # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # zero-pad
        return ts
