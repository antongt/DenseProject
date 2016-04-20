import time
import sys


# A function to measure how long something takes to run.
# Returns a string holding the time since last time the function was called.
# Uses a global variable to hold the time of previous call.
def timer():
    global lastTimeStamp
    try:
        elapsedTime = time.clock() - lastTimeStamp
    except NameError:
        # First time the function is called there is no startTime declared.
        elapsedTime = 0
    lastTimeStamp = time.clock()
    return '%.1f seconds' % elapsedTime

# Print progress bar based on size of the graph (it is reduced to zero nodes).
def printProgress(message, originalSize, currentSize):
    global lastUpdateTimeStamp
    updateFrequency = 10 # Update progress every X seconds.
    try:
        if time.clock() - lastUpdateTimeStamp < updateFrequency:
            return
    except NameError:
        lastUpdateTimeStamp = time.clock()
    lastUpdateTimeStamp = time.clock()
    percentage = '%.0f' % (100*(originalSize-currentSize)/(1.0*originalSize))
    print(message + percentage + "% done")

# For debugging. Use with tiny graphs only.
def printLookupTable():
    global lookupTable
    deg = 0
    for degreeList in lookupTable:
        sys.stdout.write(str(deg) + ": ")
        for node in degreeList:
            sys.stdout.write(str(node) + " ")
        print("")
        deg += 1

# Save the results to a snap graph file.
# TODO: why does snap.SaveEdgeList not save the file?
# TODO: what are we actually saving? Nodes, edges, density?
def saveResults(nodeList, runTime, density):
    fileName = "greedy-out.tmp"
    print("Saving as " + fileName)
    description = "Densest subgraph by greedy algorithm, completed in " + runTime
    #snap.SaveEdgeList(graph, fileName, description)

    f = open(fileName, 'w')
    f.write('# Node list of the densest common subgraph of the following graphs:\n')
    for arg in sys.argv[1:]:
        f.write('#   ' + arg + '\n')
    f.write('# Number of nodes: ' + str(len(nodeList)) + '\n')
    f.write('# Density: ' + str(density) + '\n')
    f.write('# Completed in ' + runTime + '\n')
    for n in nodeList:
        f.write(str(n) + '\n')