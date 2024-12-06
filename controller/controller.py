from model.board import Board
from model.difficulty import Difficulty
from view.minesweeper_viewer import MinesweeperViewer

class Controller:
    """Manages interactions between the model and views."""

    def __init__(self, view: MinesweeperViewer):
        self.view = view  # Reference to the view
        self.board = None  # The game board (model)

    def set_difficulty(self, difficulty: Difficulty):
        """Initializes the board with the specified difficulty."""
        self.board = Board(difficulty)  # Create a new Board instance
        self.view.controller = self  # Pass reference to view
        self.view.initialize_board()  # Reset the view for the new board
        self.update_view()

    def handle_click(self, x, y):
        """Handles a cell click event."""
        if self.board:
            self.board.reveal_cell(x, y)  # Call reveal_cell from the model
            self.update_view()

    def handle_flag(self, x, y):
        """Handles a flag event on a cell."""
        if self.board:
            self.board.toggle_flag(x, y)  # Call toggle_flag from the model
            self.update_view()

    def update_view(self):
        """Notifies the view to update based on the model state."""
        if self.board:
            self.view.update(self.board)

    def get_board(self):
        """Returns the current game board."""
        return self.board

    def enable_testing_mode(self, file_path):
        """Enables testing mode by loading a predefined board."""
        try:
            self.board.load_board_from_csv(file_path)
            self.update_view()
        except ValueError as e:
            print(f"Invalid test board: {e}")

    def save_game(self, file_path):
        """Saves the current game state to a file."""
        self.board.save_game(file_path)

    def load_game(self, file_path):
        """Loads a saved game state from a file."""
        self.board = self.board.load_game(file_path)
        self.update_view()
        
    def get_board(self):
        return self.board