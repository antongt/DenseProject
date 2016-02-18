import snap
import sys
import time
import snapGraphCopy

#if(len(sys.argv) != 3):
#  sys.exit("usage: python snapToLp2.py <file1> <file2>")

# Find the node with the smallest degree.
# TODO, some way of sorting the nodes so that it's not needed to look through
# the entire graph every time.
def findSmallestDegree(g):
    smallestDegree = g.GetEdges() + 1
    smallestNode = -1
    for n in g.Nodes():
        if n.GetDeg() < smallestDegree:
            smallestDegree = n.GetDeg()
            smallestNode = n.GetId()
    return smallestNode

# Calculate the average degree as density.
def density(g):
    # Avoid division by zero.
    if g.GetNodes() == 0:
        return 0
    else:
        return g.GetEdges()/(1.0*g.GetNodes())

# Print progress bar based on size of the graph (it is reduced to zero nodes).
def printProgress(message, originalSize, currentSize):
    if currentSize%(originalSize/10) == 0:
        percentage = 100*(originalSize-currentSize)/originalSize
        print(message + str(percentage) + "%")

def getDensestSubgraphGreedy(original):
    # Don't touch the original, caller may use it further.
    copy = snapGraphCopy.copyGraph(original)
    # Keep track of a copy that we know contains the densest subgraph. The trick
    # is to make it as small as possible while also minimizing the number of
    # graph copies (deep copies are heavy).
    searchSpace = snapGraphCopy.copyGraph(copy)

    # Pass 1, to find the subgraph with the highest density.
    highestDensity = 0
    updatesSinceSave = 0
    while copy.GetNodes() > 0:
        printProgress("Searching for highest density: ", original.GetNodes(), copy.GetNodes())
        copy.DelNode(findSmallestDegree(copy))
        if density(copy) > highestDensity:
            highestDensity = density(copy)
            updatesSinceSave += 1
            if updatesSinceSave >= 100:
                updatesSinceSave = 0
                searchSpace = snapGraphCopy.copyGraph(copy)
    print("Highest density found: " + str(highestDensity))

    # Pass 2, look for the subgraph that has a density equal to highest seen.
    # Since we start from a much smaller search space, this can be very fast.
    while searchSpace.GetNodes() > 0:
        searchSpace.DelNode(findSmallestDegree(searchSpace))
        # Is there a chance of some rounding error here? Comparing floats
        # without a margin of error. But they come from the same division.
        if density(searchSpace) >= highestDensity:
            break
    return searchSpace

def printQuickStats(g):
    print(str(g.GetNodes()) + " nodes and " + str(g.GetEdges()) + " edges.")

g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
print("Input graph has:")
printQuickStats(g)

# Time how long it takes.
startTime = time.clock()
g2 = getDensestSubgraphGreedy(g)
runningTime = time.clock() - startTime

printQuickStats(g2)
print("The greedy algorithm took " + str(runningTime) + " seconds.")

# Save the results.
outFileName = "greedy-out.tmp"
print("Saving as " + outFileName)
snap.SaveEdgeList(g2, outFileName, "Densest subgraph by greedy algorithm.")

