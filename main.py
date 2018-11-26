import imutils
import cv2
import argparse
from ChessEng import ChessEng
from board_Recognition import board_Recognition
from Board import Board
from Camera import Camera

class Game:

	def __init__(self):
		pass

	def setUp(self):
		self.camera = Camera()
		self.chessEngine = ChessEng(0)
		self.board = 0
		self.current = 0
		self.previous = 0
		print("Game Starting")

	def analyzeBoard(self):

		self.current = self.camera.takePicture()
		boardRec = board_Recognition(self.current, self.camera)
		self.board = boardRec.initialize_Board(self.current)
		self.board.assignState()
		print("Analyzing board")

	def checkBoardIsSet(self):
		self.current = self.camera.takePicture()
		print("Board is set")

	def playerMove(self):

		self.previous = self.current
		self.current = self.camera.takePicture()
		move = self.board.determineChanges(self.previous,self.current)
		self.chessEngine.updateMove(move)
		print("Player move")

	def CPUMove(self):

		print("CPU Move")
		move = self.chessEngine.feedToAI()

		return move

	def updateCurrent(self):

		self.previous = self.current
		self.current = self.camera.takePicture()
		print("updateCurrent")
