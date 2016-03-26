from lib import snap
import sys
import os
# Verifies the density of a snapGraph produced by
# logTosnap.py . 
# The program checks the following things
# - Graph is connected
# If the graph is connected it prints the 
# density e.g 
#   #edges / #nodes 
# to stdout
#
def usage():
  sys.exit("usage: python verify.py <snapGraph.txt>")

if len(sys.argv) < 2 :
  usage()
name,ext = os.path.splitext(sys.argv[1])
if ext != ".txt":
  usage()

g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)

a = snap.TIntV()
for i in g.Nodes() : 
  a.Add(i.GetId())
# get Input Graph stats
e = g.GetEdges()
n = g.GetNodes()  
# Get induced subgraph
g0  = snap.GetSubGraph(g,a)
# Get its stats
e0 = g0.GetEdges()
n0 = g0.GetNodes()

if e == e0 and n == n0:
  print "Graph is connected!"
  print "#Edges: %d, #Nodes: %d " % (e,n)
  print "Density of graph is #eges / #nodes: %.9f" % (e / float(n))
else:
  print "Graph is NOT Connected"


