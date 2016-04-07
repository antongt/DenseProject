#
# This script generates a number of random graphs over
# the same set of nodes.

import os
import math
import random
from lib import snap
from optparse import OptionParser
from lib import snapGraphCopy


def main():
  printUsageSummary()
  (options, args) = parseArguments()
  print("graphs: " + str(options.numGraphs))
  print("nodes: " + str(options.numNodes))

  directory = createNewDir()

  # Create a base graph. This will make sure the graphs have something
  # in common.
  baseGraph = snap.GenRndGnm(snap.PUNGraph, options.numNodes, 3*options.numNodes)
  # The files will be called 01.txt, 02.txt and so on. How many zeroes
  # we need to pad with depends on the number of files to have room for
  # the largest number.
  fieldWidth = int(1 + math.floor(math.log10(options.numGraphs)))
  for g in range(0, options.numGraphs):
    #graph = snap.TUNGraph.New(options.numNodes, options.numNodes)
    graph = snapGraphCopy.copyGraph(baseGraph)
    createHotSpot(graph, graph.GetRndNId(), 3, 10)
    fileName = os.path.join(directory, str(1+g).zfill(fieldWidth) + ".txt")
    snap.SaveEdgeList(graph, fileName)

# In graph, create a hotspot of edges near node, within a distance of
# diameter. Add a total of specified number of edges.
def createHotSpot(graph, node, diameter, edges):
  for i in range(0, edges):
    # Pick random number of jumps, but stay within diameter.
    # TODO: Is it supposed to be half diameter? Do we need to subtract 1
    # to account for the edge as well?
    numHops = random.randrange(diameter)
    for j in range(0, numHops):
      node = hop(graph, node)
    addRandomEdge(graph, node)


# Jump from one node to a random neighbor. Returns the new node.
def hop(graph, nodeId):
  node = graph.GetNI(nodeId)
  neighborId = node.GetOutNId(random.randrange(node.GetDeg()))
  return neighborId


# Adds an edge to the graph, with one end on node and the other on
# a random neighbor. Will make a few attempts, trying again if the
# edge already exists.
def addRandomEdge(graph, fromNode):
  toNode = graph.GetRndNId()
  attempts = 10
  while attempts > 0 and graph.IsEdge(fromNode, toNode):
    toNode = graph.GetRndNId()
    attempts -= 1
  graph.AddEdge(fromNode, toNode)


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
      help="specify number of graphs")
  parser.add_option("-n",
      "--nodes",
      type="int",
      dest="numNodes",
      default=100,
      help="specify number of nodes")
  return parser.parse_args()


# Run main function.
if __name__ == "__main__":
  main()

# vim: set expandtab tabstop=2 shiftwidth=2:
