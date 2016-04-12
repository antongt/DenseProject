from lib import snap
import sys
import time
from greedy import preprocessGreedy
from greedy import densityGreedy
from lib import snapGraphCopy

# Create the data structure that is used in the function findSmallestDegree().
# It is a list-of-lists, such that lookupTable[1] is a list of all nodes of
# degree 1.
def initLookupTable(graphs):
    global lookupTable
    global degreeList
    global takenTable
    global numberOfEdges
    degreeList = []
    lookupTable = []
    takenTable = []
    numberOfEdges = []
    for i in range(0,graphs[0].GetMxNId()):
        takenTable.append(False)
    for g in range(0, len(graphs)):
        degreeList.append([])
        for i in range(0,graphs[0].GetMxNId()):
            degreeList[g].append(0)
        numberOfEdges.append(graphs[g].GetEdges())
        for n in graphs[g].Nodes():
            degreeList[g][n.GetId()] = (n.GetDeg())
            addToLookupTable(graphs, n.GetId(), n.GetDeg())

def addToLookupTable(graphs, node,degree):
    global lookupTable
    while degree >= len(lookupTable):
        lookupTable.append([])
    lookupTable[degree].append(node)


# Find the node with the smallest degree and removes it from the list
# If it has already been removed a new node is taken until a real node
# is found. That number is returned.
def takeSmallestDegree(graphs):
    global lookupTable
    global takenTable
    global numberOfNodes
    degree = 0
    while True:
        while (len(lookupTable[degree]) == 0):
            degree += 1
        smallestNode = lookupTable[degree].pop()
        if (not takenTable[smallestNode]):  # make takenTable hashtable or similar or create larger table
            break
    # assert graphs[0].IsNode(smallestNode)
    return smallestNode

# The density of a set of graphs is the minimum density among them.
def densityMultiple(graphs):
    global numberOfNodes
    global numberOfEdges
    result = float("Infinity")
    for g in range(0, len(graphs)):
        result = min(result, densityGreedy.density(numberOfEdges[g],numberOfNodes))
    return result


# Get the densest common subgraph using the greedy algorithm.
def getDCS_Greedy(originalGraphs):
    # Don't touch any of the original graphs, caller may use them further.
    graphs = []
    global numberOfNodes
    global numberOfEdges
    for og in originalGraphs:
        graphs.append(snapGraphCopy.copyGraph(og))
    # Create a table of nodes by degree, to enable faster lookup.
    initLookupTable(graphs)

    # Pass 1, to find the subgraph with the highest density.
    highestDensity = 0
    while numberOfNodes > 1:
        printProgress("Searching for highest density: ",
            originalGraphs[0].GetNodes(), graphs[0].GetNodes())
        highestDensity = max(highestDensity, densityMultiple(graphs))
        node = takeSmallestDegree(graphs)
        numberOfNodes -= 1
        updateLists(graphs, node)
    print("Highest density found: " + str(highestDensity))
    print("number of edges left " + str(numberOfEdges))
    # Pass 2, look for the subgraph that has a density equal to highest seen.

    return (None,highestDensity)


def updateLists(graphs, node):
    global takenTable
    global degreeList
    global lookupTable
    global numberOfEdges
    takenTable[node] = True
    for g in range(0, len(graphs)):
        if (graphs[g].IsNode(node)):
            nodeObj = graphs[g].GetNI(node)
            degree = nodeObj.GetDeg()
            numberOfEdges[g] -= degreeList[g][node] # remove edges equal to the nodes current degree
            for edgeNum in range(0, degree):
                neighbourNode = nodeObj.GetNbrNId(edgeNum)
                if not takenTable[neighbourNode]:
                    degreeList[g][neighbourNode] -= 1
                    lookupTable[degreeList[g][neighbourNode]].append(neighbourNode)

