from model.difficulty import Difficulty
from model.cell import Cell, CellType
from shared.utility import Utility
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
            
    def reveal_cell(self, x, y):
        """Reveals a cell on the board and updates the game state."""
        self.update_timer()
            
        
        cell = self.tiles[x][y]
        if cell.is_checked or cell.is_flagged:
            return  # Do nothing if the cell is already checked or flagged

        cell.is_checked = True

        if cell.type == CellType.MINE:
            # End game if the revealed cell is a mine
            self.game_over(won=False)
            return

        if cell.type == CellType.TREASURE:
            # End game with a win if a treasure is revealed
            self.game_over(won=True)
            return

        if cell.nearby_mines == 0:
            # If no nearby mines, recursively reveal neighbors
            for neighbor in self.get_neighbors(x, y):
                if not neighbor.is_checked:
                    self.reveal_cell(neighbor.x, neighbor.y)

        # Check if all safe cells are revealed
        if self._all_safe_cells_revealed():
            self.game_over(won=True)

    def toggle_flag(self, x, y):
        """Toggles the flagged state of a cell."""
        cell: Cell = self.tiles[x][y]

        if cell.is_checked:
            return  # Do nothing if the cell is already revealed

        if cell.is_flagged:
            # Unflag the cell
            cell.is_flagged = False
            self.flagCount -= 1
            if cell.type == CellType.MINE:
                self.correctFlagCount -= 1
        else:
            # Flag the cell
            cell.is_flagged = True
            self.flagCount += 1
            if cell.type == CellType.MINE:
                self.correctFlagCount += 1

        # Update game state based on flags
        if self.correctFlagCount == self.actual_mines and self.flagCount == self.actual_mines:
            self.game_over(won=True)

    def _all_safe_cells_revealed(self):
        """Checks if all non-mine and non-treasure cells are revealed."""
        for row in self.tiles:
            for cell in row:
                if cell.type == CellType.EMPTY and not cell.is_checked:
                    return False
        return True

            
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
        else:
            self.startTime = datetime.now()
        return ts
