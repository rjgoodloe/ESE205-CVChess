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

empty = cv2.imread("newEmpty.jpg")
end = cv2.imread("end.jpg")
move1 = cv2.imread("move1.jpg")
move2 = cv2.imread("move2.jpg")
start = cv2.imread("start.jpg")

# Take image and make squares and store empty color value
boardRec = board_Recognition(empty)
board = boardRec.initialize_Board(empty)
board.assignState()
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


emptyResize = imutils.resize(empty, width=400, height = 400)
endResize = imutils.resize(end, width=400, height = 400)
move1Resize = imutils.resize(move1, width=400, height = 400)
move2Resize = imutils.resize(move2, width=400, height = 400)
startResize = imutils.resize(start, width=400, height = 400)
chessEngine  = ChessEng(board)

#board.draw(emptyResize)
move = board.determineChanges(startResize,move1Resize)
#board.draw(startResize)
#board.draw(move1Resize)
chessEngine.updateMove(move)
move = board.determineChanges(move1Resize,move2Resize)
#board.draw(move2Resize)

chessEngine.updateMove(move)
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

