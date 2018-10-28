import cv2
import numpy as np

class Square:

	def __init__(self, c1, c2, c3, c4, position):

		self.c1 = c1
		self.c2 = c2
		self.c3 = c3
		self.c4 = c4

		self.position = position

		self.cnt = np.array([c1,c2,c4,c3],dtype=np.int32)

	def draw(self, image, color=(0,0,255),thickness=2):

		ctr = np.array(self.cnt).reshape((-1,1,2)).astype(np.int32)
		cv2.drawContours(image, [ctr], 0, (0,0,255), 3)

