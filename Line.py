import numpy as np

class Line:

	def __init__(self,x1,x2,y1,y2):
		'''
		Creates a Line object
		'''

		# Endpoints
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2


		# Change in x and y
		self.dx = self.x2 - self.x1
		self.dy = self.y2 - self.y1

		# Orientation
		if abs(self.dx) > abs(self.dy):
			self.orientation = 'horizontal'
		else:
			self.orientation = 'vertical'


	def find_intersection(self,other):
		'''
		Finds intersection of this line and other. One line must be horizontal
		and the other must be vertical
		'''

		# Determinant for finding points of intersection
		x = ((self.x1*self.y2 - self.y1*self.x2)*(other.x1-other.x2) - (self.x1-self.x2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
		y = ((self.x1*self.y2 - self.y1*self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
		x = int(x)
		y = int(y)

		return x,y


