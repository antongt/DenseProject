from lib import snap
from lib import printResults
from greedy import DCSGreedy
from greedy import preprocessGreedy
import sys
import os
import cplex

global nIter
nIter = 5

if(len(sys.argv) < 2):
  sys.exit("usage: python lag.py <file1> ... <fileN>")

def printGraphs(Graphs):
  nodes = []
  global allEdges
  allEdges = []
  allEdgeCons = []

  for g in range(0,len(Graphs)):
    edges    = []
    edgeCons = []
    for e in Graphs[g].Edges():
      src = e.GetSrcNId()
      dst = e.GetDstNId()
      xij = "x"+str(g)+"_"+str(src)+"#"+str(dst)
      yi  = "y"+str(src)
      yj  = "y"+str(dst)
      edges.append(xij)
      edgeCons.append(xij+" - "+yi+" <= 0")
      edgeCons.append(xij+" - "+yj+" <= 0")
    for n in Graphs[g].Nodes():
      id = n.GetId()
      yi = "y"+str(id)
      nodes.append(yi)
    allEdges.append(edges)
    allEdgeCons.append(edgeCons)

  # remove duplicates
  nodes = list(set(nodes))
  
  tcof = 1-(1*len(Graphs))
  tobj = str(tcof)+"t"

  global xijm 
  xijm = [e for es in allEdges for e in es]

  with open("dense.lp", "w") as f:
    print >> f, "maximize "+tobj+" +"
    print >> f, " +\n".join(xijm)
    print >> f, "\nsubject to"
    print >> f, (" +\n".join(nodes))+" <= 1" # sum yi <= 1
    for c in allEdgeCons:
      print >> f, " \n".join(c) # xij <= yi and xij <= yj
    print >> f, "\nend"


Graphs = []

for file in sys.argv[1:]:
  Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))
printGraphs(Graphs)

# index for all x's are 1-len(xijm), in cplex.
print "Warning: This file assumes already preprocessed files,"
print "         meaning the input should be undirected and"
print "         all node-sets should be equal, see preprocess.py.\n"
print "Warning: Only does " + str(nItr) + " iterations.\n"
print "Info: total number of edges:" + str(len(xijm))


dense0 = cplex.Cplex("dense.lp")
#dense0.set_results_stream(None)
alg = dense0.parameters.lpmethod.values
dense0.parameters.lpmethod.set(alg.barrier)
dense0.parameters.barrier.crossover.set(-1)
start_time0 = dense0.get_time()
dense0.solve()
end_time0 = dense0.get_time()

iter0_time = end_time0 - start_time0

prev_t    = dense0.solution.get_values(0)
prev_xijm = dense0.solution.get_values(range(1,len(xijm)+1))
prev_val  = dense0.solution.get_objective_value()
printResults.save(dense0)
print "time taken: " + str(iter0_time)
sys.exit()
print "Iteration 0 ("+str(iter0_time)+" sec.): " + str(prev_val)

# initial value of all lamdas are -1.
lamda = [-1]*len(Graphs)

times = []
times.append(iter0_time)
usedNodes = preprocessGreedy.simplePreprocessing(Graphs)
(nodes, LB) = DCSGreedy.getDCS_Greedy(Graphs,usedNodes)
scalar = 1.0
dense = cplex.Cplex("dense.lp")
j = 0
while(j<nIter):
    #remove all output from cplex:
    dense.set_results_stream(None)

    oldlamda = lamda[:]
    #calculate (sub)gradients:
    grads = []
    start = 1
    for i in range(0,len(lamda)):
      # split up prev_xijm
      end = start+len(allEdges[i])
      prev_xijm_sum = sum(prev_xijm[start:end])
      grad = prev_t - prev_xijm_sum
      grads.append(grad)
      start = end
    print scalar
    #calculate stepsize:
    UB = prev_val
    numer = scalar * (UB - LB)
    denom = sum([grad * grad for grad in grads])
    stepsize = numer / denom

    #update lamda:
    for i in range(0,len(lamda)):
      lamda[i] = lamda[i] - stepsize * grads[i]

    #modify LP with new lamdas:
    new_obj = []
    start = 1
    for i in range(0,len(lamda)):
      end = start+len(allEdges[i])
      indexs = range(start, end)
      coef = lamda[i] * (-1)
      new_obj += [ (ind, coef) for ind in indexs ]
      start = end

    dense.objective.set_linear(0, 1+sum(lamda))
    dense.objective.set_linear(new_obj)

    alg = dense.parameters.lpmethod.values
    dense.parameters.lpmethod.set(alg.barrier)
    dense.parameters.barrier.crossover.set(-1)
    start_time = dense.get_time()
    dense.solve()
    end_time = dense.get_time()

    iter_time = end_time - start_time
    times.append(iter_time)

    #TODO: check if feasible, if not divide the scalar by 2.

    if(dense.solution.get_status() == dense.solution.status.infeasible_or_unbounded):
      print "infeasible solution."
      scalar = scalar * 0.5
      lamda = oldlamda[:]
    else:
      j += 1
      if scalar < 0.01:
          break
      prev_t    = dense.solution.get_values(0)
      prev_xijm = dense.solution.get_values(range(1,len(xijm)))
      prev_val  = dense.solution.get_objective_value()
    
      print "Iteration "+str(j)+" ("+str(iter_time)+" sec.): "+str(prev_val)

total_time = sum(times)
print "Total time: " + str(total_time) + " sec."
printResults.save(dense)
cplex.terminate()
os.remove("dense.lp")
