

from __future__ import division
from __future__ import print_function
from lib import snap
import sys
import os

if(len(sys.argv) != 3):
  sys.exit("usage: python cplexToSnap <cplex.log> <resultGraph.txt>")


filename, file_extension = os.path.splitext(sys.argv[1])
supported_exentions = [".txt",".sol",".log"]
if file_extension not in supported_exentions:
  sys.exit("file extension: "+file_extension+" not supported")

if file_extension != ".log":
  sys.exit("Current version only support .log files")


output = open(sys.argv[2],"w+")
output.write("# Undirected Dense Subgraph: ")
output.write(sys.argv[2]+"  \n")
output.write("# Nodes: TODO")
output.write("Edges: TODO\n")
output.write("# FromNodeId    ToNodeId\n")


output.close()


#Graph = snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1)
#snap.MakeUnDir(Graph)
#



  
#Graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)
#nodes = 0
#edges = 0
#for n in Graph.Nodes():
#  nodes = nodes +1 
#for e in Graph.Edges():
#  edges = edges +1



# Computes the diameter, or longest shortest path, 
# of a Graph by performing a breadth first search over the Graph. 
# This diameter is approximate, as it is calculated with an NTestNodes
# number of random starting nodes.
#isDir = False
#diam = snap.GetBfsFullDiam(Graph,100,isDir)

# closed triads: number of pairs of 
# nodes neighbors that are connected between themselves).
# https://en.wikipedia.org/wiki/Triadic_closure
# triads = snap.GetTriads(Graph)

# Get Clustering coefficient
# https://en.wikipedia.org/wiki/Clustering_coefficient
# print "triadVlen: "+str(triads)



    
#print "######################"
#print "-- Getting Results --"
#print "input: "+sys.argv[1]
#print "nodes: "+str(nodes)
#print "edges: "+str(edges)
#print "----"
#print "approx. diameter: "+str(diam)
#print "Clustering Coefficient: "+str(snap.GetClustCf(Graph))
#print "Avg. Density: "+str(edges/nodes)
#print "######################"
