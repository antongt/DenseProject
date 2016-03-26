import sys
import os
from lib import snap;
# Converts a logfile of the form
# 
# y123 \n
# y124 \n
# x*_123#456 \n
# x*_1#23456 \n
# EOF
#
# to a snapgraph with snap.saveEdgeList()
# where x*_from#to are edges and yNodeId are nodes

def usage(): 
  sys.exit("usage: python logToSnap.py <file.log> <resultGraph.txt>")
if(len(sys.argv) != 3):
  usage()
cName,cExt  = os.path.splitext(sys.argv[1])
sName,sExt  = os.path.splitext(sys.argv[2])
if cExt != ".log":
  usage()
if sExt != ".txt":
  usage()
input = open(sys.argv[1])
line = ""
g = snap.TUNGraph.New()
for line in input:
  # Add Nodes
  if line[0] == 'y':
    if not g.IsNode( int(line.split( )[0][1:]) ) :
      g.AddNode(int(line.split( )[0][1:]))
  # Add Edges
  if line[0] == 'x':
    fr_to = line.split('_',1)[1].split('#',1)
    fr_to[1] = fr_to[1].split(' ',1)[0]
    if not g.IsEdge( int(fr_to[0]),int(fr_to[1]) ) :
      g.AddEdge(int(fr_to[0]),int(fr_to[1]))
snap.SaveEdgeList(g, sys.argv[2], "SnapGraph from logfile"+cName+"\n")
input.close()
print("cplexToSnap Completed.")
