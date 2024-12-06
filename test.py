

from model.board import Board
from model.difficulty import Difficulty
from model.validator import Validator


def main():
    # Choose difficulty
    difficulty = Difficulty.BEGINNER  # Change this to intermediate or expert as needed
    model = Board(difficulty)
    isValid = Validator.validate_board(model)
    if isValid:
        print("Board is valid!")
    else:
        print("Board is NOT valid :(")


if __name__ == "__main__":
    main()