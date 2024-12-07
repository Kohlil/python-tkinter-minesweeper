from itertools import combinations
from model.board import Board
from model.cell import CellType
from model.difficulty import Difficulty
from icontract import require, ensure


class Validator:
    """Utility class for validating Minesweeper boards."""

    @staticmethod
    @require(lambda board: isinstance(board, Board), "The board must be an instance of Board.")
    @require(lambda board: hasattr(board, "dif") and isinstance(board.dif, Difficulty), "The board must have a valid difficulty.")
    @ensure(lambda board, result: isinstance(result, bool), "The result must be a boolean value.")
    def validate_board(board: Board) -> bool:
        """
        Validates the Minesweeper board for the current difficulty.

        Args:
            board (Board): The game board to validate.

        Returns:
            bool: True if the board is valid, False otherwise.
        """
        tiles = board.tiles
        difficulty = board.dif

        # Ensure the board dimensions match the difficulty
        if len(tiles) != difficulty.x_size or not all(len(row) == difficulty.y_size for row in tiles):
            print(f"Invalid board dimensions. Expected {difficulty.x_size}x{difficulty.y_size}.")
            return False

        # Count mines and treasures
        mine_count = sum(cell.type == CellType.MINE for row in tiles for cell in row)
        treasure_count = sum(cell.type == CellType.TREASURE for row in tiles for cell in row)

        # Validation rules
        if not (difficulty.min_mines <= mine_count <= difficulty.max_mines):
            print(f"Invalid number of mines. Expected between {difficulty.min_mines} and {difficulty.max_mines}, but found {mine_count}.")
            return False
        if not (difficulty.min_treasures <= treasure_count <= difficulty.max_treasures):
            print(f"Invalid number of treasures. Expected between {difficulty.min_treasures} and {difficulty.max_treasures}, but found {treasure_count}.")
            return False

        # Gather mine positions
        mine_positions = [
            (i, j) for i, row in enumerate(tiles) for j, cell in enumerate(row) if cell.type == CellType.MINE
        ]

        if len(mine_positions) != mine_count:
            print(f"Unexpected number of mines in positions list. Expected {mine_count}, but found {len(mine_positions)}.")
            return False

        # Check all combinations of 8 mines for unique rows/columns and other constraints
        for combination in combinations(mine_positions, difficulty.min_mines):
            rows = {r for r, _ in combination}
            cols = {c for _, c in combination}

            # Ensure unique rows and columns
            if len(rows) != difficulty.min_mines or len(cols) != difficulty.min_mines:
                continue

            # Ensure no adjacent mines (cardinal directions only) within this combination
            if any(
                (r + dr, c + dc) in combination
                for r, c in combination
                for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]
            ):
                continue

            # Ensure at least one mine is on the diagonal (row == col)
            if not any(r == c for r, c in combination):
                continue

            # Validate remaining mines
            remaining_mines = [pos for pos in mine_positions if pos not in combination]

            # Ninth mine must be adjacent to one of the valid 8 mines
            if len(remaining_mines) >= 1:
                r9, c9 = remaining_mines[0]
                if not any(
                    (abs(r9 - r) == 1 and c9 == c) or (r9 == r and abs(c9 - c) == 1)
                    for r, c in combination
                ):
                    continue

            # Tenth mine must be isolated from the first 9 mines
            if len(remaining_mines) == 2:
                r10, c10 = remaining_mines[1]
                if any(
                    abs(r10 - r) + abs(c10 - c) == 1
                    for r, c in combination + [remaining_mines[0]]
                ):
                    continue

            # If a valid combination is found, the board is valid
            return True

        # If no valid combination is found, the board is invalid
        print("No valid combination of 8 mines satisfies the constraints.")
        return False
