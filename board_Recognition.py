import math
import cv2
import numpy as np
import imutils
from Line import Line
from Square import Square
from Board import Board

debug =  False


class board_Recognition:

	def __init__(self, image):

		self.image = image
#		self.image2 = imutils.resize(image2, width=600)


	def initialize_Board(self, image):

		adaptiveThresh,img = self.clean_Image(image)

		mask = self.initialize_mask(adaptiveThresh,img)

		edges,colorEdges = self.findEdges(mask)

		horizontal, vertical = self.findLines(edges,colorEdges)

		corners = self.findCorners(horizontal, vertical, colorEdges)

		# find squares
		squares = self.findSquares(corners, img)

		boardMatrix = []

		board = Board(squares, boardMatrix)

		return board

	def clean_Image(self,image):
		# resize image for simpler and quicker analysis
		img = imutils.resize(image, width=400, height = 400)

		# Smooth image to remove noise
		img = cv2.GaussianBlur(img,(5,5),0)

		if debug:
			# Show smoothed image
			cv2.imshow("blur",img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Blur.png",img)

		# Convert to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

		# Setting all pixels above the threshold value to white and those below to black
		# Adaptive thresholding is used to combat differences of illumination in the picture
		adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
		if debug:
			# Show thresholded image
			cv2.imshow("Adaptive Thresholding", adaptiveThresh)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Adaptive_Thresholding.png",adaptiveThresh)

		return adaptiveThresh,img

	def initialize_mask(self, adaptiveThresh,img):

		# Find contours (closed polygons)
		_, contours, hierarchy = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Create copy of original image
		imgContours = img.copy()

		for c in range(len(contours)):
			# Area
			area = cv2.contourArea(contours[c])
			# Perimenter
			perimeter = cv2.arcLength(contours[c], True)
				# Filtering the chessboard edge / Error handling as some contours are so small so as to give zero division
				#For test values are 70-40, for Board values are 80 - 75 - will need to recalibrate if change
				#the largest square is always the largest ratio
			if c ==0:
				Lratio = 0
			if perimeter > 0:
				ratio = area / perimeter
				if ratio > Lratio:
					largest=contours[c]
					Lratio = ratio
					Lperimeter=perimeter
					Larea = area
			else:
					pass

		# Draw contours
		cv2.drawContours(imgContours, [largest], -1, (0,0,0), 1)
		if debug:
			# Show image with contours drawn
			cv2.imshow("Chess Boarder",imgContours)
			cv2.waitKey(0)
			cv2.imwrite("Boarder.png",imgContours)
			cv2.destroyAllWindows()

		# Epsilon parameter needed to fit contour to polygon
		epsilon = 0.1 * Lperimeter
		# Approximates a polygon from chessboard edge
		chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)

		# Create new all black image
		mask = np.zeros((img.shape[0], img.shape[1]), 'uint8')*125
		# Copy the chessboard edges as a filled white polygon size of chessboard edge
		cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
		# Assign all pixels that are white (i.e the polygon, i.e. the chessboard)
		extracted = np.zeros_like(img)
		extracted[mask == 255] = img[mask == 255]
		# remove strip around edge
		extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 20]

		if debug:
			# Show image with mask drawn
			cv2.imshow("mask",extracted)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Mask.png",extracted)
		return extracted

	def findEdges(self, image):
		# Find edges
		edges = cv2.Canny(image, 100, 200, None, 3)
		if debug:
			#Show image with edges drawn
			cv2.imshow("Canny", edges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Edges.png",edges)

		# Convert edges image to grayscale
		colorEdges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

		return edges,colorEdges

	def findLines (self, edges, colorEdges):
		# Infer lines based on edges
		lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 100,np.array([]), 100, 80)

		# Draw lines
		a,b,c = lines.shape
		for i in range(a):
			cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0,255,0),2,cv2.LINE_AA)

		if  debug:
			# Show image with lines drawn
			cv2.imshow("Lines",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Lines.png",colorEdges)

		# Create line objects and sort them by orientation (horizontal or vertical)
		horizontal = []
		vertical = []
		for l in range(a):
			[[x1,y1,x2,y2]] = lines[l]
			newLine = Line(x1,x2,y1,y2)
			if newLine.orientation == 'horizontal':
				horizontal.append(newLine)
			else:
				vertical.append(newLine)

		return horizontal, vertical

	def findCorners (self, horizontal, vertical, colorEdges):

		# Find corners (intersections of lines)
		corners = []
		for v in vertical:
			for h in horizontal:
				s1,s2 = v.find_intersection(h)
				corners.append([s1,s2])

		dedupeCorners = []
		for c in corners:
			matchingFlag = False
			for d in dedupeCorners:
				if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 20:
					matchingFlag = True
					break
			if not matchingFlag:
				dedupeCorners.append(c)

		for d in dedupeCorners:
			cv2.circle(colorEdges, (d[0],d[1]), 10, (0,0,255))


		if debug:
			#Show image with corners circled
			cv2.imshow("Corners",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			cv2.imwrite("Corners.png",colorEdges)



		return dedupeCorners

	def findSquares(self, corners, colorEdges):

		corners.sort(key=lambda x: x[0])
		rows = [[],[],[],[],[],[],[],[],[]]
		r = 0
		for c in range(0, 81):
			if c > 0 and c % 9 == 0:
				r = r + 1

			rows[r].append(corners[c])

		letters = ['a','b','c','d','e','f','g','h']
		numbers = ['1','2','3','4','5','6','7','8']
		Squares = []
		for r in rows:
			r.sort(key=lambda y: y[1])
		for r in range(0,8):
			for c in range (0,8):
				c1 = rows[r][c]
				c2 = rows[r][c + 1]
				c3 = rows[r + 1][c]
				c4 = rows[r + 1][c + 1]

				position = letters[r] + numbers[7-c]
				newSquare = Square(colorEdges,c1,c2,c3,c4,position)
#				newSquare.draw(colorEdges,(0,0,255),2)
				Squares.append(newSquare)



#		if debug:

                        #Show image with corners circled
			#cv2.imshow("Squares", colorEdges)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()
			#cv2.imwrite("Squares.png",colorEdges)


		return Squares
