from minesweeper_viewer import MinesweeperViewer
from model.board import Board
from model.cell import Cell

class TextView(MinesweeperViewer):
    """Represents a text-based interface for Minesweeper."""

    def __init__(self):
        super().__init__(None)
        self.elapsed_time = "00:00:00"  # Initialize timer display

    def display_status(self):
        """Displays the game status, including the timer."""
        print(f"Time Elapsed: {self.elapsed_time}")
        print("-" * 30)

    def display_board(self, model):
        """Displays the Minesweeper board in text form."""
        self.display_status()  # Show the timer and a separator
        for row in model.tiles:
            row_repr = []
            cell: Cell
            for cell in row:
                if cell.is_checked:
                    row_repr.append(str(cell.nearby_mines) if cell.nearby_mines > 0 else " ")
                elif cell.is_flagged:
                    row_repr.append("F")
                else:
                    row_repr.append(".")
            print(" ".join(row_repr))
        print("\n")

    def run(self):
        """Starts the text-based game loop."""
        while True:
            print("test")
            self.display_board(self.controller.get_board())
            cmd = input("Enter command (click x y / flag x y): ")
            parts = cmd.split()
            if len(parts) == 3:
                x, y = int(parts[1]), int(parts[2])
                if parts[0] == "click":
                    self.controller.handle_click(x, y)
                elif parts[0] == "flag":
                    self.controller.handle_flag(x, y)
            else:
                print("Invalid command!")

    def update(self, model: Board):
        """Updates the console view with the current board state."""
        self.display_board(model)

    def update_timer(self, elapsed_time):
        """Updates the timer display."""
        self.elapsed_time = elapsed_time
        # Print the status line in place without clearing the console
        print(f"\rTime Elapsed: {self.elapsed_time}", end="", flush=True)
