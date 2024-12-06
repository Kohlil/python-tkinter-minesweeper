from abc import ABC, abstractmethod
from model.board import Board

class MinesweeperViewer(ABC):
    """Abstract base class for Minesweeper views."""

    def __init__(self, controller):
        self.controller = controller  # Reference to the controller
        
    @abstractmethod
    def initialize_board(self):
        """Sets up the tiles dynamically for the current board size."""
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
        """Updates the timer display."""
        pass
    
    @abstractmethod
    def display_message(self, message):
        """Displays a message box for game-over scenarios and returns whether or not to restart."""
        pass
    
    @abstractmethod
    def get_existing_board_path(self):
        """Asks user if they want to load an existing board, returns path to board or None"""
        pass
