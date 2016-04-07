from lib import snap
import sys
import os
import cplex

if(len(sys.argv) < 2):
  sys.exit("usage: python lan.py <file1> ... <fileN>")

def printSingleGraph(Graph, filename="lp.lp"):
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

  with open(filename, "w") as f:
    print >> f, "maximize"
    print >> f, " +\n".join(edges) # sum xij
    print >> f, "\nsubject to"
    print >> f, (" +\n".join(nodes))+" <= 1" # sum yi <= 1
    print >> f, " \n".join(edgeCons) # xij <= yi and xij <= yj
    print >> f, "\nend"
  return;

Graphs = []
nameList = []
i = 0
for file in sys.argv[1:]:
  g = snap.LoadEdgeList(snap.PUNGraph, file, 0, 1)
  Graphs.append(g)
  lpName = "lp_"+str(i)+".lp"
  nameList.append(lpName)
  printSingleGraph(g, lpName)
  i+=1

print nameList

totaltime = 0
denseList = []
for file in nameList:
  dense = cplex.Cplex(file)
  os.remove(file)
  alg = dense.parameters.lpmethod.values
  dense.parameters.lpmethod.set(alg.barrier)
  start = dense.get_time()
  dense.solve()
  end = dense.get_time()
  totaltime += (end - start)
  density = dense.solution.get_objective_value()
  denseList.append(density)

print denseList
print "solution: "+str(min(denseList))
print "total solve time: "+str(totaltime)+" sec."
