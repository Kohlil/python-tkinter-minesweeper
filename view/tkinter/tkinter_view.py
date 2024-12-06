import platform
from tkinter import Button, Frame, Label, PhotoImage, Tk, filedialog, messagebox
from controller.controller import Controller
from model.cell import CellType
from model.board import Board
from view.minesweeper_viewer import MinesweeperViewer
from icontract import require, ensure

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"


class TkinterViewer(MinesweeperViewer):
    """Represents a GUI-based interface for Minesweeper using Tkinter."""

    def __init__(self):
        """
        Initializes the TkinterViewer with a Tkinter window, image resources, and layout.
        """
        super().__init__(None)  # Initialize with no controller initially

        self.tk = Tk()  # Create Tk instance
        self.tk.title("Minesweeper")  # Set program title

        # Import images for different cell states
        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "treasure": PhotoImage(file="images/tile_treasure.png"),
            "numbers": [PhotoImage(file=f"images/tile_{i}.gif") for i in range(1, 9)],
        }

        # Set up the main frame for buttons and labels
        self.frame = Frame(self.tk)
        self.frame.pack()

        # Initialize UI labels
        self.labels = {
            "time": Label(self.frame, text="00:00:00"),
            "mines": Label(self.frame, text="Mines: 0"),
            "flags": Label(self.frame, text="Flags: 0"),
        }

        self.buttons = []  # Store buttons for the game grid
        self.elasped_time = "00:00:00"
        self.is_running = True

    def run(self):
        """Starts the Tkinter main loop."""
        self.start_timer()
        self.tk.mainloop()

    @ensure(lambda result: result is None or isinstance(result, str), "Result must be None or a valid file path")
    def get_existing_board_path(self):
        """
        Prompts the user to decide if they want to load a saved board, then opens a file dialog if confirmed.

        Returns:
            str or None: The file path to the saved board, or None if the user skips.
        """
        response = messagebox.askyesno("Load Saved Board", "Do you want to load a saved board file?")
        if response:  # User clicked 'Yes'
            file_path = filedialog.askopenfilename(
                title="Select a Saved Board File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            return file_path if file_path else None
        return None  # User clicked 'No'

    @require(lambda self: self.controller is not None, "Controller must be assigned before initializing the board")
    def initialize_board(self):
        """
        Sets up the buttons dynamically for the current board size based on the controller's model.
        """
        # Clear existing buttons
        if self.buttons:
            for button_row in self.buttons:
                for button in button_row:
                    button.destroy()
            self.buttons = []

        # Get board information from the controller
        board: Board = self.controller.get_board()
        self.x_size = board.dif.x_size
        self.y_size = board.dif.y_size

        # Place UI labels
        self.labels["time"].grid(row=0, column=0, columnspan=self.y_size)
        self.labels["mines"].grid(row=self.x_size + 1, column=0, columnspan=self.y_size // 2)
        self.labels["flags"].grid(row=self.x_size + 1, column=self.y_size // 2, columnspan=self.y_size // 2)

        # Create grid buttons
        gfx = self.images["plain"]
        for x, row in enumerate(board.tiles):
            button_row = []
            for y, _ in enumerate(row):
                button = Button(self.frame, image=gfx)
                button.grid(row=x + 1, column=y)
                button.bind(BTN_CLICK, lambda event, x=x, y=y: self.controller.handle_click(x, y))  # Left-click
                button.bind(BTN_FLAG, lambda event, x=x, y=y: self.controller.handle_flag(x, y))  # Right-click
                button_row.append(button)
            self.buttons.append(button_row)

    @require(lambda elapsed_time: isinstance(elapsed_time, str), "Elapsed time must be a string")
    def update_timer(self, elapsed_time):
        """Updates the timer display."""
        self.elasped_time = elapsed_time

    def start_timer(self):
        """Starts the periodic timer updates."""
        if self.is_running:
            self.labels["time"].config(text=self.elasped_time)
            self.tk.after(1000, self.start_timer)  # Schedule the next update

    @require(lambda model: isinstance(model, Board), "Model must be an instance of Board")
    def update(self, model: Board):
        """
        Updates the view to reflect the current model state.

        Args:
            model (Board): The current state of the Minesweeper board.
        """
        self.labels["mines"].config(text=f"Mines: {model.actual_mines}")
        self.labels["flags"].config(text=f"Flags: {model.flag_count}")

        for x, row in enumerate(self.buttons):
            for y, button in enumerate(row):
                cell = model.tiles[x][y]
                if cell.is_checked:
                    if cell.type != CellType.MINE and cell.is_flagged:
                        button.config(image=self.images["wrong"])
                    elif cell.type == CellType.MINE:
                        button.config(image=self.images["mine"])
                    elif cell.type == CellType.TREASURE:
                        button.config(image=self.images["treasure"])
                    elif cell.nearby_mines == 0:
                        button.config(image=self.images["clicked"], state="disabled")
                    else:
                        button.config(image=self.images["numbers"][cell.nearby_mines - 1], state="disabled")
                elif cell.is_flagged:
                    button.config(image=self.images["flag"])
                else:
                    button.config(image=self.images["plain"])

    @require(lambda message: isinstance(message, str), "Message must be a string")
    @ensure(lambda result: isinstance(result, bool), "Result must be a boolean")
    def display_message(self, message):
        """
        Displays a message box for game-over scenarios.

        Args:
            message (str): The game-over message to display.

        Returns:
            bool: True if the user wants to play again, False otherwise.
        """
        self.tk.update()  # Force the UI to refresh before showing the dialog
        return messagebox.askyesno("Game Over", message)
