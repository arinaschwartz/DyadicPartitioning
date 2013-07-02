import sys
import os

class FatalError:
    def __init__(self, msg):
        self.msg = msg

def handleRow(row):
    try:
        return map(lambda x: float(x), row.strip().split(","))
    except ValueError:
        raise FatalError("Format error: " + ",".row)


def readData(fn):
    try:
        data = [handleRow(row) for row in open(fn)]
        return data
    except IOError:
        raise FatalError("Error: cannot open file " + fn)


def go(trainingFn, testingFn, lambda0, level):
    try:
        data = readData(trainingFn)
    except FatalError, err:
        print >>sys.stderr, err.msg
        return 2


if __name__=="__main__":
    progName = sys.argv[0]
    usageMsg = "usage: python " + progName + " <training file name> <testing filename> <lambda> <max level>"

    numArgs = len(sys.argv)
    try:
        if numArgs == 3:
            trainingFn = "version1/spiral/training.csv"
            testingFn = "version1/spiral/testing.csv"
            nextArg = 1
        elif numArgs == 5:
            trainingFn = sys.argv[1]
            testingFn = sys.argv[2]
            nextArg = 3
        else:
            print >>sys.stderr, usageMsg
            sys.exit(2)

        lambda0 = int(sys.argv[nextArg])
        level = int(sys.argv[nextArg+1])
        go(trainingFn, testingFn, lambda0, level)
    except ValueError:
        print >>sys.stderr, usageMsg
        sys.exit(1)


        
     