# Return a list of all nodes connected to node, in any of the graphs.
def getNeighbors(graphs, node):
    neighbors = []
    for g in graphs:
        assert g.IsNode(node)
        degree = g.GetNI(node).GetDeg()
        for edgeNum in range(0, degree):
            neighbor = g.GetNI(node).GetNbrNId(edgeNum)
            if not neighbor in neighbors:
                neighbors.append(neighbor)
    return neighbors

# A function to measure how long something takes to run.
# Returns a string holding the time since last time the function was called.
# Uses a global variable to hold the time of previous call.
def timer():
    global lastTimeStamp
    try:
        elapsedTime = time.clock() - lastTimeStamp
    except NameError:
        # First time the function is called there is no startTime declared.
        elapsedTime = 0
    lastTimeStamp = time.clock()
    return '%.1f seconds' % elapsedTime

# Print progress bar based on size of the graph (it is reduced to zero nodes).
def printProgress(message, originalSize, currentSize):
    global lastUpdateTimeStamp
    updateFrequency = 10 # Update progress every X seconds.
    try:
        if time.clock() - lastUpdateTimeStamp < updateFrequency:
            return
    except NameError:
        lastUpdateTimeStamp = time.clock()
    lastUpdateTimeStamp = time.clock()
    percentage = '%.0f' % (100*(originalSize-currentSize)/(1.0*originalSize))
    print(message + percentage + "% done")

# For debugging. Use with tiny graphs only.
def printLookupTable():
    global lookupTable
    deg = 0
    for degreeList in lookupTable:
        sys.stdout.write(str(deg) + ": ")
        for node in degreeList:
            sys.stdout.write(str(node) + " ")
        print("")
        deg += 1

# Save the results to a snap graph file.
# TODO: why does snap.SaveEdgeList not save the file?
# TODO: what are we actually saving? Nodes, edges, density?
def saveResults(graph, runTime, density):
    fileName = "greedy-out.tmp"
    print("Saving as " + fileName)
    description = "Densest subgraph by greedy algorithm, completed in " + runTime
    #snap.SaveEdgeList(graph, fileName, description)
    # Write the nodes into a list so that they can be sorted.
    nodeList = []
    for n in graph.Nodes():
        nodeList.append(n.GetId())
    nodeList.sort()

    f = open(fileName, 'w')
    f.write('# Node list of the densest common subgraph of the following graphs:\n')
    for arg in sys.argv[1:]:
        f.write('#   ' + arg + '\n')
    f.write('# Number of nodes: ' + str(len(nodeList)) + '\n')
    f.write('# Density: ' + str(density) + '\n')
    f.write('# Completed in ' + runTime + '\n')
    for n in nodeList:
        f.write(str(n) + '\n')


if(len(sys.argv) < 2):
  sys.exit("Usage: python " + sys.argv[0] + " <file1> <file2> ...")
  
global numberOfNodes
timer() # Start the timer.
if(sys.argv[1] == "-d"):
    graphs = loadDirGraphs()
else:
    graphs = preprocessGreedy.loadGraphs()

print("Imported " + str(len(graphs)) + " graphs in " + timer())
# Don't remove, this isn't the deep preprocessing that takes time.
numberOfNodes = preprocessGreedy.simplePreprocessing(graphs)

# If multiple graphs, do some preprocessing to make sure they are over the same
# set of nodes.
# Make sure all graphs have the same amount of nodes.
# There could be a deeper check here.
totalEdges = 0
for g in graphs:
    # assert g.GetNodes() == graphs[0].GetNodes()
    totalEdges += g.GetEdges()
print(str(graphs[0].GetNodes()) + " nodes are common to all graphs")
print(str(totalEdges) + " total number of edges in all graphs")

print("Preprocessing took " + timer())

(g2, density) = getDCS_Greedy(graphs)
runTime = timer()
# printQuickStats(g2)
print("The greedy algorithm completed in " + runTime)
#saveResults(g2, runTime, density)
