from Point import *
from Aux import readFile
from Utility import *
import sys

#Arin Schwartz


#Region class taked command line arguments (l, depth), where l is lambda and depth is level.

class Region:
	masterList = readFile("data/training.csv")
	masterDict = {}
	optimalRegions = []

	def __init__(self, lb, ub):
		self.lb = lb
		self.ub = ub

	def __eq__(self, other):
		return self.lb==other.lb and self.ub==other.ub

	def __hash__(self):
		return hash((self.lb, self.ub))

	def display(self):
		print (self.lb, self.ub)

	def inRegion(self, point):
		inX = self.lb[0] <= point.x and point.x < self.ub[0]
		inY = self.lb[1] <= point.y and point.y < self.ub[1]
		return inX and inY

	#regions include lower and left boundaries, i.e. (0,0) is in unit square, not (1,1)

	def left(self):
		newUB = ((self.lb[0] + self.ub[0])/2, self.ub[1])
		return Region(self.lb, newUB)

	def right(self):
		newLB = ((self.lb[0] + self.ub[0])/2, self.lb[1])
		return Region(newLB, self.ub)

	def top(self):
		newLB = (self.lb[0], (self.lb[1] + self.ub[1])/2)
		return Region(newLB, self.ub)

	def bottom(self):
		newUB = (self.ub[0], (self.lb[1] + self.ub[1])/2)
		return Region(self.lb, newUB)

	def pointsInRegion(self):
		regionList = []
		for point in self.masterList:
			if self.inRegion(point):
				regionList.append(point)
		return regionList

	def error(self):
		total = 0
		list = self.pointsInRegion()
		for point in list:
			total += point.cat
		if total >= len(list)/2.0:
			return len(list) - total
		else:
			return total

	def category(self):
		total = 0
		list = self.pointsInRegion()
		for point in list:
			total += point.cat
		if total >= len(list)/2.0:
			return 1.0
		else:
			return 0.0

	def draw(self):
		if self.category() == 0.0:
			hue = 'red'
		else:
			hue = 'blue'
		x0 = self.lb[0]
		y0 = self.lb[1]
		x1 = self.ub[0]
		y1 = self.ub[1]
		drawFilledRectangle(x0,y0,x1,y1,color=hue, alpha=.3)

	def dictWalker(self):
		if self.left() not in Region.masterDict:
			Region.optimalRegions.append(self)
		else:
			split = self.whichSplit()
			if split == 1:
				#removed all 'self.optimalRegions.append(self.left())-type lines, as they were causing redundancies. The regions we need will add themselves once they reach the bottom of the recursion thanks to surrounding Region.optimalRegions.append(self)-type lines.
				self.left().dictWalker()
				self.right().dictWalker()
				#added 'self' to the beginning of all optimalRegions lists 
			elif split == -1:
				self.top().dictWalker()
				self.bottom().dictWalker()
			else:
				self.optimalRegions.append(self)

	def whichSplit(self):
		#throws KeyError if region has no partitions, must check first
		lr = self.left() not in Region.masterDict and self.right() not in Region.masterDict
		tb =self.top() not in Region.masterDict and self.bottom() not in Region.masterDict
		if lr and tb:
			return 0
		cost = min(Region.masterDict[self], Region.masterDict[self.left()] + Region.masterDict[self.right()], Region.masterDict[self.top()] + Region.masterDict[self.bottom()])
		if cost == Region.masterDict[self.left()] + Region.masterDict[self.right()]:#one instance of masterList instead of masterDict. That's why it was asking for an index, because it saw Region.masterList[self.bottom()].
			return 1
		elif cost == Region.masterDict[self.top()] + Region.masterDict[self.bottom()]:
			return -1
		else:
			return 0

	def cost(self, l, depth):
		members = len(self.pointsInRegion())
		if depth == 0:
			if self in Region.masterDict:
				return Region.masterDict[self]
			else:
				Region.masterDict[self] = self.error() + l
			return self.error() + l
		elif members == 0 or members == 1:
			if self in Region.masterDict:
				return Region.masterDict[self]
			else:
				Region.masterDict[self] = self.error() + l
			return self.error() + l
		else:
			if self in Region.masterDict:
				return Region.masterDict[self]
			else:
				thiscost =  min(self.error() + l, self.left().cost(l, depth-1) + self.right().cost(l, depth-1), self.top().cost(l,depth-1) + self.bottom().cost(l,depth-1))
				Region.masterDict[self] = thiscost
			return thiscost



	#Test suite and partition drawer
	def createPartitions(self, l, depth):
		self.cost(l, depth)
		print "The cost of the optimal partitions is: " , self.cost(l, depth)
		print "Creating tree..."
		self.dictWalker()

		#print "List of optimally partitioned regions: "
		#for entry in Region.optimalRegions:
		#	entry.display()

		print "Drawing map..."
		
		for entry in Region.optimalRegions:
			entry.draw()
		#pylab.show()


#calculate accuracy of training data, first need optimalRegions list
def computeAccuracy():
	totalError = 0
	allPoints = len(Region.masterList)
	for entry in Region.optimalRegions:	
		totalError += entry.error()
	return (allPoints - totalError)/float(allPoints)

#calculates accuracy of testing data, first need optimalRegions list
def computeTestAccuracy():
	matches = 0
	list = readFile("data/testing.csv")
	allPoints = len(list)
	for point in list:
		for region in Region.optimalRegions:
			if region.inRegion(point) and point.cat == region.category():
				matches = matches + 1
	return matches/float(allPoints)

#plots points in given list of points, adjusting for color
def plotPoints(list):
	for point in list:
		if point.cat == 0:
			marker = 'o'
		else:
			marker = '*'
		pylab.plot([point.x], [point.y], marker, color='k')


def go():

	if len(sys.argv) != 3:
		print "Error: python Region.py <lambda> <depth>"
	else:
		r.createPartitions(float(sys.argv[1]),float(sys.argv[2]))
		plotPoints(Region.masterList)
		pylab.show()
		print "Training data accuracy: ", computeAccuracy()
		print "Testing data accuracy: ", computeTestAccuracy()


r = Region((0.0, 0.0), (1.0, 1.0))
go()

pylab.savefig('Lambda 1')
