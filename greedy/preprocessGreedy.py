import sys
from lib import snap
from lib import snapGraphCopy


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


# If multiple graphs, do some preprocessing to make sure they are over the same
# set of nodes.
# Make sure all graphs have the same amount of nodes.
# There could be a deeper check here.
def simplePreprocessing(graphs):
    numberOfNodes = 0;
    totalEdges = 0
    for g in graphs:
        # assert g.GetNodes() == numberOfNodes
        numberOfNodes = max(numberOfNodes,g.GetNodes())
        totalEdges += g.GetEdges()
    print(str(numberOfNodes) + " nodes are common to all graphs")
    print(str(totalEdges) + " total number of edges in all graphs")
    return numberOfNodes

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

def printQuickStats(g):
    print(str(g.GetNodes()) + " nodes and " + str(g.GetEdges()) + " edges.")
