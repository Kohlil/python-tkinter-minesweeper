from model.board import Board
from model.cell import Cell, CellType
from model.difficulty import Difficulty
from model.validator import Validator

def create_board_from_array(array):
    """
    Helper function to create a Board object from a 2D array.
    1 = Mine, 2 = Treasure, 0 = Empty.
    """
    difficulty = Difficulty.BEGINNER  # Assuming beginner difficulty for the test
    board = Board(difficulty)
    board.tiles = []

    for x, row in enumerate(array):
        board.tiles.append([])
        for y, value in enumerate(row):
            if value == 1:
                cell_type = CellType.MINE
            elif value == 2:
                cell_type = CellType.TREASURE
            else:
                cell_type = CellType.EMPTY
            board.tiles[x].append(Cell(cell_type, x, y))

    return board


# Invalid
invalid = [
    [1, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [2, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 2, 0, 0, 0, 1],
]

# Valid Test Board
valid = [
    [1, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0]
]


# Create Board object
board = create_board_from_array(valid)

# Run Validator
is_valid = Validator.validate_board(board)
print(f"Board is {'valid' if is_valid else 'invalid'}.")