import platform
from tkinter import Button, Frame, Label, PhotoImage, Tk, filedialog
from controller.controller import Controller
from model.cell import CellType
from view.minesweeper_viewer import MinesweeperViewer
from model.board import Board
from tkinter import messagebox

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

class TkinterViewer(MinesweeperViewer):
    
    def __init__(self):
        super().__init__(None)
        
        # create Tk instance
        self.tk = Tk()
        # set program title
        self.tk.title("Minesweeper")
        
        # import images
        self.images = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.gif"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "treasure": PhotoImage(file = "images/tile_treasure.png"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

        # set up frame
        self.frame = Frame(self.tk)
        self.frame.pack()

        # set up labels/UI
        self.labels = {
            "time": Label(self.frame, text = "00:00:00"),
            "mines": Label(self.frame, text = "Mines: 0"),
            "flags": Label(self.frame, text = "Flags: 0")
        }
        
        self.buttons = []
        self.elasped_time = "00:00:00"
        self.is_running = True
        
    def run(self):
        """Starts the Tkinter main loop."""
        self.start_timer()
        self.tk.mainloop()
    
    def get_existing_board_path(self):
        """Prompts the user to decide if they want to load a saved board, then opens a file dialog if confirmed."""
        # Ask the user if they want to load a saved board
        response = messagebox.askyesno(
            "Load Saved Board",
            "Do you want to load a saved board file?"
        )
        if response:  # User clicked 'Yes'
            file_path = filedialog.askopenfilename(
                title="Select a Saved Board File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            return file_path if file_path else None
        return None  # User clicked 'No'
    
    def initialize_board(self):
        """Sets up the buttons dynamically for the current board size."""
        # Clear existing buttons
        if len(self.buttons) > 0:
            for button_row in self.buttons:
                for button in button_row:
                    button.destroy()
            self.buttons = []
        
        # Create new buttons
        board: Board = self.controller.get_board()
        
        self.x_size = board.dif.x_size
        self.y_size = board.dif.y_size
        
        self.labels["time"].grid(row = 0, column = 0, columnspan = self.y_size) # top full width
        self.labels["mines"].grid(row = self.x_size+1, column = 0, columnspan = int(self.y_size/2)) # bottom left
        self.labels["flags"].grid(row = self.x_size+1, column = int(self.y_size/2)-1, columnspan = int(self.y_size/2)) # bottom right

        # tile image changeable for debug reasons:
        gfx = self.images["plain"]

        for x, row in enumerate(board.tiles):
            button_row = []
            for y, cell in enumerate(row):
                button = Button(self.frame, image = gfx)
                button.grid(row=x + 1, column=y)
                # Left-click for revealing a cell
                button.bind(BTN_CLICK, lambda event, x=x, y=y: self.controller.handle_click(x, y))
                # Right-click for flagging a cell
                button.bind(BTN_FLAG, lambda event, x=x, y=y: self.controller.handle_flag(x, y))
                button_row.append(button)
            self.buttons.append(button_row)

    def update_timer(self, elapsed_time):
        """Updates the timer display."""
        self.elasped_time = elapsed_time
        
    def start_timer(self):
        """Starts the periodic timer updates."""
        if self.is_running:
            self.labels["time"].config(text=self.elasped_time)
            self.tk.after(1000, self.start_timer)  # Schedule the next update

    
    def update(self, model: Board):
        """Updates the view to reflect the current model state."""
        self.labels["mines"].config(text=f"Mines: {model.actual_mines}")
        self.labels["flags"].config(text=f"Flags: {model.flag_count}")
        for x, row in enumerate(self.buttons):
            for y, button in enumerate(row):
                cell = model.tiles[x][y]
                if cell.is_checked:
                    if cell.type != CellType.MINE and cell.is_flagged:
                        button.config(image = self.images["wrong"])
                    elif cell.type == CellType.MINE:
                        button.config(image = self.images["mine"])  # Show mines
                    elif cell.type == CellType.TREASURE:
                        button.config(image = self.images["treasure"])  # Show treasures
                    elif cell.nearby_mines == 0:
                        button.config(
                            image = self.images["clicked"],
                            state="disabled"  # Disable checked cells
                        )
                    else:
                        button.config(
                            image = self.images["numbers"][cell.nearby_mines-1],
                            state="disabled"  # Disable checked cells
                        )
                elif cell.is_flagged:
                    button.config(image = self.images["flag"])  # Show flags
                else:
                    button.config(image = self.images["plain"])
                    
    def display_message(self, message):
        """Displays a message box for game-over scenarios."""
        self.tk.update()  # Force the UI to refresh before showing the dialog
        if messagebox.askyesno("Game Over", message):
            return True
        else:
            self.tk.quit()
        
