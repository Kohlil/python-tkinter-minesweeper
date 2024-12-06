import random
from model.difficulty import Difficulty
from model.cell import Cell, CellType
from shared.utility import Utility
from datetime import datetime
import csv


class Board:

    def __init__(self, difficulty: Difficulty):
        self.dif = difficulty
        self.restart()
        
    def setup(self):
        # create flag and clicked tile variables
        self.flag_count = 0
        self.correct_flag_count = 0
        self.clicked_count = 0
        self.start_time = None

        # Create initial board
        self.place_items()
        self.count_mines_treasures()
        
    def restart(self):
        self.setup()
            
    def reveal_cell(self, x, y):
        """Reveals a cell on the board and updates the game state."""
        self.update_timer()
            
        self.clicked_count += 1
        cell: Cell = self.tiles[x][y]
        
        # Can't click mine on first click so move to random location until empty spot is found
        if self.clicked_count == 1 and cell.type == CellType.MINE:
            self.move_mine(x, y)
        
        if cell.is_checked or cell.is_flagged:
            return  None # Do nothing if the cell is already checked or flagged

        cell.is_checked = True

        if cell.type == CellType.MINE:
            # End game if the revealed cell is a mine
            return self.game_over(won=False)

        if cell.type == CellType.TREASURE:
            # End game with a win if a treasure is revealed
            return self.game_over(won=True)

        if cell.nearby_mines == 0 and cell.nearby_treasures == 0:
            # If no nearby mines, recursively reveal neighbors
            for neighbor in self.get_neighbors(x, y):
                if not neighbor.is_checked:
                    self.reveal_cell(neighbor.x, neighbor.y)

        # Check if all safe cells are revealed
        if self._all_safe_cells_revealed():
            return self.game_over(won=True)

    def toggle_flag(self, x, y):
        """Toggles the flagged state of a cell."""
        cell: Cell = self.tiles[x][y]

        if cell.is_checked:
            return  None # Do nothing if the cell is already revealed

        if cell.is_flagged:
            # Unflag the cell
            cell.is_flagged = False
            self.flag_count -= 1
            if cell.type == CellType.MINE:
                self.correct_flag_count -= 1
        else:
            # Flag the cell
            cell.is_flagged = True
            self.flag_count += 1
            if cell.type == CellType.MINE:
                self.correct_flag_count += 1

        # Update game state based on flags
        if self.correct_flag_count == self.actual_mines and self.flag_count == self.actual_mines:
            return self.game_over(won=True)

    def _all_safe_cells_revealed(self):
        """Checks if all non-mine and non-treasure cells are revealed."""
        for row in self.tiles:
            for cell in row:
                if cell.type == CellType.EMPTY and not cell.is_checked:
                    return False
        return True

            
    def game_over(self, won: bool):
        """Ends the game and sets the final state."""
        self.is_running = False  # Stop the timer
        self.reveal_all_tiles()  # Reveal all tiles on the board
        return won

    def reveal_all_tiles(self):
        """Reveals all tiles on the board."""
        for row in self.tiles:
            for cell in row:
                cell.is_checked = True  # Reveal all cells

    def get_neighbors(self, x, y):
        """Returns a list of neighboring cells around the given coordinates."""
        neighbors = []
        coords = [
            (x - 1, y - 1),  # top left
            (x - 1, y),      # top middle
            (x - 1, y + 1),  # top right
            (x, y - 1),      # left
            (x, y + 1),      # right
            (x + 1, y - 1),  # bottom left
            (x + 1, y),      # bottom middle
            (x + 1, y + 1),  # bottom right
        ]
        for nx, ny in coords:
            if 0 <= nx < self.dif.x_size and 0 <= ny < self.dif.y_size:
                neighbors.append(self.tiles[nx][ny])
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

    def count_mines_treasures(self):
        # loop to find nearby mines and display number on tile
        for x in range(0, self.dif.x_size):
            for y in range(0, self.dif.y_size):
                mc = 0
                tc = 0
                n: Cell
                for n in self.get_neighbors(x, y):
                    mc += 1 if n.type == CellType.MINE else 0
                    tc += 1 if n.type == CellType.TREASURE else 0
                self.tiles[x][y].nearby_mines = mc
                self.tiles[x][y].nearby_treasures = tc

    def update_timer(self):
        ts = "00:00:00"
        if self.start_time != None:
            delta = datetime.now() - self.start_time
            ts = str(delta).split(".")[0]  # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # zero-pad
        else:
            self.start_time = datetime.now()
        return ts
    
    def move_mine(self, mine_x, mine_y):
        """Moves a mine from the given coordinates to a random empty spot."""
        # Validate the starting position
        if self.tiles[mine_x][mine_y].type != CellType.MINE:
            raise ValueError("The specified starting cell does not contain a mine.")

        # Find all empty spots
        empty_spots = [
            (x, y)
            for x in range(self.dif.x_size)
            for y in range(self.dif.y_size)
            if self.tiles[x][y].type == CellType.EMPTY
        ]

        if not empty_spots:
            raise ValueError("No empty spots available to move the mine.")

        # Randomly select an empty spot
        new_x, new_y = random.choice(empty_spots)

        # Move the mine
        self.tiles[mine_x][mine_y].type = CellType.EMPTY  # Remove mine from the old spot
        self.tiles[new_x][new_y].type = CellType.MINE  # Place mine in the new spot

        # Recalculate mine counts
        self.count_mines_treasures()

        # Return the new position of the mine
        return new_x, new_y

    def load_board_from_csv(self, file_path: str):
        """
        Loads a Minesweeper board from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
        
        Raises:
            ValueError: If the CSV file format is invalid.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

            # Validate the CSV dimensions
            if len(rows) != self.dif.x_size or any(len(row) != self.dif.y_size for row in rows):
                raise ValueError("CSV dimensions do not match the board size.")

            # Initialize the tiles based on the CSV content
            self.tiles = []
            for x, row in enumerate(rows):
                self.tiles.append([])
                for y, value in enumerate(row):
                    if value == "0":
                        cell_type = CellType.EMPTY
                    elif value == "1":
                        cell_type = CellType.MINE
                    elif value == "2":
                        cell_type = CellType.TREASURE
                    else:
                        raise ValueError(f"Invalid cell type '{value}' in CSV at ({x}, {y}).")
                    
                    self.tiles[x].append(Cell(cell_type, x, y))

            # Recalculate mine counts
            self.count_mines_treasures()

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except csv.Error as e:
            raise ValueError(f"Error reading CSV file: {e}")

