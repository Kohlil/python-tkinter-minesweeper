from enum import Enum


class CellType(Enum):
    MINE = 1  # Cell containing a mine
    EMPTY = 2 # Cell is empty, does not contain a mine or treasure, will display number of adjacent mines when picked
    TREASURE = 3 # Cell contains a treasure that if chosen, user automatically wins the game


class Cell:
    """Represents a cell on the minesweeper board. Contains state variables such as is_checked, is_flagged
    """

    def __init__(self, type: CellType):
        self._is_checked = False # Set to false until user interacts with this cell
        self._is_flagged = False # Set to false until user interacts with this cell
        self._type = type
        self._nearby_mines = 0 # Initialize to zero and on second pass set the value if _type == CellType.EMPTY
    
    # is_checked getter / setter
    @property
    def is_checked(self):
        return self._is_checked
    
    @is_checked.setter
    def is_checked(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_checked must be a bool")
        if self._is_flagged and value:
            raise ValueError("cannot check a cell that is currently flagged")
        self._is_checked = value
        
    # is_flagged getter / setter
    @property
    def is_flagged(self):
        return self._is_flagged
    
    @is_flagged.setter
    def is_flagged(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_flagged must be a bool")
        if self._is_checked and value:
            raise ValueError("cannot flag a cell that has already been checked")
        self._is_flagged = value
       
    # nearby_mines getter / setter 
    @property
    def nearby_mines(self):
        return self._nearby_mines

    @nearby_mines.setter
    def nearby_mines(self, value):
        if not isinstance(value, int):
            raise TypeError("nearby_mines must be an int")
        self._nearby_mines = value