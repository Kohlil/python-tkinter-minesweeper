from enum import Enum
from typing import Union
from icontract import require, ensure


class CellType(Enum):
    """Defines the types of cells on a Minesweeper board."""
    MINE = 1  # Cell containing a mine
    EMPTY = 0  # Cell is empty, will display the number of adjacent mines when revealed
    TREASURE = 2  # Cell containing a treasure that results in an automatic win
    
    # Following types are for saving board to csv, they duplicate states the boolean attributes typically store 
    MINE_FLAGGED = 3 # Cell with mine that has been correctly flagged
    EMPTY_FLAGGED = 4 # Empty cell that's been flagged
    EMPTY_CHECKED = 5 # Empty cell that's already checked
    TREASURE_FLAGGED = 6 # Treasure cell that has been flagged
    
    


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

    
class Cell:
    @require(
        lambda type, x, y: isinstance(type, (CellType, int)) and isinstance(x, int) and isinstance(y, int),
        "type must be a CellType or int, and coordinates must be integers",
    )
    def __init__(self, type: Union[CellType, int], x: int, y: int):
        """
        Initializes a new cell. Behavior varies based on the type of the `type` parameter.

        Args:
            type (CellType | int): The type of the cell, or an integer representing the saved state.
            x (int): The X-coordinate of the cell.
            y (int): The Y-coordinate of the cell.

        Raises:
            ValueError: If the type is invalid when provided as an int.
        """
        self.x = x
        self.y = y
        self._is_checked = False  # Initially unchecked
        self._is_flagged = False  # Initially unflagged
        self._nearby_mines = 0  # Default number of nearby mines
        self._nearby_treasures = 0  # Default number of nearby treasures

        if isinstance(type, CellType):
            # Standard initialization using CellType
            self.type = type
        elif isinstance(type, int):
            # Initialization from saved state in CSV
            match type:
                case CellType.EMPTY.value:
                    self.type = CellType.EMPTY
                case CellType.MINE.value:
                    self.type = CellType.MINE
                case CellType.TREASURE.value:
                    self.type = CellType.TREASURE
                case CellType.MINE_FLAGGED.value:
                    self.type = CellType.MINE
                    self._is_flagged = True
                case CellType.EMPTY_FLAGGED.value:
                    self.type = CellType.EMPTY
                    self._is_flagged = True
                case CellType.EMPTY_CHECKED.value:
                    self.type = CellType.EMPTY
                    self._is_checked = True
                case CellType.TREASURE_FLAGGED.value:
                    self.type = CellType.TREASURE
                    self._is_flagged = True
                case _:
                    raise ValueError(f"Invalid cell type '{type}' in CSV at ({x}, {y}).")
        else:
            raise TypeError("Invalid type provided for cell initialization.")

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
        
    def to_csv_state(self):
        """
        Returns the current state of the cell as a single digit

        Returns:
            int: The current state of the cell as a single digit
        """
        # Determine cell type string based on state
        type = -1
        if self.type == CellType.EMPTY and not self.is_checked and not self.is_flagged:
            type = CellType.EMPTY
        elif self.type == CellType.MINE and not self.is_flagged:
            type = CellType.MINE
        elif self.type == CellType.TREASURE and not self.is_flagged:
            type = CellType.TREASURE
        elif self.type == CellType.MINE and self.is_flagged:
            type = CellType.MINE_FLAGGED
        elif self.type == CellType.EMPTY and self.is_flagged:
            type = CellType.EMPTY_FLAGGED
        elif self.type == CellType.EMPTY and self.is_checked:
            type = CellType.EMPTY_CHECKED
        elif self.type == CellType.TREASURE and self.is_flagged:
            type = CellType.TREASURE_FLAGGED
        else:
            raise ValueError(f"Invalid cell state: cell_type={self.type}, is_checked={self.is_checked}, is_flagged={self.is_flagged}")

        return type.value
