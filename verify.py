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
# /home/kognitiva/Dokument/3NUVARANDE/3KAND/verify.py
def usage():
  sys.exit("usage: python verify.py <graphDCS_LP|DCS_GREEDY.txt> <original1.txt> <original2.txt> ...")
# Returns smallest subgraph induced by nodeset
# from sys.argv[1] over graphs from sys.argv[2:]
# and saves it to users choice of name
def findSmallestGraph():
	g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)
	Graphs = []
	names = []
	for file in sys.argv[2:]:
		Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
		lpName,lpExt  = os.path.splitext(file)
		names.append(lpName)
	a = snap.TIntV()
	for i in g.Nodes() : 
	  a.Add(i.GetId())
	density = 500
	
	for i in range(0,len(Graphs)):
		Graphs[i] = snap.GetSubGraph(Graphs[i],a)
		newD = Graphs[i].GetEdges() / float(Graphs[i].GetNodes())
		if newD < density :
			density = newD
			g = i
	

	print "Smallest graph was: "+ str(names[i])
	print "Density: "+str(density)
	return (names[i],Graphs[g])

def saveGraphs():
	g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)
	Graphs = []
	a = snap.TIntV()
	for file in sys.argv[2:]:
		Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
		folder = str(file).split("/")[0]
		if folder != "data":
			sys.exit("comparison should be made with file in 'data' folder")
	    
	data = sys.argv[2].split("/")[1]
	path = "/"
	if "DCS_LP" in sys.argv[1]:
		path = "results/snap/"+data+"DCS_LP/"
	else :# DCS_GREEDY
		path = "results/snap/"+data+"DCS_GREEDY/"
	
	if not os.path.exists(path) :
		os.makedirs(path)


	for i in g.Nodes() : 
	  a.Add(i.GetId())
	for i in range(0,len(Graphs)):
		Graphs[i] = snap.GetSubGraph(Graphs[i],a)

	filename = raw_input('Enter a snapgraph name: ')
	print "saving graphs in: " + path +" under names "+filename+"i.txt"
	for i in range(0,len(Graphs)):
		snap.SaveEdgeList(Graphs[i],path+filename+str(i+1)+".txt","Minimal graph from" + sys.argv[1])		

	
# Prints stats on the induced Graphs <data.txt> from <resultGraph.txt>
def printStats():
	g = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1],0,1)
	
	for i in range(2,len(sys.argv)):
		cName,cExt = os.path.splitext(sys.argv[i])
		
		a = snap.TIntV()

		gi = snap.LoadEdgeList(snap.PUNGraph, sys.argv[i], 0, 1)
		print "Printing stats..."
		for n in g.Nodes():
			a.Add(n.GetId())
		g0 = snap.GetSubGraph(gi,a)
		n = g0.GetNodes()
		e = g0.GetEdges()
		print "---"
		print "Stats from : " + str(cName)
		print "Nodes : "+str(n)
		print "Edges : "+str(e)
		print "Density : "+ str( e / float(n))

# Main
if len(sys.argv) < 3 :
  usage()

if not ("DCS_LP" in sys.argv[1] or "DCS_GREEDY"in sys.argv[1]):
	usage()


for i in range(1, len(sys.argv)):
	name,ext = os.path.splitext(sys.argv[i])
	if ext != ".txt":
  		usage()
usr_in = ""
print "Program: Verify..."
print "1) print graph stats"
print "2) Save graphs"
print "3) find smallest graph"
while  usr_in not in ["1","2","3"]:
	usr_in = raw_input(">") 
print "You have Choosen " + usr_in +"!"
if usr_in == "1":
	printStats()
if usr_in == "2":
	saveGraphs()
if usr_in =="3":
	name,g = findSmallestGraph()
	print "Would you like to save this graph?"
	print "y/n"
	a = ""
	while a not in ["y","n"]:
		a = raw_input(">")
	if a == "y":
		smallest = raw_input("input name: ")
		snap.SaveEdgeList(g,smallest+".txt","Smallest graph from" + sys.argv[1])
		print "saving..."
	sys.exit("exiting...")





