from abc import ABC, abstractmethod
from controller.controller import Controller


class Viewer(ABC):
    """Represents the View component in MVC architecture for minesweeper.
    Views should extend this class to ensure they will be compatible with the game.

    Args:
        ABC (ABC): Abstract class helper
    """
    
    def __init__(self, x_size: int, y_size: int, controller: Controller):
        self.controller = controller
        self.x_size = x_size
        self.y_size = y_size

    @abstractmethod
    def update_cell(self, x: int, y: int):
        pass
    
    def handle_input(self, x: int, y: int): # and some way of transfering the action taken by user
        self.controller.handle_input(x, y)
