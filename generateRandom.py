#
# This script generates a number of random graphs over
# the same set of nodes.

import os
import sys
import math
import random
from lib import snap
from optparse import OptionParser
#from lib import snapGraphCopy


def main():
  printUsageSummary()
  (options, args) = parseArguments()
  if options.cliqueSize == -1:
    options.cliqueSize = options.numNodes/2
  print("graphs: " + str(options.numGraphs))
  print("nodes: " + str(options.numNodes))
  print("clique size: " + str(options.cliqueSize))

  directory = createNewDir()

  # Create a clique. This will make sure the graphs have something
  # in common and that the optimal solution is not the entire graph.
  nodesInClique = createCliqueNodes(options.numNodes, options.cliqueSize)
  print 'Clique: ', nodesInClique

  # The files will be called 01.txt, 02.txt and so on. How many zeroes
  # we need to pad with depends on the number of files to have room for
  # the largest number.
  fieldWidth = int(1 + math.floor(math.log10(options.numGraphs)))

  # For as many graphs as we need, create a minimal randomized connected
  # graph, then add the edges from the clique previously created to it,
  # and save to a file.
  for g in range(0, options.numGraphs):
    graph = snap.TUNGraph.New(options.numNodes, options.numNodes)
    createConnectedGraph(graph, options.numNodes)
    addCliqueToGraph(graph, nodesInClique)
    fileName = os.path.join(directory, str(1+g).zfill(fieldWidth) + ".txt")
    snap.SaveEdgeList(graph, fileName)


# Defines a clique by randomly picking a number of nodes equal to size, from
# the range [1, numNodes]. This function does not add any edges or manipulates
# any graph, it simply selects the nodes and returns them as a list.
def createCliqueNodes(numNodes, size):
  if size>numNodes:
    print >> sys.stderr, '\nError: Can\'t create clique larger than the number of nodes in the graph.'
    sys.exit(1)
  nodes = []
  while len(nodes) < size:
    r = random.randrange(1, numNodes+1)
    if nodes.count(r) == 0:
      nodes.append(r)
  return nodes


# Create a clique from the nodes in cliqueNodes, in the given graph.
def addCliqueToGraph(graph, cliqueNodes):
  for a in range(1, len(cliqueNodes)-1):
    for b in range(a+1, len(cliqueNodes)):
      if not graph.IsEdge(a, b):
        graph.AddEdge(a, b)


# Given an empty snap graph and a number of nodes N, modify the graph so that
# it is a randomized connected graph with the minimum (N-1) number of edges.
#
# The graph is created with the following algorithm:
# Initialize a list of all nodes except node 1.
# Add node 1 to the graph.
# While the list of nodes is not empty:
#   Randomly pick a node n1 from the graph.
#   Arbitrary pick a node n2 in the list of nodes. Remove it from the list.
#   Create an edge between n1 and n2.
def createConnectedGraph(graph, numNodes):
  unaddedNodes = range(2, numNodes+1)
  graph.AddNode(1)
  while len(unaddedNodes) > 0:
    fromId = graph.GetRndNId()
    toId = unaddedNodes.pop()
    graph.AddNode(toId)
    graph.AddEdge(fromId, toId)


def printUsageSummary():
  print("\nThis script generates random graphs over a set of nodes.")
  print("Run it with the argument --help to see usage help.\n")


# Create a new directory.
# The default name is followed by a number, starting with 1.
# If the default one exists, increment the number until
# a directory does not exist.
def createNewDir():
  defaultName = 'generated_'
  number = 1
  dirPath = ""
  while True:
    # Note: the function zfill pads with leading zeroes.
    dirPath = os.path.join("data", defaultName + str(number).zfill(2))
    number += 1
    if not os.path.exists(dirPath):
      break
  try:
    os.makedirs(dirPath)
    print("Using output directory " + dirPath)
  except:
    print >> sys.stderr, "Could not create a new directory"
  return dirPath


# Build a parser to handle command line arguments. This uses the old
# (deprecated) optparse library from python <2.7, since that's what we have.
def parseArguments():
  usage = "%prog [options]"
  parser = OptionParser(usage)
  parser.add_option("-g",
      "--graphs",
      type="int",
      dest="numGraphs",
      default=10,
      help="specify number of graphs (default 10)")
  parser.add_option("-n",
      "--nodes",
      type="int",
      dest="numNodes",
      default=100,
      help="specify number of nodes (default 100)")
  parser.add_option("-c",
      "--clique",
      type="int",
      dest="cliqueSize",
      default=-1,
      help="specify clique size (default 1/2 number of nodes)")
  return parser.parse_args()


# Run main function.
if __name__ == "__main__":
  main()

# vim: set expandtab tabstop=2 shiftwidth=2:
