import cv2 
import imutils
import numpy as np


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
resized = imutils.resize(image, width=600)
height, width = resized.shape[:2]
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

blurBilat = cv2.bilateralFilter(gray,9,75,75)
blurGaussian = cv2.GaussianBlur(gray,(5,5),0)

cv2.imshow("blur", blurBilat)
cv2.waitKey(0)
cv2.destroyAllWindows()	

edges = cv2.Canny(blurBilat,100,200)

lines = HoughLines(edges, 1, np.pi / 180, 150, None, 0 , 0)

#cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
#cdstP = np.copy(cdst)

blackImage = np.zeros((width,height,3), np.uint8)
 
 # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(blackImage, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
cv2.imshow("Black with Lines", blackImage)
cv2.waitKey(0)
cv2.destroyAllWindows()	
	
_, contours,_ = cv2.findContours(blackImage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cnt = contours[0]
#moments = cv2.moments(cnt)

z = 0
squares = []
for c in contours:
	area = contourArea(c)
	if area > 2000 and area < 3000:
		drawContours(resized, contours, z, (255,0,0), 5)
		newSquare = boundingRect(c)
		squares.append(newSquare)
	z = z + 1

	
cv2.imshow("Final", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()	