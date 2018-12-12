import imutils
import cv2
import argparse
import chess
from ChessEng import ChessEng
from board_Recognition import board_Recognition
from Board import Board
from Camera import Camera

class Game:
	'''
	This calss holds Game information interacting with the Board and Chess Engine
	'''

	def __init__(self):
		'''
		Initializes Game object	
		'''
		self.over = False
		self.CPUMoveError = False
		self.PlayerMoveError = False
		self.isCheck = False
		self.winner = "Me"

	def setUp(self):
		'''
		Initializes objects with which the Game will interact
		'''	
		self.camera = Camera()
		self.chessEngine = ChessEng(0)
		self.board = 0
		self.current = 0
		self.previous = 0
		self.CPULastMove = "0"


	def analyzeBoard(self):
		'''
		Calls board_recognition to take image and initialize Board
		'''

		boardRec = board_Recognition(self.camera)
		self.board = boardRec.initialize_Board()
		self.board.assignState()

	def checkBoardIsSet(self):
		'''
		Takes inital picture of set board
		'''	
		self.current = self.camera.takePicture()


	def playerMove(self):
		'''
		Compares previous Board to current board to determine the movement made by the player
		'''
		self.previous = self.current
		self.current = self.camera.takePicture()
		move = self.board.determineChanges(self.previous,self.current)
		code = self.chessEngine.updateMove(move)
		if code == 1:
			self.PlayerMoveError = True
		else:
			self.PlayerMoveError = False
			f = open("Game.txt", "a+")
			f.write(chess.Move.from_uci(move).uci() + "\r\n")
			f.close()
		if  self.chessEngine.engBoard.is_checkmate():
			self.winner = "You win!"
			self.over = True
			
	def playerPromotion(self, move):
		'''
		Compares previous Board to current board to determine the movement made by the player
		'''
		print(move)
		code = self.chessEngine.updateMove(move)
		if code == 1:
			print("Error")
			self.PlayerMoveError = True
		else:
			self.PlayerMoveError = False
			f = open("Game.txt", "a+")
			f.write(chess.Move.from_uci(move).uci() + "\r\n")
			f.close()
		if  self.chessEngine.engBoard.is_checkmate():
			self.winner = "You win!"
			self.over = True


	def CPUMove(self):
		'''
		Gets the CPU Move from the chess engine
		'''	

		self.CPULastMove = self.chessEngine.feedToAI()
		self.isCheck = self.chessEngine.engBoard.is_check()		
		if self.chessEngine.engBoard.is_checkmate():
			self.winner = "CPU Wins!"
			self.over = True
		return self.CPULastMove

	def updateCurrent(self):
		'''
		Compares previous image of the board to the current picture to update.
		Ensures player has moved the CPU piece properly
		'''
		self.previous = self.current
		self.current = self.camera.takePicture()
		move = self.board.determineChanges(self.previous, self.current)
		move = chess.Move.from_uci(move)
		if move == self.CPULastMove:
			self.CPUMoveError = False
		else:
			self.CPUMoveError = True
