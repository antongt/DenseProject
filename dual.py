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
    y = [] # nodes. common to all graphs.
    x = [] # edges. one list for each graph.
    for gi in range(0, len(graphs)):
        x.append([])
        for edge in graphs[gi].Edges():
            x[gi].append((edge.GetSrcNId(), edge.GetDstNId()))
        for node in graphs[gi].Nodes():
            nid = node.GetId()
            if not nid in y:
                y.append(nid)
    if(False):
        print("X:")
        for listnum in range(0, len(x)):
            for xvar in x[listnum]:
                print(str(listnum) + ", " + str(xvar[0]) + ", " + str(xvar[1]))
        print("Y:")
        for yvar in y:
            print(str(yvar))
    # The primal is a maximization problem, to this is a minimization.
    sys.stdout.write("minimize")
    column = 1
    first = True
    for yvar in y:
        if first:
            first = False
        else:
            sys.stdout.write(" +")
        sys.stdout.write(" y" + str(yvar))
        column += 1
        if column % 6 == 0: # Line break after every N terms.
            sys.stdout.write("\n")
    print(";")

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

