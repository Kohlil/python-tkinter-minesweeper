from enum import Enum
from icontract import require, invariant


@invariant(
    lambda self: self.min_treasures < self.min_mines,
    "The number of treasures must always be less than the number of mines"
)
@invariant(
    lambda self: self.max_treasures < self.max_mines,
    "The maximum number of treasures must always be less than the maximum number of mines"
)
class Difficulty(Enum):
    """
    Represents the difficulty levels for a Minesweeper game.

    Attributes:
        x_size (int): The number of rows in the board.
        y_size (int): The number of columns in the board.
        max_mines (int): The maximum number of mines allowed.
        min_mines (int): The minimum number of mines required.
        max_treasures (int): The maximum number of treasures allowed.
        min_treasures (int): The minimum number of treasures required.
    """
    BEGINNER = (8, 8, 10, 6, 5, 2)
    INTERMEDIATE = (16, 16, 40, 11, 4, 2)
    EXPERT = (30, 16, 99, 41, 3, 2)

    @property
    def x_size(self):
        """
        Returns the number of rows in the board.

        Returns:
            int: Number of rows.
        """
        return self.value[0]

    @property
    def y_size(self):
        """
        Returns the number of columns in the board.

        Returns:
            int: Number of columns.
        """
        return self.value[1]

    @property
    def max_mines(self):
        """
        Returns the maximum number of mines allowed.

        Returns:
            int: Maximum number of mines.
        """
        return self.value[2]

    @property
    def min_mines(self):
        """
        Returns the minimum number of mines required.

        Returns:
            int: Minimum number of mines.
        """
        return self.value[3]

    @property
    def max_treasures(self):
        """
        Returns the maximum number of treasures allowed.

        Returns:
            int: Maximum number of treasures.
        """
        return self.value[4]

    @property
    def min_treasures(self):
        """
        Returns the minimum number of treasures required.

        Returns:
            int: Minimum number of treasures.
        """
        return self.value[5]
