import numpy as np

class Line:

	def __init__(self,x1,x2,y1,y2):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2 

		# Change in x and y
		self.dx = self.x2 - self.x1
		self.dy = self.y2 - self.y1

		if abs(self.dx) > abs(self.dy):
			self.orientation = 'horizontal'
		else:
			self.orientation = 'vertical'
		# Slope
		self.m = self. dy / (self.dx + 1e7)

		# Using point-slope and slope-intercept form
		self.a =  self.m
		self.c = (-self.m * self.x1 + self.y1)
		self.b = ((self.m * self.x2) - (self.m * self.x1 + self.y1)) / self.y2

	def find_intersection(self,other):

		#a = np.array(((-self.a, self.b), (-other.a, other.b)))
		#b = np.array((self.b, other.b))
		#x, y = np.linalg.solve(a,b)
		x = ((self.x1*self.y2 - self.y1*self.x2)*(other.x1-other.x2) - (self.x1-self.x2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
		y = ((self.x1*self.y2 - self.y1*self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
		x = int(x)
		y = int(y)
		return x,y
