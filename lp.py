from lib import snap
import sys
import time
import os
import cplex


def main(argv):
  asUnDir = False
  oneGraph = False
  
  if(len(argv) < 2):
    sys.exit("usage: python lp.py [-d] <file1> ... <fileN>")

  if(len(argv) == 2):
    if argv[1] == "-d":
      sys.exit("no input.")
    oneGraph = True

  if(len(argv) == 3 and argv[1] == "-d"):
    asUnDir = True
    oneGraph = True

  if(len(argv) > 3 and argv[1] == "-d"):
    asUnDir = True
  if(oneGraph):
    if(asUnDir):
      Graph = snap.LoadEdgeList(snap.PNGraph, argv[2], 0, 1)
      snap.MakeUnDir(Graph)
    else:
      Graph = snap.LoadEdgeList(snap.PUNGraph, argv[1], 0, 1)
    printSingleGraph(Graph)
  else:
    Graphs = []
    if(asUnDir):
      for file in argv[2:]:
        g = snap.LoadEdgeList(snap.PNGraph, file, 0, 1)
        snap.MakeUnDir(g)
        Graphs.append(g)
    else:
      for file in argv[1:]:
        Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
    printMoreGraphs(Graphs)


  dense = cplex.Cplex("dense.lp")
  os.remove("dense.lp")
  alg = dense.parameters.lpmethod.values
  dense.parameters.lpmethod.set(alg.barrier)
# include the below line to not do the crossover and get a close
# but not exact solution that can be extracted with filterLpSolution
#  dense.parameters.barrier.crossover.set(-1)
  startTime = time.clock()
  #dense.parameters.lpmethod.set(5) # sifting algorithm
  dense.solve()
 
  print("time taken: " + str(time.clock()-startTime))
  
  print "The solution is", dense.solution.get_status_string()
  print "Density:", dense.solution.get_objective_value()

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

if __name__ == "__main__":
    main(sys.argv)

