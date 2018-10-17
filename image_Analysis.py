import math
import cv2
import numpy as np
import argparse
import imutils
from Line import Line

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
args =vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
img = imutils.resize(image, width=600)


debug =  True

img = cv2.GaussianBlur(img,(5,5),0)
if debug:
	cv2.imshow("blur",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/blur.png",img)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Show adaptively thresholded image
adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
if debug:
	# Show both thresholded images
	cv2.imshow("Adaptive Thresholding", adaptiveThresh)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/Adaptive_Thresholding.png",adaptiveThresh)

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

cv2.drawContours(imgContours, [largest], -1, (0,0,0), 1)
if debug:
	cv2.imshow("Chess Boarder",imgContours)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
# Epsilon parameter needed to fit contour to polygon
epsilon = 0.1 * Lperimeter
# Approximates a polygon from chessboard edge
chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)

roi = cv2.polylines(imgContours,[chessboardEdge], True, (0,0,0), thickness=1)
if debug:
	cv2.imshow("roi",imgContours)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/ROI.png",imgContours)


# Create new all black image
mask = np.zeros((img.shape[0], img.shape[1]), 'uint8')*125
# Copy the chessboard edges as a filled white polygon
cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
# Assign all pixels to out that are white (i.e the polygon, i.e. the chessboard)
extracted = np.zeros_like(img)
extracted[mask == 255] = img[mask == 255]
# Make mask green in order to facilitate removal of the red strip around chessboard
extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 20]

if debug:
	cv2.imshow("mask",extracted)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/Mask.png",extracted)

edges = cv2.Canny(extracted, 100, 200, None, 3)
if debug:
	cv2.imshow("Canny", edges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/Edge_Detection.png",edges)


colorEdges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 100,np.array([]), 100, 80)

a,b,c = lines.shape
for i in range(a):
	cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0,255,0),2,cv2.LINE_AA)

if debug:
	cv2.imshow("Lines",colorEdges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/Line_Detection.png",colorEdges)


horizontal = []
vertical = []
for l in range(a):
	[[x1,y1,x2,y2]] = lines[l]
	newLine = Line(x1,x2,y1,y2)
	if newLine.orientation == 'horizontal':
		horizontal.append(newLine)
	else:
		vertical.append(newLine)
corners = []
for v in vertical:
	for h in horizontal:
		s1,s2 = v.find_intersection(h)
		corners.append([s1,s2])
		cv2.circle(colorEdges, (s1,s2), 10, (255,0,0))

#print(corners)
#print(lines[0])
#cv2.line(colorEdges, (x1,y1) , (x2, y2),(0,0,255))
if debug:
	cv2.imshow("Corners",colorEdges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite("Pictures/Corners.png",colorEdges)

