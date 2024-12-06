import threading
from model.board import Board
from model.difficulty import Difficulty
from view.minesweeper_viewer import MinesweeperViewer
import time

import faulthandler
faulthandler.enable()

class Controller:
    """Manages interactions between the model and views."""

    def __init__(self, view: MinesweeperViewer):
        self.view = view  # Reference to the view
        self.board = None  # The game board (model)
        self.is_running = False

    def set_difficulty(self, difficulty: Difficulty):
        """Initializes the board with the specified difficulty."""
        self.board = Board(difficulty)  # Create a new Board instance
        self.view.controller = self  # Pass reference to view
        self.view.initialize_board()  # Reset the view for the new board
        self.update_view()
        self.is_running = True
        
    def update_timer(self):
        """Periodically updates the view with the elapsed time."""
        while self.is_running:
            elapsed_time = self.board.update_timer()
            self.view.update_timer(elapsed_time)
            time.sleep(1)
        
    def stop_game(self):
        """Stops the game and timer."""
        self.is_running = False
        if self.board:
            self.board.stop_timer()

    def handle_click(self, x, y):
        """Handles a cell click event."""
        print(str(x) + ' ' + str(y))
        # start timer on first click
        if self.board.clicked_count == 0:
            threading.Thread(target=self.update_timer, daemon=True).start()
            
        if self.board:
            won = self.board.reveal_cell(x, y)  # Call reveal_cell from the model
            if won != None:  # Check if the game is over
                self.handle_game_over(won)
            else:
                self.update_view()

    def handle_flag(self, x, y):
        """Handles a flag event on a cell."""
        if self.board:
            won = self.board.toggle_flag(x, y)  # Call toggle_flag from the model
            if won != None:  # Check if the game is over
                self.handle_game_over(won)
            else:
                self.update_view()

    def update_view(self):
        """Notifies the view to update based on the model state."""
        if self.board:
            self.view.update(self.board)
        
    def handle_game_over(self, won):
        """Handles the game-over scenario."""
        self.is_running = False  # Stop the game loop
        self.update_view()  # Reveal the entire board
        restart = False
        if won:
            restart = self.view.display_message("You Win! Play again?")
        else:
            restart = self.view.display_message("You Lose! Play again?")
        
        if restart:
            self.set_difficulty(self.board.dif)

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