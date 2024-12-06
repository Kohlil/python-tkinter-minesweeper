from abc import ABC, abstractmethod
from model.board import Board

class MinesweeperViewer(ABC):
    """Abstract base class for Minesweeper views."""

    def __init__(self, controller):
        self.controller = controller  # Reference to the controller
        
    @abstractmethod
    def initialize_board(self):
        pass

    @abstractmethod
    def run(self):
        """Starts the view loop."""
        pass

    @abstractmethod
    def update(self, model: Board):
        """Updates the view based on the current model state."""
        pass
    
    @abstractmethod
    def update_timer(self):
        pass
