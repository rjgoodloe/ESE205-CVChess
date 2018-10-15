import cv2
import numpy as np

detector = cv2.SimpleBlobDetector_create()

squares = detector.detect(image)

imgSquares = drawKeypoints(image, squares, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Squares", image)