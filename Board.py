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

		stateChange = []
		largest = 0
		secondLargest = 0
		# check for differences in color between the photos
		for sq in self.squares:
			colorPrevious = sq.roiColor(previous)
			colorCurrent = sq.roiColor(current)

			sum = 0
			for i in range(0,3):
				sum += (colorCurrent[i] - colorPrevious[i])**2

			distance = math.sqrt(sum)
			if distance > secondLargest:
				if distance > largest:
					secondLargest = largest
					largest = distance
					stateChange.insert(0,sq)
				else:
					secondLargest = distance
					stateChange.insert(0,sq)

		squareOne = stateChange[0]
		squareTwo = stateChange[1]

		if debug:
#			squareOne.draw(current, (255,0,0), 2)
#			squareTwo.draw(current, (255,0,0), 2)
			cv2.imshow("previous",previous)
			cv2.imshow("identified",current)
			cv2.waitKey(0)
			cv2.imwrite("Identify.png",current)
			cv2.imwrite("Previous.png",previous)
			cv2.destroyAllWindows()

		# get colors for each square from each photo
		#onePrev = squareOne.roiColor(previous)
		oneCurr = squareOne.roiColor(current)
		#twoPrev = squareTwo.roiColor(previous)
		twoCurr = squareTwo.roiColor(current)

		sumCurr1 = 0
		sumCurr2 = 0
		for i in range(0,3):
			#sumPrev1 += (onePrev[i] - squareOne.emptyColor[i])**2
			sumCurr1 += (oneCurr[i] - squareOne.emptyColor[i])**2
			#sumPrev2 += (twoPrev[i] - squareTwo.emptyColor[i])**2
			sumCurr2 += (twoCurr[i] - squareTwo.emptyColor[i])**2

		#distPrev1 = math.sqrt(sumPrev1)
		distCurr1 = math.sqrt(sumCurr1)
		#distPrev2 = math.sqrt(sumPrev2)
		distCurr2 = math.sqrt(sumCurr2)
		attack = False
		#if squareOne.state != '.' and squareTwo.state != '.':
		#	attack = True

		if distCurr1 < distCurr2:
			# square 1 is currently empty
			squareTwo.state = squareOne.state
			squareOne.state = '.'
			if attack:
				move = squareOne.position + 'x' + squareTwo.position
			else:
				move = squareOne.position + squareTwo.position
		else:
			# square 2 is currently empty
			squareOne.state = squareTwo.state
			squareTwo.state = '.'
			if attack:
				move = squareTwo.position + 'x' + squareOne.position
			else:
				move = squareTwo.position + squareOne.position

		print(move)
		return move
