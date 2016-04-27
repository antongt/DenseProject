import sys
from lib import snap
from lib import snapGraphCopy
from lib import triangleDensity

def loadGraphs(locations):
      graphs = []
      for arg in locations:
          graphs.append(snap.LoadEdgeList(snap.PUNGraph, arg, 0, 1))
      return graphs

graphs = loadGraphs(sys.argv[1:-1])
subgraphNodes = open(sys.argv[-1]).read()
subgraphNodes = subgraphNodes.split("\n")
nodes = snap.TIntV()
for i in range(0,len(subgraphNodes)-1):
    if(subgraphNodes[i][0] != '#'):
        nodes.Add(int(subgraphNodes[i]))

leastDense = 0
smallestNumberOfEdges = sys.maxint
for g in range(0,len(graphs)):
    graphs[g] = snap.GetSubGraph(graphs[g],nodes)
    edges = graphs[g].GetEdges()
    if (smallestNumberOfEdges>edges):
        leastDense = g
        smallestNumberOfEdges = edges
print ("number of edges: " + str(smallestNumberOfEdges))
print "calculating diameter"
diam = snap.GetBfsFullDiam(graphs[leastDense], 100)
print "calculating clustering coef"
cc = snap.GetClustCf(graphs[leastDense])
print "calculating percentage of clique"
precentOfClique = smallestNumberOfEdges/((len(nodes)-1)*len(nodes)/2.0)
print "calculating triangle density"
triDensity = triangleDensity.triangleDensity(graphs[leastDense])

print("diam: " + str(diam) + "\ncc: " + str(cc) + "\npercent of clique: " + str(precentOfClique)
      + "\ntriangle density " + str(triDensity))
