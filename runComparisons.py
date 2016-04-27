from lib import snap
import sys
import os
import subprocess
import cplex

# This script runs several tests with randomly created small graphs to compare
# the solutions given by LP, greedy and brute force.

def main(argv):
  global datafile
  datafile = open('run.dat', 'w')
  numNodes = 20
  numRepetitions = 5

  for numGraphs in [1, 2, 4, 8]:
    for numRandomEdges in [0, 10, 20, 40, 80]:
      for cliqueSize in [0, 3, 6, 9, 12]:
        for i in range(0, numRepetitions):
          doTest(numGraphs, numNodes, numRandomEdges, cliqueSize)
  datafile.write('\n')
  datafile.close()

def doTest(numGraphs, numNodes, numRandomEdges, cliqueSize):
  global datafile
  graphDir = generateGraphs(numGraphs, numNodes, numRandomEdges, cliqueSize)
  graphFiles = getFiles(graphDir)
  densityLP = float(testLP(graphFiles))
  densityGreedy = float(testGreedy(graphFiles))
  densityBrute = float(testBrute(graphFiles))
  # Write the results to a data file. Just write columns of data, to make it
  # easier to read the data later into some program.
  datafile.write(graphDir + '\t')
  datafile.write(str(numGraphs) + '\t' + str(numNodes) + '\t')
  datafile.write(str(numRandomEdges) + '\t' + str(cliqueSize) + '\t')
  datafile.write(str(densityLP) + '\t')
  datafile.write(str(densityGreedy) + '\t')
  datafile.write(str(densityBrute) + '\n')
  # Do some printing as well, to give an update to the user.
  summary = "Graphs: " + str(numGraphs) + ", Nodes: " + str(numNodes) + \
      ", RandomEdges: " + str(numRandomEdges) + ", CliqueSize: " + \
      str(cliqueSize) + "\nLP density:          " + str(densityLP) + "\n" + \
      "Greedy density:      " + str(densityGreedy) + "\n" + \
      "Brute force density: " + str(densityBrute) + "\n"
  print summary
  # And remember the interesting lines?
  #if(max(abs(densityLP-densityBrute),abs(densityGreedy-densityBrute)) > 0.01


# Generate graphs and search the output for the directory where the graphs are
# placed. Return that directory.
def generateGraphs(numGraphs, numNodes, numRandomEdges, cliqueSize):
  output = subprocess.check_output(["python", "generateRandom.py", "-g",
    str(numGraphs), "-n", str(numNodes), "-r", str(numRandomEdges), "-c",
    str(cliqueSize)])
  return findStringBetween(output, "Using output directory ", "\n")


# Run the LP program on the graph directory. Return the density.
def testLP(files):
  output = subprocess.check_output(["python", "lp.py"] + files)
  return findStringBetween(output, "Density: ", "\n")


# Run the greedy program and return the density.
def testGreedy(files):
  output = subprocess.check_output(["python", "greedy.py"] + files)
  return findStringBetween(output, "Highest density found: ", "\n")


# Run the brute force program and return the density.
def testBrute(files):
  output = subprocess.check_output(["brute_force/brute"] + files)
  return findStringBetween(output, "Largest density found was ", " for solution")


# Search the string called haystack for substrings before and after. Return
# what's between them.
# Note, the first occurrence of before is used, and the next match of after from
# that position.
def findStringBetween(haystack, before, after):
  stringStartIndex = haystack.find(before)
  if stringStartIndex == -1:
    return ""
  stringEndIndex = haystack.find(after, stringStartIndex)
  if stringEndIndex == -1:
    return ""
  return haystack[stringStartIndex + len(before) : stringEndIndex]


# Return a list of all files (not subdirectories) in the directory.
def getFiles(directory):
  result = []
  contents = os.listdir(directory)
  for content in contents:
    filepath = os.path.join(directory, content)
    if os.path.isfile(filepath):
      result.append(filepath)
  return result




if __name__ == "__main__":
    main(sys.argv)

# vim: set expandtab tabstop=2 shiftwidth=2:
