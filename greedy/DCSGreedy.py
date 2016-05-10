from lib import snapGraphCopy
from greedy import utils, densityGreedy


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
    HighestNode = 0
    # finds the largest node incase not all node sets are identical
    for g in range(0, len(graphs)):
        HighestNode = max(graphs[g].GetMxNId(),HighestNode)
    # initialize takentable to all nodes not taken
    for i in range(0,HighestNode):
        takenTable.append(False)
    # creates a lookuptable for every graph
    for g in range(0, len(graphs)):
        degreeList.append([])
        for i in range(0,HighestNode):
            degreeList[g].append(0)
        numberOfEdges.append(graphs[g].GetEdges())
        for n in graphs[g].Nodes():
            degreeList[g][n.GetId()] = n.GetDeg()
            addToLookupTable(n.GetId(), n.GetDeg())

def addToLookupTable(node,degree):
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
def getDCS_Greedy(graphs,nodes):
    global numberOfNodes
    global numberOfEdges
    numberOfNodes = len(nodes)
    # Create a table of nodes by degree, to enable faster lookup.
    utils.timer()
    initLookupTable(graphs)
    print("initilization took " + str(utils.timer()))
    # Pass 1, to find the subgraph with the highest density.
    highestDensity = 0
    originalNumberOfNodes = numberOfNodes
    while numberOfNodes > 1:
        #printProgress("Searching for highest density: ",
        #    originalGraphs[0].GetNodes(), graphs[0].GetNodes())
        currDensity = densityMultiple(graphs)
        if (highestDensity < currDensity):
            highestDensity = currDensity
            optimalNumberOfNodes = numberOfNodes
        node = takeSmallestDegree(graphs)
        numberOfNodes -= 1
        updateLists(graphs, node)
    print("first pass took: " + str(utils.timer()))
    print("Highest density found: " + str(highestDensity))
    # Pass 2, look for the subgraph that has a density equal to highest seen.
    numberOfNodes = originalNumberOfNodes
    initLookupTable(graphs)
    while numberOfNodes > optimalNumberOfNodes:
        node = takeSmallestDegree(graphs)
        numberOfNodes -=1
        updateLists(graphs,node)

    nodesInSubGraph = getNodesInSubGraph(nodes)
    print("second pass took: " + str(utils.timer()))
    print("we found a total number of nodes = " + str(optimalNumberOfNodes))
    return (nodesInSubGraph,highestDensity)

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

def getNodesInSubGraph(nodes):
    global takenTable
    exists = []
    for i in nodes:
        if not takenTable[i]:
            exists.append(i)
    return exists
