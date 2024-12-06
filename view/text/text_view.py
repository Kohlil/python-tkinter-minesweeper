from view.minesweeper_viewer import MinesweeperViewer
from model.board import Board
from model.cell import Cell, CellType
import sys


class TextView(MinesweeperViewer):
    """Represents a text-based interface for Minesweeper."""

    def __init__(self):
        super().__init__(None)  # Initialize with no controller for now

    def initialize_board(self):
        """Sets up the text-based board display with a legend."""
        self.elapsed_time = "00:00:00"  # Timer display
        self.x_size = 0
        self.y_size = 0
        print("Welcome to Minesweeper!")
        print("Commands: 'click x y' or 'flag x y'")
        print("Type 'exit' to quit the game.")
        print("\nLegend:")
        print("  .  : Unchecked cell")
        print("  F  : Flagged cell")
        print("  X  : Incorrect flag")
        print("  M  : Mine")
        print("  T  : Treasure")
        print("  <number>: Number of nearby mines")
        print("  (space): Checked cell with no nearby mines")
        print("-" * 30)

    def display_status(self):
        """Displays the game status, including the timer and separator."""
        print(f"Time Elapsed: {self.elapsed_time}")
        print("-" * 30)

    def display_board(self, model: Board):
        """Displays the Minesweeper board in text form, reflecting the current model state."""
        self.display_status()  # Show timer and separator

        # Create column headers (shifted to start from 1)
        column_labels = "    " + "".join(f"{i+1:2}" for i in range(len(model.tiles[0])))
        print(column_labels)
        print("   " + "-" * (len(model.tiles[0]) * 2 + 1))  # Add horizontal line separator

        # Create each row with a row label (shifted to start from 1)
        for idx, row in enumerate(model.tiles):
            row_repr = []
            cell: Cell
            for cell in row:
                if cell.is_checked:
                    if cell.type != CellType.MINE and cell.is_flagged:
                        row_repr.append("X")  # Incorrect flag
                    elif cell.type == CellType.MINE:
                        row_repr.append("M")  # Mine
                    elif cell.type == CellType.TREASURE:
                        row_repr.append("T")  # Treasure
                    elif cell.nearby_mines == 0:
                        row_repr.append(" ")  # No nearby mines
                    else:
                        row_repr.append(str(cell.nearby_mines))  # Number of nearby mines
                elif cell.is_flagged:
                    row_repr.append("F")  # Flag
                else:
                    row_repr.append(".")  # Unchecked cell
            print(f"{idx+1:2} | " + " ".join(row_repr))  # Add row label and vertical separator
        print("\n\n")


    def run(self):
        """Starts the text-based game loop."""
        self.keep_going = True
        while self.keep_going:
            cmd = input("Enter command (click x y / flag x y): ").strip()
            if cmd.lower() == "exit":
                self.is_running = False
                break
            parts = cmd.split()
            if len(parts) == 3:
                try:
                    x, y = int(parts[2]) - 1, int(parts[1]) - 1
                    
                    if x > self.x_size or y > self.y_size or self.x_size < 1 or self.y_size < 1:
                        raise ValueError()
                    
                    if parts[0].lower() == "click":
                        self.keep_going = not self.controller.handle_click(x, y)
                    elif parts[0].lower() == "flag":
                        self.keep_going = not self.controller.handle_flag(x, y)
                    else:
                        print("Invalid command! Use 'click x y' or 'flag x y'.")
                except ValueError:
                    print("Invalid coordinates! Use integers for x and y.")
            else:
                print("Invalid command! Use 'click x y' or 'flag x y'.")

    def update(self, model: Board):
        """Updates the console view with the current board state."""
        self.x_size = model.dif.x_size
        self.y_size = model.dif.y_size
        self.display_board(model)

    def update_timer(self, elapsed_time):
        """Updates the timer display."""
        self.elapsed_time = elapsed_time

    def display_message(self, message):
        """Displays a message to the player."""
        print(message)
        while True:
            restart = input("Do you want to play again? (yes/no): ").strip().lower()
            if restart in ("yes", "no"):
                if restart == "no":
                    sys.exit(0)
                return restart == "yes"
            print("Invalid input. Please type 'yes' or 'no'.")

    def get_existing_board_path(self):
        """Asks the user if they want to load an existing board."""
        path = input("Enter the path to a saved board file, or press Enter to skip: ").strip()
        return path if path else None
