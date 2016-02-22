from lib import snap
import sys
import time
import snapGraphCopy

# Consider every argument after the first (which is the name of the executed
# command) to be a graph file. Load them all and store them in a list.
def loadGraphs():
    Graphs = []
    for arg in sys.argv[1:]:
        Graphs.append(snap.LoadEdgeList(snap.PUNGraph, arg, 0, 1))
        sys.stdout.write("Imported " + arg + ": ")
        printQuickStats(Graphs[len(Graphs)-1])
    return Graphs

def preprocess(Graphs):
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

# Find the node with the smallest degree.
def findSmallestDegree(graphs):
    smallestDegree = float("Infinity")
    smallestNode = float("NaN")
    for n in graphs[0].Nodes():
        degree = getDegree(graphs, n.GetId())
        if degree < smallestDegree:
            smallestDegree = degree
            smallestNode = n.GetId()
    return smallestNode

# Get the smallest degree of node, in all graphs.
def getDegree(graphs, node):
    result = float("Infinity")
    for g in graphs:
        assert g.IsNode(node)
        result = min(result, g.GetNI(node).GetDeg())
    return result

# Calculate the average degree as density of a single graph.
def density(g):
    # Avoid division by zero.
    if g.GetNodes() == 0:
        return 0
    else:
        return g.GetEdges()/float(g.GetNodes())

# The density of a set of graphs is the minimum density among them.
def densityMultiple(graphs):
    result = float("Infinity")
    for g in graphs:
        result = min(result, density(g))
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
    for og in originalGraphs:
        graphs.append(snapGraphCopy.copyGraph(og))
    # To avoid having to do two full passes over the entire graph, we keep
    # track of a set of nodes that we know contains the densest subgraph. The
    # trick is to make it as small as possible while also minimizing the number
    # of updates.
    searchSpace = []
    for n in graphs[0].Nodes():
        searchSpace.append(n.GetId())

    # Pass 1, to find the subgraph with the highest density.
    highestDensity = 0
    updatesSinceSave = 0
    while graphs[0].GetNodes() > 1:
        printProgress("Searching for highest density: ",
                originalGraphs[0].GetNodes(), graphs[0].GetNodes())
        if densityMultiple(graphs) > highestDensity:
            highestDensity = densityMultiple(graphs)
            updatesSinceSave += 1
            if updatesSinceSave >= 100:
                updatesSinceSave = 0
                searchSpace = []
                for n in graphs[0].Nodes():
                    searchSpace.append(n.GetId())
        removeSmallestDegreeNode(graphs)

    print("Highest density found: " + str(highestDensity))

    # Pass 2, look for the subgraph that has a density equal to highest seen.
    # Since we start from a much smaller search space, this can be very fast.
    print("Going back to find best solution. Search space is " +
            str(len(searchSpace)) + " nodes")
    graphs = []
    for og in originalGraphs:
        graphs.append(snapGraphCopy.copyGraph(og))
    for g in graphs:
        subGraph(g, searchSpace)

    while graphs[0].GetNodes() > 1:
        # Is there a chance of some rounding error here? Comparing floats
        # without a margin of error. But they come from the same division.
        if densityMultiple(graphs) >= highestDensity:
            break
        removeSmallestDegreeNode(graphs)

    # TODO: which edges should be in the returned graph? Should we return the
    # full graph set?
    return graphs[0]

def removeSmallestDegreeNode(graphs):
    smallestNode = findSmallestDegree(graphs)
    for g in graphs:
        g.DelNode(smallestNode)

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
# TODO: buggy. does not save the file.
def saveResults(graph, runTime):
    fileName = "greedy-out.tmp"
    print("Saving as " + fileName)
    description = "Densest subgraph by greedy algorithm, completed in " + runTime
    snap.SaveEdgeList(graph, fileName)
    #snap.SaveEdgeList(graph, fileName, description)

if(len(sys.argv) < 2):
  sys.exit("Usage: python " + sys.argv[0] + " <file1> <file2> ...")

timer() # Start the timer.
graphs = loadGraphs()
print("Imported " + str(len(graphs)) + " graphs in " + timer())

print("Preprocessing...")
preprocess(graphs)
# Make sure all graphs have the same amount of nodes. There could be a deeper
# check here.
for g in graphs:
    assert g.GetNodes() == graphs[0].GetNodes()
print(str(graphs[0].GetNodes()) + " nodes are common to all graphs")
print("Preprocessing took " + timer())

g2 = getDCS_Greedy(graphs)
runTime = timer()
printQuickStats(g2)
print("The greedy algorithm completed in " + runTime)
saveResults(g2, runTime)

