import argparse
from model.difficulty import Difficulty
from view.tkinter.tkinter_view import TkinterViewer
from view.text.text_view import TextView
from controller.controller import Controller


def main():
    """
    Entry point for the Minesweeper program.
    Usage:
        python run.py <difficulty> <viewer> [--testing-mode]
        Example:
        python run.py BEGINNER tkinter --testing-mode
    """

    # Supported difficulties and viewers
    difficulties = {
        "BEGINNER": Difficulty.BEGINNER,
        "INTERMEDIATE": Difficulty.INTERMEDIATE,
        "EXPERT": Difficulty.EXPERT,
    }

    viewers = {
        "tkinter": TkinterViewer,
        "text": TextView,
    }

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run Minesweeper with specified settings.")
    parser.add_argument(
        "difficulty",
        choices=difficulties.keys(),
        help="Select the difficulty level: BEGINNER, INTERMEDIATE, EXPERT",
    )
    parser.add_argument(
        "viewer",
        choices=viewers.keys(),
        help="Select the viewer type: tkinter or text",
    )
    parser.add_argument(
        "--testing-mode",
        action="store_true",
        help="Enable testing mode to load a predefined board.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Get difficulty and viewer
    difficulty = difficulties[args.difficulty.upper()]
    viewer_class = viewers[args.viewer.lower()]

    # Initialize the viewer and controller
    viewer = viewer_class()
    controller = Controller(viewer)
    viewer.controller = controller

    # Set the difficulty and optionally enable testing mode
    controller.set_difficulty(difficulty)
    controller.load_existing_board(args.testing_mode)

    # Start the game
    viewer.run()

if __name__ == "__main__":
    main()
