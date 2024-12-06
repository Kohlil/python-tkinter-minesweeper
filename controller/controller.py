import sys
import threading
from model.board import Board
from model.difficulty import Difficulty
from model.validator import Validator
from view.minesweeper_viewer import MinesweeperViewer
import time
from icontract import require, ensure

class Controller:
    """Manages interactions between the model and views."""

    @require(lambda view: isinstance(view, MinesweeperViewer), "View must be an instance of MinesweeperViewer")
    def __init__(self, view: MinesweeperViewer):
        """
        Initializes the Controller with a reference to the view.

        Args:
            view (MinesweeperViewer): The view that displays the Minesweeper game.
        """
        self.view = view
        self.board = None
        self.is_running = False

    @require(lambda difficulty: isinstance(difficulty, Difficulty), "Difficulty must be an instance of Difficulty")
    def set_difficulty(self, difficulty: Difficulty):
        """
        Initializes the board with the specified difficulty and resets the view.

        Args:
            difficulty (Difficulty): The difficulty settings for the game.
        """
        self.board = Board(difficulty)
        self.view.controller = self  # Provide the controller reference to the view
        self.view.initialize_board()  # Reset the view for the new board
        self.is_running = True
        self.update_view()

    def update_timer(self):
        """
        Periodically updates the view with the elapsed time from the model.
        Runs in a separate thread to prevent blocking the main thread.
        """
        while self.is_running:
            elapsed_time = self.board.update_timer()
            self.view.update_timer(elapsed_time)
            time.sleep(1)

    def stop_game(self):
        """
        Stops the game and timer by updating the running state.
        """
        self.is_running = False

    @require(lambda self, x, y: self.board is not None and 0 <= x < self.board.dif.x_size and 0 <= y < self.board.dif.y_size,
             "Invalid cell coordinates or board not initialized")
    def handle_click(self, x, y):
        """
        Handles a cell click event by revealing the cell and checking game status.

        Args:
            x (int): The x-coordinate of the clicked cell.
            y (int): The y-coordinate of the clicked cell.

        Returns:
            bool: False if the game continues, or True if it ends.
        """
        if self.board.clicked_count == 0:
            threading.Thread(target=self.update_timer, daemon=True).start()

        if self.board:
            won = self.board.reveal_cell(x, y)
            if won is not None:
                self.handle_game_over(won)
            else:
                self.update_view()
        return False

    @require(lambda self, x, y: self.board is not None and 0 <= x < self.board.dif.x_size and 0 <= y < self.board.dif.y_size,
             "Invalid cell coordinates or board not initialized")
    def handle_flag(self, x, y):
        """
        Handles a flagging event on a cell, toggling its flagged state.

        Args:
            x (int): The x-coordinate of the flagged cell.
            y (int): The y-coordinate of the flagged cell.

        Returns:
            bool: False if the game continues, or True if it ends.
        """
        if self.board:
            won = self.board.toggle_flag(x, y)
            if won is not None:
                self.handle_game_over(won)
            else:
                self.update_view()
        return False

    @require(lambda self: self.board is not None, "Board must be initialized before updating the view")
    def update_view(self):
        """
        Notifies the view to update its display based on the current board state.
        """
        if self.board:
            self.view.update(self.board)

    @require(lambda self, won: isinstance(won, bool), "Game outcome must be a boolean")
    def handle_game_over(self, won):
        """
        Handles the game-over scenario by stopping the game, updating the view,
        and prompting the user to restart if desired.

        Args:
            won (bool): True if the player won, False otherwise.
        """
        self.is_running = False
        self.stop_game()
        self.update_view()

        # Display the result and prompt for restart
        restart = self.view.display_message("You Win! Play again?" if won else "You Lose! Play again?")
        if restart:
            self.set_difficulty(self.board.dif)

    @ensure(lambda self, result: result is None or isinstance(result, Board), "Returned object must be a Board or None")
    def get_board(self):
        """
        Retrieves the current game board.

        Returns:
            Board: The current game board, or None if not initialized.
        """
        return self.board

    def enable_testing_mode(self):
        """
        Enables testing mode by loading a predefined board configuration from a file.
        Validates the board before use.
        """
        file_path = self.view.get_existing_board_path()
        if file_path:
            try:
                self.board.load_board_from_csv(file_path)
                if not Validator.validate_board(self.board):
                    raise ValueError("Loaded board is not valid")
                self.update_view()
            except ValueError as e:
                print(f"Error loading board: {e}")
                sys.exit(1)

    @require(lambda self, file_path: isinstance(file_path, str) and self.board is not None,
             "File path must be a string and the board must be initialized")
    def save_game(self, file_path):
        """
        Saves the current game state to the specified file.

        Args:
            file_path (str): The path to save the game state.
        """
        self.board.save_game(file_path)
