from controller.controller import Controller
from model.board import Board
from model.difficulty import Difficulty
from view.minesweeper_viewer import Viewer
from view.tkinter.tkinter_view import TkinterViewer

def main():
    controller = Controller()
    board: Board = Board(Difficulty.BEGINNER)
    view: Viewer = TkinterViewer(board, board.dif.x_size, board.dif.y_size)
    view.start_board()

if __name__ == "__main__":
    main()