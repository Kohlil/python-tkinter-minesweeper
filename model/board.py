import random
from model.difficulty import Difficulty
from model.cell import Cell, CellType
from shared.utility import Utility
from datetime import datetime
import csv
from icontract import require, ensure, invariant


@invariant(lambda self: 0 <= self.flag_count <= (self.dif.x_size * self.dif.y_size))
@invariant(lambda self: 0 <= self.correct_flag_count <= self.actual_mines)
class Board:
    """Represents the Minesweeper game board."""

    @require(lambda difficulty: isinstance(difficulty, Difficulty))
    def __init__(self, difficulty: Difficulty):
        """
        Initializes the Board with the given difficulty level.

        Args:
            difficulty (Difficulty): The difficulty settings of the game.
        """
        self.dif = difficulty
        self.restart()

    def setup(self):
        """
        Sets up the initial game state by initializing flags, counters,
        and the board layout with mines and treasures.
        """
        self.flag_count = 0
        self.correct_flag_count = 0
        self.clicked_count = 0
        self.start_time = None

        self.place_items()  # Distribute mines and treasures
        self.count_mines_treasures()  # Calculate nearby mines and treasures for each cell

    def restart(self):
        """
        Restarts the game by resetting the board and reinitializing the state.
        """
        self.setup()

    @require(lambda self, x, y: 0 <= x < self.dif.x_size and 0 <= y < self.dif.y_size)
    @ensure(lambda self, result: result in {None, True, False})
    def reveal_cell(self, x, y):
        """
        Reveals a cell on the board and updates the game state.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            bool: True if the game is won, False if lost, or None if the game continues.
        """
        self.update_timer()

        self.clicked_count += 1
        cell: Cell = self.tiles[x][y]

        # Handle the first click to ensure it's not on a mine
        if self.clicked_count == 1 and cell.type == CellType.MINE:
            self.move_mine(x, y)

        # Do nothing if the cell is already revealed or flagged
        if cell.is_checked or cell.is_flagged:
            return None

        cell.is_checked = True  # Mark the cell as revealed

        if cell.type == CellType.MINE:
            return self.game_over(won=False)  # Lose if it's a mine

        if cell.type == CellType.TREASURE:
            return self.game_over(won=True)  # Win if it's a treasure

        # If the cell is empty, reveal its neighbors recursively
        if cell.nearby_mines == 0 and cell.nearby_treasures == 0:
            for neighbor in self.get_neighbors(x, y):
                if not neighbor.is_checked:
                    self.reveal_cell(neighbor.x, neighbor.y)

        # Check if all safe cells have been revealed
        if self._all_safe_cells_revealed():
            return self.game_over(won=True)

    @require(lambda self, x, y: 0 <= x < self.dif.x_size and 0 <= y < self.dif.y_size)
    def toggle_flag(self, x, y):
        """
        Toggles the flagged state of a cell.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        """
        cell: Cell = self.tiles[x][y]

        # Do nothing if the cell is already revealed
        if cell.is_checked:
            return None

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

        # Win the game if all mines are correctly flagged
        if self.correct_flag_count == self.actual_mines and self.flag_count == self.actual_mines:
            return self.game_over(won=True)

    def _all_safe_cells_revealed(self):
        """
        Checks if all cells without mines or treasures have been revealed.

        Returns:
            bool: True if all safe cells are revealed, False otherwise.
        """
        return all(
            cell.type != CellType.EMPTY or cell.is_checked
            for row in self.tiles
            for cell in row
        )

    @ensure(lambda self, won: not self.is_running and won in {True, False})
    def game_over(self, won: bool):
        """
        Ends the game and reveals all tiles on the board.

        Args:
            won (bool): True if the player won, False otherwise.

        Returns:
            bool: The game's outcome (won or lost).
        """
        self.is_running = False  # Stop the timer
        self.reveal_all_tiles()  # Reveal all tiles for the final state
        return won

    def reveal_all_tiles(self):
        """
        Reveals all tiles on the board, typically when the game ends.
        """
        for row in self.tiles:
            for cell in row:
                cell.is_checked = True

    @require(lambda self, x, y: 0 <= x < self.dif.x_size and 0 <= y < self.dif.y_size)
    @ensure(lambda self, result: isinstance(result, list))
    def get_neighbors(self, x, y):
        """
        Retrieves a list of neighboring cells around the specified coordinates.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            list: A list of neighboring Cell objects.
        """
        neighbors = []
        coords = [
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1),               (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
        ]
        for nx, ny in coords:
            if 0 <= nx < self.dif.x_size and 0 <= ny < self.dif.y_size:
                neighbors.append(self.tiles[nx][ny])
        return neighbors

    @require(lambda self: self.dif.min_mines > self.dif.min_treasures,
            "Minimum number of mines must be greater than the minimum number of treasures.")
    @require(lambda self: self.dif.max_mines > self.dif.max_treasures,
            "Maximum number of mines must be greater than the maximum number of treasures.")
    @ensure(lambda self: self.dif.min_mines <= self.actual_mines <= self.dif.max_mines,
            "Number of mines placed must be within the specified range.")
    @ensure(lambda self: self.dif.min_treasures <= sum(cell.type == CellType.TREASURE for row in self.tiles for cell in row) <= self.dif.max_treasures,
            "Number of treasures placed must be within the specified range.")
    @ensure(lambda self: self.actual_mines > sum(cell.type == CellType.TREASURE for row in self.tiles for cell in row),
            "Number of mines must always be greater than the number of treasures.")
    def place_items(self):
        """
        Randomly places mines and treasures on the board and initializes cells.
        """
        self.tiles: list[list[Cell]] = []
        self.actual_mines = 0

        # Distribute mines and treasures randomly
        mines = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size), self.dif.min_mines, self.dif.max_mines
        )
        treasures = Utility.randomly_distribute_values_2d(
            (self.dif.x_size, self.dif.y_size), self.dif.min_treasures, self.dif.max_treasures
        )

        for x in range(self.dif.x_size):
            for y in range(self.dif.y_size):
                if y == 0:
                    self.tiles.append([])

                cell_type = CellType.EMPTY
                if treasures[x][y] == 1:
                    cell_type = CellType.TREASURE
                elif mines[x][y] == 1:
                    cell_type = CellType.MINE
                    self.actual_mines += 1

                tile = Cell(cell_type, x, y)
                self.tiles[x].append(tile)

    def count_mines_treasures(self):
        """
        Updates the count of nearby mines and treasures for each cell.
        """
        for x in range(self.dif.x_size):
            for y in range(self.dif.y_size):
                mc = 0
                tc = 0
                for neighbor in self.get_neighbors(x, y):
                    mc += 1 if neighbor.type == CellType.MINE else 0
                    tc += 1 if neighbor.type == CellType.TREASURE else 0
                self.tiles[x][y].nearby_mines = mc
                self.tiles[x][y].nearby_treasures = tc

    def update_timer(self):
        """
        Updates the game timer based on the elapsed time since the game started.

        Returns:
            str: Formatted time string (hh:mm:ss).
        """
        ts = "00:00:00"
        if self.start_time:
            delta = datetime.now() - self.start_time
            ts = str(delta).split(".")[0]
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # Add leading zero for single-digit hours
        else:
            self.start_time = datetime.now()
        return ts

    @require(lambda self, mine_x, mine_y: self.tiles[mine_x][mine_y].type == CellType.MINE)
    def move_mine(self, mine_x, mine_y):
        """
        Moves a mine from the specified location to a random empty spot.

        Args:
            mine_x (int): X-coordinate of the mine to be moved.
            mine_y (int): Y-coordinate of the mine to be moved.

        Returns:
            tuple: The new coordinates of the moved mine.
        """
        empty_spots = [
            (x, y)
            for x in range(self.dif.x_size)
            for y in range(self.dif.y_size)
            if self.tiles[x][y].type == CellType.EMPTY
        ]
        if not empty_spots:
            raise ValueError("No empty spots available to move the mine.")

        new_x, new_y = random.choice(empty_spots)
        self.tiles[mine_x][mine_y].type = CellType.EMPTY
        self.tiles[new_x][new_y].type = CellType.MINE

        self.count_mines_treasures()  # Recalculate counts after moving the mine
        return new_x, new_y

    @require(lambda file_path: isinstance(file_path, str))
    def load_board_from_csv(self, file_path: str):
        """
        Loads a board configuration from a CSV file.

        Args:
            file_path (str): The path to the CSV file.

        Raises:
            ValueError: If the CSV format is invalid or the file is not found.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

            if len(rows) != self.dif.x_size or any(len(row) != self.dif.y_size for row in rows):
                raise ValueError("CSV dimensions do not match the board size.")

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

            self.count_mines_treasures()

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except csv.Error as e:
            raise ValueError(f"Error reading CSV file: {e}")
