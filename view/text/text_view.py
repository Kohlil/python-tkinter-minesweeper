from minesweeper_viewer import MinesweeperViewer

class TextView(MinesweeperViewer):
    """Represents a text-based interface for Minesweeper."""

    def __init__(self):
        super().__init__(None)

    def display_board(self, model):
        """Displays the Minesweeper board in text form."""
        for row in model.tiles:
            row_repr = []
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

    def update(self, model):
        """Updates the console view with the current board state."""
        self.display_board(model)
