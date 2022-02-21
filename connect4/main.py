"""
--------------------------------------------------------------------------
Connect 4 Human vs Robot
--------------------------------------------------------------------------
License:   
Copyright 2022 Sam Sarver

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Connect4 Game:
- Human vs robot game on real connect 4 game set
- 

Connect4 game code modified from Keith Galli: https://github.com/KeithGalli/Connect4-Python

--------------------------------------------------------------------------
"""
# Imports:
import operator
import numpy as np
import time
from random

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

ROW_COUNT = 6
COLUMN_COUNT = 7

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

game_over = False
turn = 0

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def displayScreen(message):
    #displays message on LCD screen
    return
# End def 

def create_board(): #creates blank board
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece): # drops a 1 or 2 in the row and col of the board
    board[row][col] = piece

def is_valid_location(board, col): # checks to see if the col has an empty spot
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col): # finds the next empety spot in a column
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board): # prints the board and flips it so that it looks real
    print(np.flip(board, 0))

def winning_move(board, piece): #detects if the added piece wins the game with 4 in a row
    #check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check for positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    #check for negatively sloped diagonals
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def checkDraw(board): #check to see if there are no possible ways for either player to win, in order to save time
    return#check to see if the current
    #turnNum is 1 or 2 depending on whose turn it is after the current state of array

def moveTo(col): #moves stepper motor to possition 0-6 on the board
    return

def releasePiece(): #moves servo motor to release 1 robot piece
    return

def get_OpenCV_board(): #get board data from camera
    cameraBoard = np.zeros((ROW_COUNT,COLUMN_COUNT)) # TEMPORARY - change to import openCV data
    return cameraBoard

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
board = create_board()
newBoard = board
board_update = False
#displayScreen("") get difficulty # - maybe do this at a later time

displayScreen("press button to start")

while not game_over:
    print_board(board)
    # player turn
    if turn == 0:
        displayScreen("human player turn")
        while not board_update:
            newBoard = get_OpenCV_board()
            if newBoard != board
                board = newBoard
                board_update = True
            else:
                time.sleep(1)
            
        if winning_move(board, 1):
            displayScreen("human player wins")
            game_over = True
        #insert checkDraw()
    # robot turn
    else:
        displayScreen("robot turn")
        col = random.randint(0, COLUMN_COUNT-1) # for now just does a random col for simplicity
        # col = getBestMove(board, player) #algorithim to determine robot best move, could be used to give hints to human player too
        if is_valid_location(board, col): # currently will not place a piece if not valid location
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            moveTo(col)
            releasePiece()
            
            if winning_move(board, 2):
                displayScreen("robot wins >:)")
                game_over = True
        #need to check to see if board matches with get_OpenCV_board() after piece has been released (~3 sec delay)
        
    turn += 1
    turn = turn % 2 #odd/even turns
    
    

    
    
    
    
