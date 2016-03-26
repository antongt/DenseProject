from __future__ import division
from lib import snap;
import sys;
import os
import cplex;

model = cplex.Cplex()

def usage():
	sys.exit("usage: python compare.py <SnapGraph1DCS_LP.txt> <SnapGraph1DCS_GREEDY.txt>")
if(len(sys.argv) != 3):

	usage()

lpName,lpExt  = os.path.splitext(sys.argv[1])
gName,gExt  = os.path.splitext(sys.argv[2])


if lpExt != ".txt" or "DCS_LP" not in sys.argv[1]:
	usage()
if gExt != ".txt" or "DCS_GREEDY" not in sys.argv[2]:
	usage()
# Load graphs
lpG = snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1)
gG = snap.LoadEdgeList(snap.PNGraph, sys.argv[2], 0, 1)

nLP=0.0
eLP=0.0
nG=0.0
eG=0.0

# calc density for DCS_LP
for n in lpG.Nodes():
	nLP= nLP+1
print("nodes: " +str(nLP))
for e in lpG.Edges():
	eLP = eLP+1
print("edges: "+str(eLP))
densityLP = eLP /  float(nLP)



# calc density for DCS_GREEDY
for n in gG.Nodes():
	nG = nG+1
for e in gG.Edges():
	eG = eG+1
densityG = eG / float(nG)
#print " lp: n:%d e:%d, greedy:  n:%d e:%d" %(nLP,eLP,nG,eG)


#sys.exit()
print "Approximate Diameter,		 DCS_LP: %d, DCS_GREEDY: %d" % (snap.GetBfsFullDiam(lpG, 10),snap.GetBfsFullDiam(gG,10))
print "Clustering Coefficient,		 DCS_LP: %.3f, DCS_GREEDY: %.3f" %(snap.GetClustCf(lpG), snap.GetClustCf(gG))
print "Density,			 DCS_LP: %.3f, DCS_GREEDY: %.3f" % (densityLP,densityG)
sys.exit("End of program...")
