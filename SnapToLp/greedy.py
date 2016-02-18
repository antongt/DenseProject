import snap
import sys;

#if(len(sys.argv) != 3):
#  sys.exit("usage: python snapToLp2.py <file1> <file2>")

def findSmallestDegree(g):
    smallestDegree = -1
    smallestNode = -1
    for n in g.Nodes():
        if smallestDegree == -1 or n.GetId() < smallestDegree:
            smallestDegree = n.GetDeg()
            smallestNode = n.GetId()
    return smallestNode

def removeSmallestDegree(g):
    g.DelNode(findSmallestDegree(g))

def density(g):
    # Avoid division by zero.
    if g.GetNodes() == 0:
        return 0
    else:
        return g.GetEdges()/(1.0*g.GetNodes())

def printProgress(originalSize, currentSize):
    if currentSize%(originalSize/100) == 0:
        percentage = 100*(originalSize-currentSize)/originalSize
        print(str(percentage) + "%")

# TODO: save the actual graph
def getHighestDensity(g):
    originalSize = g.GetNodes()
    highestDensity = 0
    while g.GetNodes() > 0:
        printProgress(originalSize, g.GetNodes())
        removeSmallestDegree(g)
        if density(g) > highestDensity:
            highestDensity = density(g)
    return highestDensity

# BUG? copy of graphs?
def getDensestSubgraph(g):
    originalSize = g.GetNodes()
    highestDensity = getHighestDensity(g)
    while g.GetNodes() > 0:
        printProgress(originalSize, g.GetNodes())
        removeSmallestDegree(g)
        if density(g) >= highestDensity:
            break
    return g

g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)

print("The graph has " + str(g.GetNodes()) + " nodes and " + str(g.GetEdges()) + " edges.")
g2 = getDensestSubgraph(g)
print("The densest subgraph has " + str(g2.GetNodes()) + " nodes and " + str(g2.GetEdges()) + " edges.")



