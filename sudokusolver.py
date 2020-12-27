from imutils.perspective import four_point_transform
import imutils
import cv2
import numpy as np
import pytesseract

def find_board(image):
  image = cv2.imread(image)
  grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(grayscale, (7,7), 3)
  threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  threshold = cv2.bitwise_not(threshold)

  conts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  conts = imutils.grab_contours(conts)
  conts = sorted(conts, key=cv2.contourArea, reverse=True)

  board_cont = None

  #loop over contors to find the board rather than assumingthe largest is the board
  for cont in conts:
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)

    if len(approx) == 4:
      board_cont = approx
      break

  board = four_point_transform(image, board_cont.reshape(4,2))

  sudoku = cv2.resize(board, (450,450))
  grid = np.zeros([9,9], dtype=int)
  for i in range(9):
      for j in range(9):
          image = sudoku[i*50:(i+1)*50,j*50:(j+1)*50]

          num = identify_number(image)
          try:
            grid[i][j] = int(num)
          except:
            pass

  return grid


def identify_number(cell):

  grayscale = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

  img_cropped = grayscale[8:45, 8:45]
  custom_config = r'--oem 3 --psm 13 -c tessedit_char_whitelist=123456789'
  return pytesseract.image_to_string(img_cropped, config=custom_config)


def solve(board):
  find = find_empty(board)
  if not find:
    return True
  else:
    row, col = find

  for i in range(1,10):
    if valid(board, i, (row,col)):
      board[row][col] = i

      if solve(board):
        return True

      board[row][col] = 0

  return False


def valid(board, num, pos):
  for i in range(len(board[0])):
    if board[pos[0]][i] == num and pos[1] != i:
      return False

  for i in range(len(board)):
    if board[i][pos[1]] == num and pos[0] != i:
      return False

  box_x = pos[1] // 3
  box_y = pos[0] // 3

  for i in range(box_y * 3, box_y * 3 + 3):
    for j in range(box_x * 3, box_x * 3 + 3):
      if board[i][j] == num and (i,j) != pos:
        return False

  return True

# function to find an empty space
def find_empty(board):
  for i in range(len(board)):
    for j in range (len(board[0])):
      if board[i][j] == 0:
        return (i, j) # row, col

  return None

def print_board(board):
  for i in range(len(board)):
    if i % 3 == 0 and i != 0:
      print("-----------------------")

    for j in range(len(board[0])):
      if j % 3 == 0 and j != 0:
        print(" | ", end="")

      if j == 8:
        print(board[i][j])
      else:
        print(str(board[i][j]) + " ", end="")

file = input("name of img: ")
print("Identifying digits...")
board = find_board(file)
print_board(board)
print("-----------------------------------------------------------------------")
print("Finding the solution...")
solve(board)
print_board(board)


