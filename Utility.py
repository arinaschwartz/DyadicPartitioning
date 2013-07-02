import pylab

def drawFilledRectangle(x0,y0,x1,y1, *args, **kwargs):
       '''Draw a rectangle with bounding box ((x0,y0), (x1, y1))
       Assumes rectangle is with the axis boundaries
       Example: a yellow, translucent rectangle:
       drawFilledRectangle(0.25,0.25,.75,.75, color='yellow', alpha=.3)'''
       
       l = x1-x0
       h = y1-y0
       rect = pylab.Rectangle((x0,y0),l,h, *args, **kwargs)
       pylab.gca().add_patch(rect)


# uncomment and then run to see the example
#drawFilledRectangle(0.25,0.25,.75,.75, color='yellow', alpha=.3)
#pylab.show()
