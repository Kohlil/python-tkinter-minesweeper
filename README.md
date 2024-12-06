# Python Tkinter Minesweeper

Minesweeper game reengineered in Python using the Tkinter GUI library, following the Model-View-Controller (MVC) design pattern.

<img src="https://i.imgur.com/8JwCyAQ.png" alt="Screenshot on OSX" height="350"/>

## Contents:
- **`run.py`** - The entry point for the program. Accepts command-line arguments for difficulty, viewer type, and testing mode.
- **`images/`** - GIF images used by the Tkinter GUI for rendering tiles, flags, and treasures.
- **`model/`** - Package containing classes that represent the underlying Minesweeper game logic, including the board and cells.
- **`controller/`** - Package that connects the model to a specific view, serving as the game's logic and mediator.
- **`view/`** - Package containing multiple views (e.g., text-based or GUI) for interacting with the game.

## Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/Kohlil/python-tkinter-minesweeper.git
   ```
2. Ensure you have Python 3.13 installed. Install Tkinter if necessary:
   - Linux/WSL/MacOS:
     ```bash
     brew install python-tk
     ```
3. Create a virtual environment:
   ```bash
   python3.13 -m venv .venv
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the Minesweeper game:
   ```bash
   python run.py -h
   ```

## Command-Line Usage
The `run.py` program accepts the following command-line arguments:

### Required Arguments:
- **`<difficulty>`**: Select the difficulty level. Options:
  - `BEGINNER`: 8x8 board with 10 mines.
  - `INTERMEDIATE`: 16x16 board with 40 mines.
  - `EXPERT`: 30x16 board with 99 mines.
- **`<viewer>`**: Choose the viewer type. Options:
  - `tkinter`: GUI-based view using the Tkinter library.
  - `text`: Text-based view for playing in the terminal.

### Optional Arguments:
- **`--testing-mode`**: Enable testing mode to load a predefined board from a CSV file.

### Example Usage:
```bash
python run.py BEGINNER tkinter
python run.py INTERMEDIATE text --testing-mode
```

## Reengineered System

This project has been refactored to follow the MVC design pattern, improving modularity and separation of concerns. The reengineered system separates logic into three main components: `model`, `view`, and `controller`.

### **Model**
The `model` package contains all classes representing the Minesweeper game state. This includes the `Board`, which manages the grid, and `Cell`, which represents individual tiles.

### **View**
The `view` package contains subclasses for different types of user interfaces (e.g., text-based, GUI). Each view inherits from the abstract `MinesweeperViewer` class, enabling the controller to interact with all views uniformly.

### **Controller**
The `controller` package connects the model to a specific view. It handles user interactions, updates the model, and ensures the view reflects the latest game state.

### Key Changes from Original Design
Below is a table mapping functions from the original project to their corresponding locations in the reengineered system.

| **Original**            | **Reengineered**                             |
|:-----------------------:|:-------------------------------------------:|
| `__init__`              | `view.MinesweeperViewer.__init__`           |
| `setup` (board creation)| `model.board.Board.place_items`             |
| `setup` (count mines)   | `model.board.Board.count_mines_treasures`   |
| `setup` (view creation) | `view.MinesweeperViewer.initialize_board`   |
| `restart`               | `controller.Controller.handle_game_over`    |
| `refreshLabels`         | `view.MinesweeperViewer.update`             |
| `gameOver`              | `controller.Controller.handle_game_over`    |
| `updateTimer` (model)   | `model.board.Board.update_timer`            |
| `updateTimer` (view)    | `view.MinesweeperViewer.update_timer`       |
| `updateTimer` (controller)| `controller.Controller.update_timer`      |
| `getNeighbors`          | `model.board.Board.get_neighbors`           |
| `onClickWrapper`, `onRightClickWrapper` | `view.MinesweeperViewer`   |
| `onClick` (controller)  | `controller.Controller.handle_click`        |
| `onClick` (model)       | `model.board.Board.reveal_cell`             |
| `onRightClick` (controller)| `controller.Controller.handle_flag`      |
| `onRightClick` (model)  | `model.board.Board.toggle_flag`             |
| `clearSurroundingTiles` | `model.board.Board.reveal_cell` (recursive) |
| `main`                  | `run.py`                                   |

## Features
- **Multiple Difficulty Levels:** Beginner, Intermediate, and Expert difficulties with varying board sizes and mine counts.
- **GUI and Text-Based Views:** Play using a graphical interface or a terminal-based view.
- **MVC Architecture:** Clean separation of game logic (model), user interface (view), and game control (controller).
- **Custom Boards:** Load custom board configurations from a CSV file.
- **Testing Mode:** Easily enable testing mode via command-line arguments for pre-configured games.

Enjoy playing Minesweeper in your preferred format and difficulty level!