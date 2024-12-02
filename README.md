# Python Tkinter Minesweeper

Minesweeper game written in Python using Tkinter GUI library.

<img src="https://i.imgur.com/8JwCyAQ.png" alt="Screenshot on OSX" height="350"/>

## Contents:
- */minesweeper.py* - The actual python driver program
- */images/* - GIF Images ready for usage with Tkinter
- */images/original* - Original PNG images made with GraphicsGale
- */model* - Model package which abstracts the model of minesweeper
- */controller* - Controller package for connecting the model to a view
- */view* - View package containing different views that can be used by the controller

## Setup:
1. Clone the repository: `git clone https://github.com/Kohlil/python-tkinter-minesweeper.git`
2. If on Linux, Windows (WSL/Ubuntu) or MacOS, ensure tkinter is configured: `brew install python-tk`
3. Create a virtual environemnt: `python3.13 -m venv venv`
4. Activate the environemnt: `source venv/bin/activate`
5. Run the minesweeper game: `python minesweeper.py`

## Reengineered System
When refactoring the project to adhere to the MVC model, many methods were moved to new packages and modules.
Below is a table mapping functions from the original project to the new MVC architecture. The new architecture contains three main packages: model, view, and controller.
These packages each encapsulate a component of the MVC architecture.

### Model
Model contains all classes related to the underlying model of minesweeper such as a board and the cells that make up the board.

### View
View contains subpackages for each view. These views all extend an abstract class. This allows the controller to interact with the view in a consistent manner no matter what way each view actually displays the model.

### Controller
Connects the model to a specific view. This package contains the code for actually playing the game and manipulating the model.

|Original|Reengineered|
|---|---|
|||
