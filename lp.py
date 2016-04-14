from lib import snap
import sys
import os
import cplex

oneGraph = False

if(len(sys.argv) < 2):
  sys.exit("usage: python lp.py <file1> ... <fileN>")

if(len(sys.argv) == 2):
  oneGraph = True

def printSingleGraph(Graph):
  edges = []
  nodes = []
  edgeCons = []

  for e in Graph.Edges():
    src = e.GetSrcNId()
    dst = e.GetDstNId()
    xij = "x"+str(src)+"#"+str(dst)
    yi  = "y"+str(src)
    yj  = "y"+str(dst)
    edges.append(xij)
    edgeCons.append(xij+" - "+yi+" <= 0")
    edgeCons.append(xij+" - "+yj+" <= 0")

  for n in Graph.Nodes():
    id = n.GetId()
    yi = "y"+str(id)
    nodes.append(yi)

  with open("dense.lp", "w") as f:
    print >> f, "maximize"
    print >> f, " +\n".join(edges) # sum xij
    print >> f, "\nsubject to"
    print >> f, (" +\n".join(nodes))+" <= 1" # sum yi <= 1
    print >> f, " \n".join(edgeCons) # xij <= yi and xij <= yj
    print >> f, "\nend"
  return;

def printMoreGraphs(Graphs):
  nodes = []
  allEdges = []
  allEdgeCons = []

  for g in range(0,len(Graphs)):
    edges    = []
    edgeCons = []
    for e in Graphs[g].Edges():
      src = e.GetSrcNId()
      dst = e.GetDstNId()
      xij = "x"+str(g)+"_"+str(src)+"#"+str(dst)
      yi  = "y"+str(src)
      yj  = "y"+str(dst)
      edges.append(xij)
      edgeCons.append(xij+" - "+yi+" <= 0")
      edgeCons.append(xij+" - "+yj+" <= 0")
    for n in Graphs[g].Nodes():
      id = n.GetId()
      yi = "y"+str(id)
      nodes.append(yi)
    allEdges.append(edges)
    allEdgeCons.append(edgeCons)

  # remove duplicates
  nodes = list(set(nodes))

  with open("dense.lp", "w") as f:
    print >> f, "maximize t"
    print >> f, "\nsubject to"
    print >> f, (" +\n".join(nodes))+" <= 1" # sum yi <= 1
    for e in allEdges:
      print >> f, (" +\n".join(e))+" - t >= 0" # sum xij >= t
    for c in allEdgeCons:
      print >> f, " \n".join(c) # xij <= yi and xij <= yj
    print >> f, "\nend"


print "Warning: This file assumes already preprocessed files,"
print "         meaning the input should be undirected and"
print "         all node-sets should be equal, see preprocess.py.\n"
if(oneGraph):
  Graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
  printSingleGraph(Graph)
else:
  Graphs = []
  for file in sys.argv[1:]:
    Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
  printMoreGraphs(Graphs)


dense = cplex.Cplex("dense.lp")
os.remove("dense.lp")
alg = dense.parameters.lpmethod.values
dense.parameters.lpmethod.set(alg.barrier)
dense.parameters.barrier.crossover.set(dense.parameters.barrier.crossover.values.none)
dense.solve()
