import random
from Point import *
import copy

#Andrew Christoforakis
#Arin Schwartz


def readFile(name):
        file = open(name)
        list = file.readlines()
        points = []
        masterList =  [x.strip().split(',') for x in list]
        file.close()
        for entry in masterList:
                p = Point([float(x) for x in entry[:-1]], float(entry[-1]))
                points.append(p)
        return points

def randomPoints(num,dim):
        for i in range(num):
                list = []
                for j in range(dim):
                        list.append(str(random.random()))
                list.append(str(random.randint(0,1)))
                print ",".join(list)



class Region:
	"""Region is defined by a list of N lists (for N dimensions), each containing two 
coordinates: a lower and upper bound for the Nth dimension."""

	masterList = []
	masterDict = {}
	optimalRegions = []

        def __init__(self, boundaries):
                self.boundaries = boundaries

        def __eq__(self, other):
                return self.boundaries==other.boundaries

        def __hash__(self):
                tuples = []
		for list in self.boundaries:
			tuples.append(tuple(list))
		return hash(tuple(tuples))

        def display(self):
                for minMax in self.boundaries:
                        print minMax

	def size(self):
		return len(self.boundaries)

        #returns boundaries of ith dimension
        def dimension(self, i):
                return [float(p[i]) for p in self.boundaries]

        #tests if value falls within region
        def inRegion(self, point):
		for i in range(self.size()):
			boundaries = self.boundaries[i]
			value = point.list[i]
			if value < boundaries[0] or value >= boundaries[1]:
				return False
		return True
                
        def pointsInRegion(self):
                points = []
                for point in Region.masterList:
                        if self.inRegion(point):
                                points.append(point)
                return points

	#bisects region at ith dimension, returns bottom slice
	def bottom(self, i):
		minMax = self.boundaries[i]
		mean = sum(minMax)/2.0
		bottomHalf = copy.deepcopy(self)
		bottomHalf.boundaries[i][1] = mean
		return bottomHalf

	def top(self, i):
		minMax = self.boundaries[i]
		mean = sum(minMax)/2.0
		topHalf = copy.deepcopy(self)
		topHalf.boundaries[i][0] = mean
		return topHalf

	def nextSplit(self):
		list = []
		for i in range(self.size()):
			list.append([self.top(i), self.bottom(i)])
		return list

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
				costs = [x[0].cost(l,depth-1) + x[1].cost(l,depth-1) for x in self.nextSplit()]
				costs.append(self.error() + l)
				minCost = min(costs)
				Region.masterDict[self] = minCost
				return minCost
		
	def optimalSplits(self):
		if self.bottom(0) not in Region.masterDict:
			Region.optimalRegions.append(self)
		cost = Region.masterDict[self]
		for list in self.nextSplit():
			if cost == Region.masterDict[list[0]] + Region.masterDict[list[1]]:
				Region.optimalRegions.append(list[0])
				Region.optimalRegions.append(list[1])

#calculate accuracy of training data, first need optimalRegions list
def computeAccuracy():
        totalError = 0
        allPoints = len(Region.masterList)
        for entry in Region.optimalRegions:
                totalError += entry.error()
        return (allPoints - totalError)/float(allPoints)

#calculates accuracy of testing data, first need optimalRegions list
def computeTestAccuracy(fileName):
        matches = 0
        list = readFile(fileName)
        allPoints = len(list)
        for point in list:
                for region in Region.optimalRegions:
                        if region.inRegion(point) and point.cat == region.category():
                                matches = matches + 1
        return matches/float(allPoints)

#creates unit region in N dimensions
def unitRegion(N):
	boundaries = []
	for i in range(N):
		boundaries.append([0,1])
	return Region(boundaries)


#required function
def go(trainingFn, testingFn,lambda0, level):
	Region.masterList = readFile(trainingFn)
	size = len(Region.masterList[0].list)
	r = unitRegion(size)
	print "Optimal cost of training data: ", r.cost(lambda0, level)
	r.optimalSplits()
	print "Accuracy of model on training data: ", computeAccuracy()
	print "Optimal regions are:"
	for region in Region.optimalRegions:
		region.display()
		print
	print "Test accuracy is: ", computeTestAccuracy(testingFn)



go("data/pima0124/training.csv", "data/pima0124/testing.csv", 0, 3)

"""In testing this we ran the go function on the pima0124 data with lambda values ranging from 
zero to ten, and depths ranging from two to ten. In all cases, the region split once, and the 
accuracies were around 70%. Higher depths took exponentially longer, but returned similar 
accuracies and similar numbers of splits."""
