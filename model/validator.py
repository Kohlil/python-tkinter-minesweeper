from model.board import Board
from model.cell import CellType

class Validator:

    @staticmethod
    def validate_board(board: Board):
        """
        Validate the test game board for beginner mode (8x8, 10 mines)

        Args:
            board (Board): The game board to validate.

        Returns:
            bool: True if the board is valid, False otherwise.
        """
        # Ensure the board dimensions are 8x8
        tiles = board.tiles
        if len(tiles) != 8 or not all(len(row) == 8 for row in tiles):
            return False

        # Count mines and treasures
        mine_count = sum(cell.type == CellType.MINE for row in tiles for cell in row)
        treasure_count = sum(cell.type == CellType.TREASURE for row in tiles for cell in row)

        # Validation rules
        if mine_count != 10:
            return False  # Must have exactly 10 mines
        if treasure_count < 1 or treasure_count > 9:
            return False  # Must have between 1 and 9 treasures

        # Validate mine placement
        mine_positions = [(i, j) for i, row in enumerate(tiles) for j, cell in enumerate(row) if cell.type == CellType.MINE]

        if len(mine_positions) < 10:
            return False

        # First 8 mines
        rows_covered = set()
        cols_covered = set()
        for idx, (r, c) in enumerate(mine_positions[:8]):
            if r in rows_covered or c in cols_covered:
                return False
            rows_covered.add(r)
            cols_covered.add(c)

            # Ensure no adjacent mines
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if (r + dr, c + dc) in mine_positions[:8]:
                    return False

        # Ensure one mine is at a diagonal (row == col)
        if not any(r == c for r, c in mine_positions[:8]):
            return False

        # Ninth mine adjacent to one of the first 8 mines
        r9, c9 = mine_positions[8]
        if not any((abs(r9 - r) == 1 and abs(c9 - c) == 0) or (abs(r9 - r) == 0 and abs(c9 - c) == 1) for r, c in mine_positions[:8]):
            return False

        # Tenth mine isolated
        r10, c10 = mine_positions[9]
        if any(abs(r10 - r) <= 1 and abs(c10 - c) <= 1 for r, c in mine_positions[:9]):
            return False

        return True
