from enum import Enum
from icontract import require, ensure


class CellType(Enum):
    """Defines the types of cells on a Minesweeper board."""
    MINE = 1  # Cell containing a mine
    EMPTY = 2  # Cell is empty, will display the number of adjacent mines when revealed
    TREASURE = 3  # Cell containing a treasure that results in an automatic win


class Cell:
    """
    Represents a cell on the Minesweeper board.

    Attributes:
        x (int): The X-coordinate of the cell.
        y (int): The Y-coordinate of the cell.
        type (CellType): The type of the cell (MINE, EMPTY, TREASURE).
        is_checked (bool): Whether the cell has been checked.
        is_flagged (bool): Whether the cell is flagged.
        nearby_mines (int): Number of nearby mines (only for empty cells).
        nearby_treasures (int): Number of nearby treasures (only for empty cells).
    """

    @require(lambda type: isinstance(type, CellType), "type must be an instance of CellType")
    @require(lambda x, y: isinstance(x, int) and isinstance(y, int), "Coordinates must be integers")
    def __init__(self, type: CellType, x: int, y: int):
        """
        Initializes a new cell.

        Args:
            type (CellType): The type of the cell.
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.
        """
        self.x = x
        self.y = y
        self._is_checked = False  # Initially unchecked
        self._is_flagged = False  # Initially unflagged
        self.type = type
        self._nearby_mines = 0  # Default number of nearby mines
        self._nearby_treasures = 0  # Default number of nearby treasures

    @property
    def is_checked(self):
        """
        Returns whether the cell has been checked.

        Returns:
            bool: True if the cell is checked, False otherwise.
        """
        return self._is_checked

    @is_checked.setter
    @require(lambda self, value: isinstance(value, bool), "is_checked must be a boolean")
    @require(lambda self, value: not (self._is_flagged and value), "Cannot check a cell that is flagged")
    def is_checked(self, value):
        """
        Sets the checked state of the cell.

        Args:
            value (bool): The new checked state of the cell.
        """
        self._is_checked = value

    @property
    def is_flagged(self):
        """
        Returns whether the cell is flagged.

        Returns:
            bool: True if the cell is flagged, False otherwise.
        """
        return self._is_flagged

    @is_flagged.setter
    @require(lambda self, value: isinstance(value, bool), "is_flagged must be a boolean")
    @require(lambda self, value: not (self._is_checked and value), "Cannot flag a cell that is already checked")
    def is_flagged(self, value):
        """
        Sets the flagged state of the cell.

        Args:
            value (bool): The new flagged state of the cell.
        """
        self._is_flagged = value

    @property
    def nearby_mines(self):
        """
        Returns the number of nearby mines.

        Returns:
            int: The number of mines adjacent to this cell.
        """
        return self._nearby_mines

    @nearby_mines.setter
    @require(lambda value: isinstance(value, int), "nearby_mines must be an integer")
    @ensure(lambda self: self._nearby_mines >= 0, "nearby_mines must be non-negative")
    def nearby_mines(self, value):
        """
        Sets the number of nearby mines.

        Args:
            value (int): The new number of nearby mines.
        """
        self._nearby_mines = value

    @property
    def nearby_treasures(self):
        """
        Returns the number of nearby treasures.

        Returns:
            int: The number of treasures adjacent to this cell.
        """
        return self._nearby_treasures

    @nearby_treasures.setter
    @require(lambda value: isinstance(value, int), "nearby_treasures must be an integer")
    @ensure(lambda self: self._nearby_treasures >= 0, "nearby_treasures must be non-negative")
    def nearby_treasures(self, value):
        """
        Sets the number of nearby treasures.

        Args:
            value (int): The new number of nearby treasures.
        """
        self._nearby_treasures = value
