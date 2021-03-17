# SudokuSolver
Sudoku solver using backtracking. This initially started out with a hard-coded board however I have implemented Tesseract OCR to pull the board from a screenshot/image.

# How It Works
1. Drop an image of a sudoku puzzle into the folder
1. Run the script and it'll ask you for the file name
1. It will then open that image, complete some pre-processing and identify the digits in each cell.
1. This board is then passed to the backtracking algorithm which solves the soduku
1. The solution is then printed to the console.

# Notes
Most puzzles work, however, Tesseract has some difficulty in identifying single digits.
