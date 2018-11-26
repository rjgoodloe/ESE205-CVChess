import cv2
import numpy as np
import math
debug = True

class Board:
	"""
	Holds all the Square instances and updates changes
	"""
	def __init__(self, squares, boardMatrix):
		# Squares
		self.squares = squares
		self.boardMatrix = boardMatrix

	def draw(self,image):
		"""
		Draws the board and classifies the squares (draws the square state on the image).
		"""
		for square in self.squares:
			square.draw(image, (0,0,255))
			square.classify(image)

	def assignState(self):
		"""
		Assigns initial setup states to squares and initialises the BWE matrix.
		"""
		black = ['r', 'n', 'b','q','k','b','n','r']
		white = ['R','N','B','Q','K','B','N','R']
		for i in range(8):
			self.squares[8*i + 0].state = black[i]
			self.squares[8*i + 1].state = 'p'
			self.squares[8*i + 2].state = '.'
			self.squares[8*i + 3].state = '.'
			self.squares[8*i + 4].state = '.'
			self.squares[8*i + 5].state = '.'
			self.squares[8*i + 6].state = 'P'
			self.squares[8*i + 7].state = white[i]

		for square in self.squares:
			self.boardMatrix.append(square.state)

	def determineChanges(self,previous, current):

		copy = current.copy()
		largestSquare = 0
		secondLargestSquare = 0
		largestDist = 0
		secondLargestDist = 0
		stateChange = []
		# check for differences in color between the photos
		for sq in self.squares:
			colorPrevious = sq.roiColor(previous)
			colorCurrent = sq.roiColor(current)

			sum = 0
			for i in range(0,3):
				sum += (colorCurrent[i] - colorPrevious[i])**2

			distance = math.sqrt(sum)
			if distance > 30:
				stateChange.append(sq)
			if distance > largestDist:
				secondLargestSquare = largestSquare
				secondLargestDist = largestDist
				largestDist = distance
				largestSquare = sq

			elif distance > secondLargestDist:
				secondLargestDist = distance
				secondLargestSquare = sq


		if  len(stateChange) == 4:
			print("castling")
			squareOne = stateChange[0]
			squareTwo = stateChange[1]
			squareThree = stateChange[2]
			squareFour = stateChange[3]
			if squareOne.position == "e1" or squareTwo.position == "e1" or squareThree.position == "e1" or  squareFour.position == "e1":
				if squareOne.position == "h1"  or squareTwo.position == "h1" or squareThree.position == "h1"  or squareFour.position == "h1":
					move = "e1g1"
					if debug:
						squareOne.draw(copy, (255,0,0), 2)
						squareTwo.draw(copy, (255,0,0), 2)
						squareThree.draw(copy, (255,0,0),2)
						squareFour.draw(copy, (255,0,0), 2)
						cv2.imshow("previous",previous)
						cv2.imshow("identified",copy)
						cv2.waitKey()
						cv2.imwrite("Identify.png",copy)
						cv2.imwrite("Previous.png",previous)
						cv2.destroyAllWindows()
				else:
					move = "e1c1"
					if debug:
						squareOne.draw(copy, (255,0,0), 2)
						squareTwo.draw(copy, (255,0,0), 2)
						squareThree.draw(copy, (255,0,0),2)
						squareFour.draw(copy, (255,0,0), 2)
						cv2.imshow("previous",previous)
						cv2.imshow("identified",copy)
						cv2.waitKey()
						cv2.imwrite("Identify.png",copy)
						cv2.imwrite("Previous.png",previous)
						cv2.destroyAllWindows()
				print(move)
				return move


		squareOne = largestSquare
		squareTwo = secondLargestSquare

		if debug:
			squareOne.draw(copy, (255,0,0), 2)
			squareTwo.draw(copy, (255,0,0), 2)
			cv2.imshow("previous",previous)
			cv2.imshow("identified",copy)
			cv2.waitKey(0)
			cv2.imwrite("Identify.png",copy)
			cv2.imwrite("Previous.png",previous)
			cv2.destroyAllWindows()

		# get colors for each square from each photo
		oneCurr = squareOne.roiColor(current)
		twoCurr = squareTwo.roiColor(current)

		sumCurr1 = 0
		sumCurr2 = 0
		for i in range(0,3):
			sumCurr1 += (oneCurr[i] - squareOne.emptyColor[i])**2
			sumCurr2 += (twoCurr[i] - squareTwo.emptyColor[i])**2

		distCurr1 = math.sqrt(sumCurr1)
		distCurr2 = math.sqrt(sumCurr2)

		if distCurr1 < distCurr2:
			# square 1 is currently empty
			squareTwo.state = squareOne.state
			squareOne.state = '.'

			move = squareOne.position + squareTwo.position
		else:
			# square 2 is currently empty
			squareOne.state = squareTwo.state
			squareTwo.state = '.'

			move = squareTwo.position + squareOne.position

		print(move)
		return move
