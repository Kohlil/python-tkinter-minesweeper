from controller.controller import Controller
from view.tkinter.tkinter_view import TkinterViewer
from model.difficulty import Difficulty

def main():
    # Choose difficulty
    difficulty = Difficulty.BEGINNER  # Change this to intermediate or expert as needed

    # Create the view
    view = TkinterViewer()

    # Create the controller and set difficulty
    controller = Controller(view)
    controller.set_difficulty(difficulty)

    # Run the game
    view.run()

if __name__ == "__main__":
    main()