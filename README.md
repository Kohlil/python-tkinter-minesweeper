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