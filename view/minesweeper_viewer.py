from abc import ABC, abstractmethod
from controller.controller import Controller


class Viewer(ABC):
    """Represents the View component in MVC architecture for minesweeper.
    Views should extend this class to ensure they will be compatible with the game.

    Args:
        ABC (ABC): Abstract class helper
    """
    
    @abstractmethod
    def __init__(self, controller: Controller, x_size: int, y_size: int):
        pass

    @abstractmethod
    def update_cell(self, x: int, y: int, ):
        pass
    
    @abstractmethod
    def get_difficulty(self):
        pass
    
    @abstractmethod
    def start_board(self):
        pass
    
    @abstractmethod
    def get_existing_board_path(self):
        """If user wishes to load an existing board, return the path to the board, otherwise returns None
        """
        pass
    
    def handle_input(self, x: int, y: int): # and some way of transfering the action taken by user
        self.controller.handle_input(x, y)
