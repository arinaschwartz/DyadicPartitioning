from Point import *
import random

def readFile(name):
	file = open(name)
	list = file.readlines()
	masterList =  [x.strip().split(',') for x in list] 
	points = [Point(float(entry[0]), float(entry[1]),float(entry[2])) for entry in masterList]
	file.close()
	return points

#outputs random points to test our functions with
def randomPoints(num):
	for i in range(num):
		list = []
		list.append(str(random.random()))
		list.append(str(random.random()))
		list.append(str(random.randint(0,1)))
		print ",".join(list)

