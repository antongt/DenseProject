import snap;
import sys;

if(len(sys.argv) != 2):
  sys.exit("usage: python snapToLp.py <file>")

Graph = snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1)
snap.MakeUnDir(Graph)
#for n in Graph.Nodes():

print "Maximize"
b = " "
for e in Graph.Edges():
  b = b + ("\nx"+''.join(map(str,e.GetId()))+" + ")

b = b[:-2]
print b

print "Subject to"
for e in Graph.Edges():
  nodesrc = e.GetSrcNId()
  nodedst = e.GetDstNId()
  edgeId  = ''.join(map(str,e.GetId()))
  print " x"+edgeId+" - y"+str(nodesrc) + " <= 0"
  print " x"+edgeId+" - y"+str(nodedst) + " <= 0"
  print " x"+edgeId+" >= 0"

a = " "
for n in Graph.Nodes():
  print "\ny"+str(n.GetId())+" >= 0"
  a = a + ("y"+str(n.GetId())+" + ")

a = a[:-2]
a = a + "<= 1"
print a
print "end"
