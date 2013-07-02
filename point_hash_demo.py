class Point:
    """ A class to hold x and y coordinates of a point """
    def __init__(self, x,y):
        self.x = x
        self.y = y

# Make two points
P = Point(1,2)
Q = Point(1,2)

# Make an empty dict
d = {}
d[P] = 5 # map P->5

# We now want to query d for Q and get out 5. We think this will work because
# we think that P is the same as Q (they both have the same x and y values)
# This is a simplistic version of the task you'll need to do for memoization

# Actually this code will raise an error
print d[Q]

# Lets see what's wrong
print "P equals Q?: ", P==Q # Prints False!!

# redefine point with an __eq__ method
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

P = Point(1,2)
Q = Point(1,2)

# This now prints true! Hooray!
print "P equals Q?: ", P==Q

d = {}
d[P] = 5 # this causes an error because now P is unhashable
# Annoyingly when you redefine __eq__ python no longer trusts the default hash
# method. Looks like we'll need to define one for it

# redefine point with an __hash__ method
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __hash__(self):
        return hash((self.x, self.y))


P = Point(1,2)
Q = Point(1,2)

d = {}
d[P] = 5 # This works!
print d[Q] # This now prints 5. All is well in the world.
# P and Q are effectively identical


# The following isn't relevant to your homework but might interest you
print "P==Q?: ", P==Q
print "P is Q?: " P is Q
# The is operator tests whether two objects are actually the same thing
# This is the difference between value equality '==' and object equality 'is'
