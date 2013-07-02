#Andrew Christoforakis
#Arin Schwartz

class Point:
	"""Point is constructed with a list of N coordinates (for N dimensions) and an 
additional value outside of the list representing its category as either a 0 or a 1."""
        def __init__(self, list, cat):
                self.list = list
                self.cat = cat

        def __eq__(self, other):
                return self.list==other.list and self.cat==other.cat

        def __hash__(self):
                return hash((self.list, self.cat))

        def display(self):
                print self.list, self.cat

