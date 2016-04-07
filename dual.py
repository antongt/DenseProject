# This is the dual of the LP for the finding of the densest subgraph.

from lib import snap
import sys
import time
from lib import snapGraphCopy

# Consider every argument after the first (which is the name of the executed
# command) to be a graph file. Load them all and store them in a list.
def loadGraphs():
    Graphs = []
    for arg in sys.argv[1:]:
        Graphs.append(snap.LoadEdgeList(snap.PUNGraph, arg, 0, 1))
        sys.stderr.write("Imported " + arg + "\n")
    return Graphs


def loadDirGraphs():
    Graphs = []
    for arg in sys.argv[2:]:
         g = snap.LoadEdgeList(snap.PNGraph, arg, 0, 1)
         snap.MakeUnDir(g)
         Graphs.append(g)
         sys.stderr.write("Imported " + arg + "\n")
    return Graphs


# Print the dual. All other output is to stderr, so that the output
# of this script can be redirected to a file.
def printDualLP(graphs):
    # Build a list of all the variables.
    primalVars = [] # xs, ys, t.
    for gi in range(0, len(graphs)):
        for e in graphs[gi].Edges():
            varName = "x_"+str(gi)+"_"+str(e.GetSrcNId())+"_"+str(e.GetDstNId())
            primalVars.append(varName)
        for node in graphs[gi].Nodes():
            varName = "y_" + str(node.GetId())
            if not varName in primalVars:
                primalVars.append(varName)

    # The primal is a maximization problem, to this is a minimization.
    sys.stdout.write("minimize")
    # Write all the terms of the objective function.
    # * Write a plus sign before every term except the first.
    # * Write a newline after every maxColumns terms.
    firstTerm = True
    currentColumn = 1
    maxColumns = 6
    for yvar in y:
        if not firstTerm:
            sys.stdout.write(" +")
        else:
            firstTerm = False
        sys.stdout.write(" y" + str(yvar))
        currentColumn += 1
        if currentColumn % maxColumns == 0:
            sys.stdout.write("\n")
    print(";")
    # First set of constraints correspond to x_ij in each graph.
    #for graphNum in range(0, len(x)):
    #    for xvar in x[graphNum]:

    sys.stdout.write("\nend\n")


# Program starts here.
# Check command line parameters.
if(len(sys.argv) < 2):
  sys.exit("Usage: python " + sys.argv[0] + " <file1> <file2> ...")
# Import data.
if(sys.argv[1] == "-d"):
    graphs = loadDirGraphs()
else:
    graphs = loadGraphs()
sys.stderr.write("Imported " + str(len(graphs)) + " graphs.\n")
# Print the LP of the dual problem.
printDualLP(graphs)

