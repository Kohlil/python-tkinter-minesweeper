import platform
from controller.controller import Controller
from view.minesweeper_viewer import MinesweeperViewer
from tkinter import *
from model.board import Board

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
        
    def run(self):
        """Starts the Tkinter main loop."""
        self.tk.mainloop()
    
    def get_existing_board_path(self):
        return None
    
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

        for x, row in enumerate(board.tiles):
            button_row = []
            for y, cell in enumerate(row):
                button = Button(self.frame, text="", width=3, height=1,
                                command=lambda x=x, y=y: self.controller.handle_click(x, y))
                button.grid(row=x + 1, column=y)
                button_row.append(button)
            self.buttons.append(button_row)

    def update_timer(self, elapsed_time):
        """Updates the timer display."""
        self.labels["time"].config(text=elapsed_time)
    
    def update(self, model: Board):
        """Updates the view to reflect the current model state."""
        self.labels["mines"].config(text=f"Mines: {model.actual_mines}")
        self.labels["flags"].config(text=f"Flags: {model.flagCount}")
        for x, row in enumerate(self.buttons):
            for y, button in enumerate(row):
                cell = model.tiles[x][y]
                if cell.is_checked:
                    button.config(text=str(cell.nearby_mines) if cell.nearby_mines > 0 else " ")
                elif cell.is_flagged:
                    button.config(text="F")
