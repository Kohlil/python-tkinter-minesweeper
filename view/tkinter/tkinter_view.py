import platform
from controller.controller import Controller
from view.minesweeper_viewer import Viewer
from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
from datetime import datetime
from model.board import Board

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

class TkinterViewer(Viewer):
    
    def __init__(self, controller: Controller, x_size: int, y_size: int):
        self.controller = controller
        self.x_size = x_size
        self.y_size = y_size
        
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
        self.labels["time"].grid(row = 0, column = 0, columnspan = self.y_size) # top full width
        self.labels["mines"].grid(row = self.x_size+1, column = 0, columnspan = int(self.y_size/2)) # bottom left
        self.labels["flags"].grid(row = self.x_size+1, column = int(self.y_size/2)-1, columnspan = int(self.y_size/2)) # bottom right
        
    def start_board(self):
        self.tk.mainloop()
        
    def get_difficulty(self):
        pass
    
    def get_existing_board_path(self):
        return None
    
    def update_cell(self, x: int, y: int):
        pass
        
    # def gameOver(self, won):
    #     for x in range(0, self.X_SIZE):
    #         for y in range(0, self.Y_SIZE):
    #             if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
    #                 self.tiles[x][y]["button"].config(image = self.images["wrong"])
    #             if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
    #                 self.tiles[x][y]["button"].config(image = self.images["mine"])

    #     self.tk.update()

    #     msg = "You Win! Play again?" if won else "You Lose! Play again?"
    #     res = tkMessageBox.askyesno("Game Over", msg)
    #     if res:
    #         self.restart()
    #     else:
    #         self.tk.quit()
            
    # def refreshLabels(self):
    #     self.labels["flags"].config(text = "Flags: "+str(self.flagCount))
    #     self.labels["mines"].config(text = "Mines: "+str(self.mines))
            
    # def onClickWrapper(self, x, y):
    #     return lambda Button: self.onClick(self.tiles[x][y])

    # def onRightClickWrapper(self, x, y):
    #     return lambda Button: self.onRightClick(self.tiles[x][y])

    # def onClick(self, tile):
    #     if self.startTime == None:
    #         self.startTime = datetime.now()

    #     if tile["isMine"] == True:
    #         # end game
    #         self.gameOver(False)
    #         return

    #     # change image
    #     if tile["mines"] == 0:
    #         tile["button"].config(image = self.images["clicked"])
    #         self.clearSurroundingTiles(tile["id"])
    #     else:
    #         tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
    #     # if not already set as clicked, change state and count
    #     if tile["state"] != STATE_CLICKED:
    #         tile["state"] = STATE_CLICKED
    #         self.clickedCount += 1
    #     if self.clickedCount == (self.X_SIZE * self.Y_SIZE) - self.mines:
    #         self.gameOver(True)

    # def onRightClick(self, tile):
    #     if self.startTime == None:
    #         self.startTime = datetime.now()

    #     # if not clicked
    #     if tile["state"] == STATE_DEFAULT:
    #         tile["button"].config(image = self.images["flag"])
    #         tile["state"] = STATE_FLAGGED
    #         tile["button"].unbind(BTN_CLICK)
    #         # if a mine
    #         if tile["isMine"] == True:
    #             self.correctFlagCount += 1
    #         self.flagCount += 1
    #         self.refreshLabels()
    #     # if flagged, unflag
    #     elif tile["state"] == 2:
    #         tile["button"].config(image = self.images["plain"])
    #         tile["state"] = 0
    #         tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
    #         # if a mine
    #         if tile["isMine"] == True:
    #             self.correctFlagCount -= 1
    #         self.flagCount -= 1
    #         self.refreshLabels()
            
    # def clearSurroundingTiles(self, id):
    #     queue = deque([id])

    #     while len(queue) != 0:
    #         key = queue.popleft()
    #         parts = key.split("_")
    #         x = int(parts[0])
    #         y = int(parts[1])

    #         for tile in self.getNeighbors(x, y):
    #             self.clearTile(tile, queue)

    # def clearTile(self, tile, queue):
    #     if tile["state"] != STATE_DEFAULT:
    #         return

    #     if tile["mines"] == 0:
    #         tile["button"].config(image = self.images["clicked"])
    #         queue.append(tile["id"])
    #     else:
    #         tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

    #     tile["state"] = STATE_CLICKED
    #     self.clickedCount += 1
