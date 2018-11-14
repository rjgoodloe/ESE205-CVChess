import imutils
import cv2
import argparse
from ChessEng import ChessEng
from board_Recognition import board_Recognition
from Board import Board
from Camera import Camera

#Prompt initialize empty board
#Take picture of board initially empty
#camera = Camera()
#image = camera.takePicture()
class Game:
#empty = cv2.imread("newEmpty.jpg")
#end = cv2.imread("end.jpg")
#move1 = cv2.imread("move1.jpg")
#move2 = cv2.imread("move2.jpg")
#start = cv2.imread("start.jpg")
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

		#self.current = self.camera.takePicture()
		#boardRec = board_Recognition(self.current)
		#self.board = boardRec.initialize_Board(self.current)
		#board.assignState()
		print("Analyzing board")

	def checkBoardIsSet(self):
		print("Board is set")

	def playerMove(self):

		#self.previous = self.current
		#self.current = self.camera.takePicture()
		#move = self.board.determineChanges(self.previous,self.current)
		#self.chessEngine.updateMove(move)
		print("Player move")

	def CPUMove(self):

		print("CPU Move")
		move = self.chessEngine.feedToAI()
		return move

# prompt fill board with pieces
# on button click -> begin game
# previous = camera.takePicture()
#gameOver = False
#while !gameOver
# 	prompt player  move
# on button click:
#	current = camera.takePicture()
# 	move = board.determineChanges(previous,current)
# 	give move to chess engine
# 	print response to touchscreen
# on button click:
#	previous = current
#	current = camera.takePicture()
# 	move = board.determineChanges(previous,current)
#	if response != move: throw error
#	previous = current


#emptyResize = imutils.resize(empty, width=400, height = 400)
#endResize = imutils.resize(end, width=400, height = 400)
#move1Resize = imutils.resize(move1, width=400, height = 400)
#move2Resize = imutils.resize(move2, width=400, height = 400)
#startResize = imutils.resize(start, width=400, height = 400)
#chessEngine  = ChessEng(board)

#board.draw(emptyResize)
#move = board.determineChanges(startResize,move1Resize)
#board.draw(startResize)
#board.draw(move1Resize)
#chessEngine.updateMove(move)
#move = board.determineChanges(move1Resize,move2Resize)
#board.draw(move2Resize)

#chessEngine.updateMove(move)
	#on start
	#	take image
	#	clean image
	#	makeboard
	#		find edges
	#		makes squares
	#		assign squares to matrix
	#	IF NO MOVES MADE YET
	#	prompt ready for first move return to start
	#	ELSE
	#		image difference
	#			determine which squares leaving entering
	#			set current image to previous for next iteration
	#		feed image difference to chess engine
	#		display results in GUI
	#	on click return to start

