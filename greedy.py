from lib import snap
import sys
import time
from greedy import DCSGreedy, utils, preprocessGreedy

if(len(sys.argv) < 2):
  sys.exit("Usage: python " + sys.argv[0] + " <file1> <file2> ...")
  
utils.timer() # Start the timer.
if(sys.argv[1] == "-d"):
    graphs = preprocessGreedy.loadDirGraphs()
else:
    graphs = preprocessGreedy.loadGraphs()

print("Imported " + str(len(graphs)) + " graphs in " + utils.timer())
# Don't remove, this isn't the deep preprocessing that takes time.
numberOfNodes = preprocessGreedy.simplePreprocessing(graphs)

# If multiple graphs, do some preprocessing to make sure they are over the same
# set of nodes.
# Make sure all graphs have the same amount of nodes.
# There could be a deeper check here.

print("Preprocessing took " + utils.timer())
startTime = time.clock()
(nodes,density) = DCSGreedy.getDCS_Greedy(graphs,numberOfNodes)
runTime = time.clock()-startTime

utils.saveResults(nodes,str(runTime) + " seconds",density)

# printQuickStats(g2)
print("The greedy algorithm completed in " + str(runTime) + " seconds")
#saveResults(g2, runTime, density)
