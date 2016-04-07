from lib import snap
import os
import sys

def usage():
	sys.exit("usage: python pic.py <inputGraph.txt>")
if len(sys.argv) < 2:
	usage()
g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)
labels = snap.TIntStrH()
for NI in g.Nodes():
	labels[NI.GetId()] = str(NI.GetId())
name = ""
while name == "":
	name = raw_input("save file as: ")
	print ">"
snap.DrawGViz(g, snap.gvlDot, name+".png", " ", labels)