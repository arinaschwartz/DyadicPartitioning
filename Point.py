class Point:
	def __init__(self, x, y, cat):
		self.x = x
		self.y = y
		self.cat = cat

	def __eq__(self, other):
		return self.x==other.x and self.y==other.y and self.cat==other.cat

	def __hash__(self):
		return hash((self.x, self.y, self.cat))
	
	def display(self):
		print (self.x, self.y)
