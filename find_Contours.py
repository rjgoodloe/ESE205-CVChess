# USAGE
# python findContours.py --image imageName.png


import cv2
import numpy as np
import argparse


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
blurred = cv2.pyrMeanShiftFiltering(image,31,91)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
ret, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

_,contours,_ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(image, contours, -1, (0,0,255),6)

cv2.imwrite("Pictures/drawContours.png", image)