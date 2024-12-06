import sys
import threading
from model.board import Board
from model.difficulty import Difficulty
from model.validator import Validator
from view.minesweeper_viewer import MinesweeperViewer
import time
import deal

@deal.inv(lambda self: isinstance(self.view, MinesweeperViewer))  # Ensure the view is always a MinesweeperViewer
@deal.inv(lambda self: self.board is None or isinstance(self.board, Board))  # Board must be None or a valid Board
@deal.inv(lambda self: isinstance(self.is_running, bool))  # is_running must always be a boolean
class Controller:
    """Manages interactions between the model and views."""

    @deal.pre(lambda view: isinstance(view, MinesweeperViewer))  # Ensure the view is valid
    def __init__(self, view: MinesweeperViewer):
        self.view = view  # Reference to the view
        self.board = None  # The game board (model)
        self.is_running = False

    @deal.pre(lambda self, difficulty: isinstance(difficulty, Difficulty))  # Ensure difficulty is valid
    @deal.post(lambda self: self.board is not None)  # Ensure a board is created
    def set_difficulty(self, difficulty: Difficulty):
        """Initializes the board with the specified difficulty."""
        self.board = Board(difficulty)  # Create a new Board instance
        self.view.controller = self  # Pass reference to view
        self.view.initialize_board()  # Reset the view for the new board
        self.is_running = True
        self.update_view()
        
    @deal.pre(lambda self: self.board is not None)  # Ensure a board exists
    def update_timer(self):
        """Periodically updates the view with the elapsed time."""
        while self.is_running:
            elapsed_time = self.board.update_timer()
            self.view.update_timer(elapsed_time)
            time.sleep(1)
        
    def stop_game(self):
        """Stops the game and timer."""
        self.is_running = False

    @deal.pre(lambda self, x, y: x >= 0 and y >= 0)  # Ensure coordinates are non-negative
    @deal.pre(lambda self, x, y: self.board is not None)  # Ensure a board exists
    def handle_click(self, x, y):
        """Handles a cell click event."""
        # Start timer on first click
        if self.board.clicked_count == 0:
            threading.Thread(target=self.update_timer, daemon=True).start()
            
        if self.board:
            won = self.board.reveal_cell(x, y)  # Call reveal_cell from the model
            if won is not None:  # Check if the game is over
                self.handle_game_over(won)
            else:
                self.update_view()
        return False

    @deal.pre(lambda self, x, y: x >= 0 and y >= 0)  # Ensure coordinates are non-negative
    @deal.pre(lambda self, x, y: self.board is not None)  # Ensure a board exists
    def handle_flag(self, x, y):
        """Handles a flag event on a cell."""
        if self.board:
            won = self.board.toggle_flag(x, y)  # Call toggle_flag from the model
            if won is not None:  # Check if the game is over
                self.handle_game_over(won)
            else:
                self.update_view()
        return False

    @deal.pre(lambda self: self.board is not None)  # Ensure a board exists
    def update_view(self):
        """Notifies the view to update based on the model state."""
        if self.board:
            self.view.update(self.board)
        
    @deal.pre(lambda self, won: isinstance(won, bool))  # Ensure won is a boolean
    def handle_game_over(self, won):
        """Handles the game-over scenario."""
        self.is_running = False  # Stop the game loop
        self.stop_game()
        self.update_view()  # Reveal the entire board
        restart = False
        if won:
            restart = self.view.display_message("You Win! Play again?")
        else:
            restart = self.view.display_message("You Lose! Play again?")
        
        if restart:
            self.set_difficulty(self.board.dif)

    @deal.post(lambda result: result is None or isinstance(result, Board))  # Ensure the returned board is valid
    def get_board(self):
        """Returns the current game board."""
        return self.board

    def enable_testing_mode(self):
        """Enables testing mode by loading a predefined board."""
        file_path = self.view.get_existing_board_path()
        if file_path:
            try:
                self.board.load_board_from_csv(file_path)
                if not Validator.validate_board(self.board):
                    raise ValueError("board is not valid")
                self.update_view()
            except ValueError as e:
                print(f"Error loading board: {e}")
                sys.exit(1)

    @deal.pre(lambda self, file_path: isinstance(file_path, str))  # Ensure the file path is a string
    def save_game(self, file_path):
        """Saves the current game state to a file."""
        self.board.save_game(file_path)
        
    @deal.post(lambda result: result is None or isinstance(result, Board))  # Ensure the returned board is valid
    def get_board(self):
        return self.board
