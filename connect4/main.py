"""
--------------------------------------------------------------------------
Main Connect 4 Game Code
--------------------------------------------------------------------------
License:   
Copyright 2022 Samuel Sarver

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Connect4 game code modified from Keith Galli: https://github.com/KeithGalli/Connect4-Python

About:
- main code for robot vs human connect 4
- uses: lcd screen, external camera, 360 servo, stepper motor
"""

import numpy as np
import random
import sys
import math
import time
#import servo as SERVO
#from servo import Servo
import lcd as LCD
import readboard as RB
from bbpystepper import Stepper
import dropPiece
import posReset
import movetopos
import servo

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

DEG2POS = 20

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0				### was causing issues so i got rid of it. not sure if needed

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	# # Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	# # Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# # Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# # Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def getBoard(board):
	tries = 0
	while (True):
		#newCol = np.where()		#want way to detect valid board
		#newBoard = RB.readBoard()
		try:
			newBoard = RB.readBoard()
			if (np.array_equal(board, newBoard)):
				tries = tries + 1
				print('no new piece detected (',tries,')')
			else:
				newBoard2 = RB.readBoard()
				if (np.array_equal(newBoard, newBoard2)):
					if (np.array_equal(board, newBoard2)):
						tries = tries + 1
						print('no new piece detected (',tries,')')
					else:
						return newBoard
				else:
					print("temporary obstruction, trying again") # if the two board scans are not equal to each other # uncomment out these lines if getting inconsistent results or if want to detect obstructions
		except:
			print("error in board detection")
			tries = tries + 1
		
def wait4blankBoard():
	while True:
		newBoard = RB.readBoard()
		if (np.array_equal(create_board(), newBoard)):
			newBoard2 = RB.readBoard()
			if (np.array_equal(create_board(), newBoard2)):
				return
		

''' START OF MAIN CODE ''' 

lcd = LCD.LCD_Display()
mystepper = Stepper()
position = posReset.reset(1)

try: #needed to detect when the user stops the program
	while True: #game repeates when over
		board = create_board()
		print_board(board)
		game_over = False
		minimax_depth = 4 #depth how many turns in the future alg looks. max of 5 for PB processing power. min of 1 
		## minimax_depth = getDifficulty() #sets difficulty from a range of 1-4 with button (short press for next, long press for select) #currently not added
		turn = AI #random.randint(PLAYER, AI)
		
		while not game_over:
			if turn == PLAYER:
				lcd.display("Human player\nturn...")
				print("human player turn...")#
				#col = int(input("Player 1 make your selection (0-6): ")) #delete'''
				board = getBoard(board) #waits until a piece is added to the board, returns new board
				print("board recieved")
				print_board(board)
				
				if winning_move(board, PLAYER_PIECE):
					game_over = True
				turn += 1
				turn = turn % 2
			if turn == AI and not game_over:				
				print("Computer Turn. Calculating...")
				lcd.display("Computer Turn\ncalculating...")
				#col = random.randint(0, COLUMN_COUNT-1)
				col, minimax_score = minimax(board, minimax_depth, -math.inf, math.inf, True) #get best move using minimax
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, AI_PIECE)
					if winning_move(board, AI_PIECE):
						game_over = True
					turn += 1
					turn = turn % 2
					#print("please put a BLUE piece in column (left to right):",(col+1))
					#lcd.display('Place BLUE in\ncolumn: '+str(col+1))
					newpos = col + 1
					#print('moving to position',newpos,'from position',position)
					#print(position,newpos)
					print('Dropping piece in col ', col+1)
					lcd.display("Dropping piece\nin col " + str(col+1))
					newpos = movetopos.goto(position, newpos)
					servo.drop1()
					position = 4 # return to board center after piece dropped
					position = movetopos.goto(newpos, position)
					print_board(board)
			if game_over:
				print("Game over!")
				lcd.display("Game over!")
				#verify = input("Please emptey board. Press ENTER to start a new game. ")
				time.sleep(2)
				print("Empety board to start new game")
				lcd.display("Empety board to\nstart new game")
				wait4blankBoard()
				print("Starting new game")
				lcd.display("Starting new\ngame")
				

except KeyboardInterrupt:
	servo1.cleanup() #cleanup
	print("game stopped manually through KeyboardInterrupt")
