from lib import snap
import sys
import time
import gmpy2
from lib import snapGraphCopy

# Consider every argument after the first (which is the name of the executed
# command) to be a graph file. Load them all and store them in a list.
def loadGraphs():
    Graphs = []
    for arg in sys.argv[1:]:
        Graphs.append(snap.LoadEdgeList(snap.PUNGraph, arg, 0, 1))
        sys.stdout.write("Imported " + arg + ": ")
        printQuickStats(Graphs[len(Graphs)-1])
    return Graphs

def loadDirGraphs():
    Graphs = []
    for arg in sys.argv[2:]:
        g = snap.LoadEdgeList(snap.PNGraph, arg, 0, 1)
        snap.MakeUnDir(g)
        Graphs.append(g)
        sys.stdout.write("Imported " + arg + ": ")
        printQuickStats(Graphs[len(Graphs)-1])
    return Graphs

def preprocess(Graphs):
    global numberOfNodes
    ##### preprocessing start #####
    # TODO: clean up the preprocessing, possibly make it into a new function

    v = []

    # appends node set for all graphs to v.
    for g in range(0,len(Graphs)):
        a = []
        for n in Graphs[g].Nodes():
            a.append(n.GetId())
        v.append(set(a))

    # take the intersection, giving us all common nodes.
    u = list(set.intersection(*v))

    # converts to a snap-vector
    w = snap.TIntV()
    for i in u:
        w.Add(i)

    # update graph list with subgraph induced by common nodes.
    for g in Graphs:
        subGraph(g, u)
    numberOfNodes = Graphs[0].GetNodes()

# TODO: Use snap.GetSubGraph() instead? It returned some sort of NoneType object
# when I tried. It gave the following error when calling GetNodes on the
# returned graph.
# AttributeError: 'NoneType' object has no attribute 'GetNodes'

    ##### preprocessing end #####

# Make g into an induced subgraph of g, removing all nodes that are not in v.
# Keep the list of nodes to remove in a list to avoid removing while iterating
# over the graph.
# This function is used because the one in snap would not work.
def subGraph(g, v):
    nodesToRemove = []
    for n in g.Nodes():
        if not n.GetId() in v:
            nodesToRemove.append(n.GetId())
    for n in nodesToRemove:
        g.DelNode(n)

# Find the node with the smallest degree. Uses the lookup table to avoid having
# to traverse the entire graph.
def findSmallestDegree(graphs):
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
    assert graphs[0].IsNode(smallestNode)
    return smallestNode

def getSmallestDegree(node):
    global degreeList
    deg = -1
    for n in range(0, len(degreeList)):
        deg = min(degreeList[n][node], deg)
    return deg

# Create the data structure that is used in the function findSmallestDegree().
# It is a list-of-lists, such that lookupTable[1] is a list of all nodes of
# degree 1 (as reported by getMinDegree()).
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

def removeFromLookupTable(graphs, node):
    global lookupTable
    degree = getMinDegree(graphs, node)
    if lookupTable[degree].count(node) > 0:
        lookupTable[degree].remove(node)

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

# Get the smallest degree of node, in all graphs.
def getMinDegree(graphs, node):
    result = float("Infinity")
    for g in graphs:
        assert g.IsNode(node)
        result = min(result, g.GetNI(node).GetDeg())
    return result

# Calculate the average degree as density of a single graph.
def density(n):
    global numberOfNodes
    global numberOfEdges
    return numberOfEdges[n]/float(numberOfNodes)

def quasiClique(n):
    global numberOfNodes
    global numberOfEdges
    return numberOfEdges[n]-(0.334*gmpy2.comb(numberOfNodes, 2))

def Clique(n):
    global numberOfNodes
    global numberOfEdges
    return numberOfEdges[n]/gmpy2.comb(numberOfNodes, 2)

# The density of a set of graphs is the minimum density among them.
def densityMultiple(graphs):
    result = float("Infinity")
    for g in range(0, len(graphs)):
        result = min(result, newDensity(g))
    return result

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

# Get the densest common subgraph using the greedy algorithm.
def getDCS_Greedy(originalGraphs):
    # Don't touch any of the original graphs, caller may use them further.
    graphs = []
    global numberOfNodes
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
        #removeSmallestDegreeNode(graphs)
        node = findSmallestDegree(graphs)
        numberOfNodes -= 1
        updateLists(graphs, node)
    print("Highest density found: " + str(highestDensity))

    # Pass 2, look for the subgraph that has a density equal to highest seen.
    graphs = []
    for og in originalGraphs:
        graphs.append(snapGraphCopy.copyGraph(og))
    initLookupTable(graphs)

    while graphs[0].GetNodes() > 1:
        # Is there a chance of some rounding error here? Comparing floats
        # without a margin of error. But they come from the same division.
        if densityMultiple(graphs) >= highestDensity:
            break
        removeSmallestDegreeNode(graphs)

    # TODO: which edges should be in the returned graph? Should we return the
    # full graph set?
    return (graphs[0], highestDensity)

# Find the node with the smallest degree and remove it. Also update the lookup
# table. The node that is removed from the graph must also be removed from the
# table, and all its neighbors must have their degree updated.
# TODO: Instead of removing and re-adding the nodes in the lookup table, how
# about just moving them one step up? The degree only changes by -1, right?
def removeSmallestDegreeNode(graphs):
    smallestNode = findSmallestDegree(graphs)
    neighbors = getNeighbors(graphs, smallestNode)
    removeFromLookupTable(graphs, smallestNode)
    for n in neighbors:
        removeFromLookupTable(graphs, n)
    for g in graphs:
        g.DelNode(smallestNode)
    for n in neighbors:
        addToLookupTable(graphs, n)

def updateLists(graphs, node):
    global takenTable
    global degreeList
    global lookupTable
    global numberOfEdges
    takenTable[node] = True
    for g in range(0, len(graphs)):
        nodeObj = graphs[g].GetNI(node)
        degree = nodeObj.GetDeg()
        numberOfEdges[g] -= degreeList[g][nodeObj.GetId()]
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

def printQuickStats(g):
    print(str(g.GetNodes()) + " nodes and " + str(g.GetEdges()) + " edges.")

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
  

timer() # Start the timer.
if(sys.argv[1] == "-d"):
    graphs = loadDirGraphs()
else:
    graphs = loadGraphs()

print("Imported " + str(len(graphs)) + " graphs in " + timer())

# If multiple graphs, do some preprocessing to make sure they are over the same
# set of nodes.
# Make sure all graphs have the same amount of nodes.
# There could be a deeper check here.
totalEdges = 0
for g in graphs:
    assert g.GetNodes() == graphs[0].GetNodes()
    totalEdges += g.GetEdges()
print(str(graphs[0].GetNodes()) + " nodes are common to all graphs")
print(str(totalEdges) + " total number of edges in all graphs")
print("Preprocessing took " + timer())

(g2, density) = getDCS_Greedy(graphs)
runTime = timer()
printQuickStats(g2)
print("The greedy algorithm completed in " + runTime)
saveResults(g2, runTime, density)
