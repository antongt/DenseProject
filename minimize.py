
from lib import snap

import os
import sys
import cplex
import lp


# Finds a local minimum(ddmin) of a fault inducing graph set, e.g a set of graphs
# for which DCS_LP finds  a suboptimal solution

# The code uses the following modules
# - lp.py
# where it uses printMoreGraphs() function call.
def usage():
	print "python minimize.py <graph1.txt> <graph2.txt> <graph3.txt> ... graphn.txt"

# takes sys.argv[1:] as input and outputs the smallest graph w.r.t the parameter nodes
# which is a set of common nodes over the graphs in argv[1:]

# "Smallest graph" is the graph with smallest density w.r.t the parameter nodes
def fsg(nodes):
	g = -1
	Graphs = []
	names = []
	for file in sys.argv[1:]:
		Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
		lpName,lpExt  = os.path.splitext(file)
		names.append(lpName)
	a = snap.TIntV()
	for i in nodes : 
	  a.Add(i)
	density = 500
	
	for i in range(0,len(Graphs)):
		Graphs[i] = snap.GetSubGraph(Graphs[i],a)
		newD = Graphs[i].GetEdges() / float(Graphs[i].GetNodes())
		if newD < density :
			density = newD
			g = i
	

	print "Smallest graph was: "+ str(names[g])
	print "Density: "+str(density)
	return (names[g],Graphs[g],density)

# is a function which parametrizes graphs. This does not return the file name but is otherwise the same as fsg.
def findSmallestGraph(nodes,Graphs):

	a = snap.TIntV()
	for i in nodes : 
	  a.Add(i)
	density = 500
	g = -1

	for i in range(0,len(Graphs)):
		Graphs[i] = snap.GetSubGraph(Graphs[i],a)
		newD = Graphs[i].GetEdges() / float(Graphs[i].GetNodes())
		if newD < density :
			density = newD
			g = i
	#print "Smallest graph was: "+ str(g)
	#print "Density: "+str(density)
	return ("find smallest",Graphs[g],density)

def printStats(graphs):
	
	for g in graphs:
		n = g.GetNodes()
		e = g.GetEdges()
		print "---"
		print "Stats from : " + str(g)
		print "Nodes : "+str(n)
		print "Edges : "+str(e)
		print "Density : "+ str( e / float(n))
	

# Returns a list of tuples containing variable (name,value)
# from the cplex object c which is a solved problem.
def getNonZero(c):
	res = []
	for i,x in enumerate(c.solution.get_values()):
		if x != 0:
			res.append((c.variables.get_names(i),x))
	return res
# returns the list of node ID as integers
def getNodes(list):
	res = []
	for  var in list:
		if var[0][0] == 'y':
			res.append(int(var[0][1:]))
	return res
# returns the subgraph of target from nodes
def getSubgraph(target_graph,nodes):
	
	a = snap.TIntV()
	for i in nodes:
		a.Add(i)
	return snap.GetSubGraph(target_graph,a)

# returns the list of Edges
# TODO not sure how to represent edges yet
def getEdges(list):
	res = []
	for var in list:
		if var[0][0] == 'x':
			res.append(var)
	return res
# returns the optimum value of the LP.
def getSolution(list):
	for var in list:
		if var[0] == 't':
			return var[1] 
	return -1

# Returns true if DCS_LP is optimal
# over the graphs gs
def testGraphs(gs,output):
	lp.printMoreGraphs(gs)
	dense = cplex.Cplex("dense.lp")
	
	# Turn off cplex output
	if not output : 
		dense.set_log_stream(None)
		dense.set_error_stream(None)
		dense.set_warning_stream(None)
		dense.set_results_stream(None)

	os.remove("dense.lp")
	alg = dense.parameters.lpmethod.values
	dense.parameters.lpmethod.set(alg.barrier)
	dense.solve()
	nodes = getNodes(getNonZero(dense))
	t = getSolution(getNonZero(dense))
	(name,graph,density) = findSmallestGraph(nodes,gs)
	if abs(t-density) < 0.000005:
		return True
	else:
		return False 
# Divides the list into n number of chunks
def split(list, n):
    k, m = len(list) / n, len(list) % n
    return (list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

# minimizes the fault inducing node set
# returns a local minimal fault inducing node set
# if it terminates that is...
def ddmin(chunk_size,nodes,graphs):
	
	while chunk_size != len(nodes):
		cdid_pass = True
		gs = []
		a = split(nodes,chunk_size)	
		for chunk in a:
			n = [x for x in nodes if x not in chunk]
			gs = []
			for g in graphs : 
				gs.append(getSubgraph(g,n))
			if not testGraphs(gs,True):
				print "nodes: "+str(nodes)
				print "caused fault. minimizing.."
				did_pass = False
				nodes = n
				graphs = gs
				chunk_size = max(chunk_size-1,2)
				break
				#break early since we need to look no further
		if did_pass:
			chunk_size = min(chunk_size*2,len(nodes))
	print "returning nodes: "+str(nodes)
	if testGraphs(graphs,False):
		sys.exit("ddmin bug.. exiting")
	return nodes,graphs

def main(argv):

	if len(argv) < 1:
		usage()
	gs = []		
	for file in argv[1:]: gs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
	# Load and solve LP
	usr_in = ""
	print "Program: minimize..."
	print "1) minimize nodes wrt sys.argv[1:]"
	print "2) Does this input fail (sys.argv[1:]) yes/no"

	while  usr_in not in ["1","2"]:
		usr_in = raw_input(">") 

	print "You have Choosen " + usr_in +"!"

	if usr_in == "1":
		lp.printMoreGraphs(gs)
		dense = cplex.Cplex("dense.lp")
		os.remove("dense.lp")
		alg = dense.parameters.lpmethod.values
		dense.parameters.lpmethod.set(alg.barrier)
		dense.solve()

		# get the nodes for the LP
		nodes = getNodes(getNonZero(dense))
		print "size nodes:"+str(nodes)
		# minimize the nodes and respective graphs
		n,gs = ddmin(2,nodes,gs)
		gs0 = []
		for g in gs:
			gs0.append(getSubgraph(g,n))

		lp.printMoreGraphs(gs)
		dense = cplex.Cplex("dense.lp")
		os.remove("dense.lp")
		alg = dense.parameters.lpmethod.values
		dense.parameters.lpmethod.set(alg.barrier)
		dense.solve()

		t = getSolution(getNonZero(dense))
		
		(name,graph,density) = fsg(nodes)
		
		print "t* = "+str(t)
		print "density = "+str(density)
		print "t* =? density : " +str(abs(t - density) < 0.000005)
	if usr_in == "2":
		if testGraphs(gs,True):
			print "No, input does not fail, e.g t* = density"
		else:
			print "Yes, input does fail, e.g t* != density"

if __name__ == "__main__":
	main(sys.argv)

