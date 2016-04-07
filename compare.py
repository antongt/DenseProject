from __future__ import division
from lib import snap;
import sys;
import os
import cplex;


def usage():
	sys.exit("usage: python compare.py <GraphNameminLP.txt> <GraphNameminGREEDY.txt>")
# returns the list of nodes in graph
def getNodes(graph):
	a = []
	for n in graph.Nodes():
		a.append(n.GetId())
	return a

# returns the induced subgraph of the nodes from graph over the graph target_graph
def getSubgraph(target_graph,graph):
	
	a = snap.TIntV()
	for i in graph.Nodes():
		a.Add(i.GetId())
	return snap.GetSubGraph(target_graph,a)

# Start of main program
if(len(sys.argv) < 3):
	usage()
lpName,lpExt  = os.path.splitext(sys.argv[1])
gName,gExt  = os.path.splitext(sys.argv[2])
if lpExt != ".txt":
	usage()
if gExt != ".txt":
	usage()
# Load graphs
lpG = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
gG = snap.LoadEdgeList(snap.PUNGraph, sys.argv[2], 0, 1)
if "minLP" not in sys.argv[1]:
	usage()
if "minGREEDY" not in sys.argv[2]:
	usage()
print "What would you like to do?"
print "1) print common nodes"
print "2) print structural properties"
i =""
while i not in ["1","2"]:
	i = raw_input(">")
if i == "1":
	# calc similarities between node sets...
	
	lpN = getNodes(lpG)
	gN = getNodes(gG)
	# Take union of node sets to get number of unique nodes
	print "Number of nodes in LP:"+str(len(lpN))
	print "Number of nodes in GREEDY:"+str(len(gN))
	print "Number of unique nodes: LP_S 'union' GREEDY_S  : " + str(len(set(lpN) | set(gN)))
	print "Number of common nodes: LP_S 'intersection' GREEDY_S: " + str(len(set(lpN) & set(gN)))
	print "number of unique nodes in LP LP_S \ GREEDY_S : "+str(len(set(lpN) - set(gN)))
	print "number of unique nodes in GREEDY, GREEDY_S \ LP_S : "+str(len(set(gN) - set(lpN)))
	sys.exit("End of program...")
if i =="2":	
	g0LP = getSubgraph(snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1), lpG)
	g0G = getSubgraph(snap.LoadEdgeList(snap.PNGraph, sys.argv[2], 0, 1), gG)

	densityLP = float(g0LP.GetEdges()) / float(g0LP.GetNodes())
	densityG = float(g0G.GetEdges()) / float(g0G.GetNodes())

	print "Approximate Diameter,		 DCS_LP: %d, DCS_GREEDY: %d" % (snap.GetBfsFullDiam(g0LP, 10),snap.GetBfsFullDiam(g0G,10))
	print "Clustering Coefficient,		 DCS_LP: %.5f, DCS_GREEDY: %.5f" %(snap.GetClustCf(g0LP), snap.GetClustCf(g0G))
	print "Density,			 DCS_LP: %.5f, DCS_GREEDY: %.5f" % (densityLP,densityG)
	sys.exit("End of program...")
