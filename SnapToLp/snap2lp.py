from lib import snap;
import sys;

oneGraph = False

if(len(sys.argv) < 2):
  sys.exit("usage: python snap2lp.py <file1> ... <fileN>")
if(len(sys.argv) == 2):
  oneGraph = True



def printSingleGraph(Graph):
  edges = []
  nodes = []
  edgeCons = []

  for e in Graph.Edges():
    src = e.GetSrcNId()
    dst = e.GetDstNId()
    xij = "x"+str(src)+str(dst)
    yi  = "y"+str(src)
    yj  = "y"+str(dst)
    edges.append(xij)
    edgeCons.append(xij+" - "+yi+" <= 0")
    edgeCons.append(xij+" - "+yj+" <= 0")

  for n in Graph.Nodes():
    id = n.GetId()
    yi = "y"+str(id)
    nodes.append(yi)

  print "maximize"
  print " +\n".join(edges) # sum xij
  print "\nsubject to"
  print (" +\n".join(nodes))+" <= 1" # sum yi <= 1
  print " \n".join(edgeCons) # xij <= yi and xij <= yj
  print (" >= 0\n".join(edges))+" >= 0" # xij >= 0
  print (" >= 0\n".join(nodes))+" >= 0" # yi  >= 0
  print "\nend"
  return;

def printMoreGraphs(Graphs):
  nodes = []
  allEdges = []
  allEdgeCons = []
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
  for g in range(0,len(Graphs)):
    Graphs[g] = snap.GetSubGraph(Graphs[g],w)

##### preprocessing end #####


  for g in range(0,len(Graphs)):
    edges    = []
    edgeCons = []
    for e in Graphs[g].Edges():
      src = e.GetSrcNId()
      dst = e.GetDstNId()
      xij = "x"+str(g)+"_"+str(src)+str(dst)
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

  print "maximize t"
  print "\nsubject to"
  print (" +\n".join(nodes))+" <= 1" # sum yi <= 1
  print (" >= 0\n".join(nodes))+" >= 0" # yi  >= 0
  for e in allEdges:
    print (" +\n".join(e))+" - t >= 0" # sum xij >= t
    print (" >= 0\n".join(e))+" >= 0" # xij >= 0
  for c in allEdgeCons:
    print " \n".join(c) # xij <= yi and xij <= yj
  print "\nend"


if(oneGraph):
  Graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
  printSingleGraph(Graph)
else:
  Graphs = []
  for i in range(1,len(sys.argv)):
    Graphs.append(snap.LoadEdgeList(snap.PUNGraph, sys.argv[i], 0, 1))
  printMoreGraphs(Graphs)
