import snap;
import sys;


if(len(sys.argv) != 3):
  sys.exit("usage: python snapToLp2.py <file1> <file2>")

Graph1 = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
Graph2 = snap.LoadEdgeList(snap.PUNGraph, sys.argv[2], 0, 1)

#remove unnecessary nodes and edges from the grahps
v = snap.TIntV()
for n in Graph1.Nodes():
  for m in Graph2.Nodes():
   if(n.GetId() == m.GetId()):
     v.Add(n.GetId())

Graph1 = snap.GetSubGraph(Graph1,v)
Graph2 = snap.GetSubGraph(Graph2,v)

# Objective function
print "Maximize t"


# constraints
print "Subject to"

# sum x1_ij >= t
b = " "
for e in Graph1.Edges():
  b = b + ("x1_"+''.join(map(str,e.GetId()))+" + ")

b = b[:-2]
print b+" - t >= 0"

# sum x2_ij >= t
b = " "
for e in Graph2.Edges():
  b = b + ("x2_"+''.join(map(str,e.GetId()))+" + ")

b = b[:-2]
print b+" - t >= 0"

# x1_ij <= min (y_i, y_j)
# x1_ij >= 0
for e in Graph1.Edges():
  nodesrc = e.GetSrcNId()
  nodedst = e.GetDstNId()
  edgeId  = ''.join(map(str,e.GetId()))
  print " x1_"+edgeId+" - y"+str(nodesrc) + " <= 0"
  print " x1_"+edgeId+" - y"+str(nodedst) + " <= 0"
  print " x1_"+edgeId+" >= 0"

# x2_ij <= min (y_i,y_j)
# x2_ij >= 0
for e in Graph2.Edges():
  nodesrc = e.GetSrcNId()
  nodedst = e.GetDstNId()
  edgeId  = ''.join(map(str,e.GetId()))
  print " x2_"+edgeId+" - y"+str(nodesrc) + " <= 0"
  print " x2_"+edgeId+" - y"+str(nodedst) + " <= 0"
  print " x2_"+edgeId+" >= 0"

# sum y_i <= 0
# y_i >= 0
a = " "
for n in Graph1.Nodes():
  print "y"+str(n.GetId())+" >= 0"
  a = a + ("y"+str(n.GetId())+" + ")

a = a[:-2]
a = a + "<= 1"
print a

# end
print "end"
