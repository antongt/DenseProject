#
# This script generates a number of random graphs over
# the same set of nodes.
#
# Each graph is first generated as a connected graph with as few edges as
# possible (N-1 edges for N nodes).
# Then a number of random edges are added.
# Finally a clique is added. This clique is the same in all the graphs
# generated.

import os
import sys
import math
import random
from lib import snap
from optparse import OptionParser


def main():
  printUsageSummary()
  (options, args) = parseArguments()
  if not cleanUpArguments(options):
    sys.exit(2) # 2 is usually command line error?

  print("graphs: " + str(options.numGraphs))
  print("nodes: " + str(options.numNodes))
  print("random edges: " + str(options.numRandomEdges))
  for cs in options.cliqueSize:
    print("clique size: " + str(cs))

  # Create the cliques. They will make sure the graphs have something
  # in common and that the optimal solution is not the entire graph.
  nodesInClique = []
  blacklist = [] # This list is to make sure the cliques don't overlap.
  for i in range(0, len(options.cliqueSize)):
    if options.cliqueSize[i] > 0:
      nodesInClique.append(sorted(createCliqueNodes(options.numNodes,
          options.cliqueSize[i],
          blacklist)))
      print 'Clique: ', nodesInClique[-1]
      blacklist += nodesInClique[-1]

  # The files will be called 01.txt, 02.txt and so on. How many zeroes
  # we need to pad with depends on the number of files to have room for
  # the largest number.
  fieldWidth = int(1 + math.floor(math.log10(options.numGraphs)))

  # For as many graphs as we need, create a minimal randomized connected
  # graph, then add the edges from the clique previously created to it,
  # and save to a file.
  directory = createNewDir()
  for g in range(0, options.numGraphs):
    graph = snap.TUNGraph.New(options.numNodes, options.numNodes)
    createConnectedGraph(graph, options.numNodes)
    addRandomEdges(graph, options.numRandomEdges)
    for c in nodesInClique:
      addCliqueToGraph(graph, c)
    fileName = os.path.join(directory, str(1+g).zfill(fieldWidth) + ".txt")
    snap.SaveEdgeList(graph, fileName)


# Make sure the options are somewhat sensible.
# Returns True if everything checks out, False if there were errors.
def cleanUpArguments(options):
  options.numGraphs = max(0, options.numGraphs)
  if options.numGraphs < 1:
    print >> sys.stderr, "Error: number of graphs must be at least 1."
    return False
  options.numNodes = max(0, options.numNodes)
  if options.numNodes < 1:
    print >> sys.stderr, "Error: number of nodes must be at least 1 (but ideally more)."
    return False
  options.numRandomEdges = max(0, options.numRandomEdges)
  # Make sure the clique size list exists, to avoid errors later.
  if not options.cliqueSize:
    options.cliqueSize = [0]
  for i in range(0, len(options.cliqueSize)):
    options.cliqueSize[i] = max(0, options.cliqueSize[i])
  if sum(options.cliqueSize) > options.numNodes:
    print >> sys.stderr, "Error: cliques contain more nodes than the graph."
    return False
  return True


# Defines a clique by randomly picking a number of nodes equal to size, from
# the range [1, numNodes]. This function does not add any edges or manipulates
# any graph, it simply selects the nodes and returns them as a list.
# Note that regardless of size, the function will not return more nodes than
# there are in the graf.
def createCliqueNodes(numNodes, size, blacklist):
  nodes = []
  while len(nodes) < min(numNodes, size):
    r = random.randrange(1, numNodes+1)
    if not r in nodes and not r in blacklist:
      nodes.append(r)
  return nodes


# Create a clique from the nodes in nodesInClique, in the given graph.
def addCliqueToGraph(graph, nodesInClique):
  for a in range(0, len(nodesInClique)-1):
    for b in range(a+1, len(nodesInClique)):
      if not graph.IsEdge(nodesInClique[a], nodesInClique[b]):
        graph.AddEdge(nodesInClique[a], nodesInClique[b])


# Add a number of completely random edges to the graph. The number of edges
# added might be smaller if some of the edges already exists.
def addRandomEdges(graph, numRandomEdges):
  for i in range(0, numRandomEdges):
    fromId = graph.GetRndNId()
    toId = graph.GetRndNId()
    if fromId != toId and not graph.IsEdge(fromId, toId):
      graph.AddEdge(fromId, toId)


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
      action="append",
      type="int",
      dest="cliqueSize",
      help="specify clique size (default 0). This option can be used multiple times to create non-overlapping cliques.")
  parser.add_option("-r",
      "--random",
      type="int",
      dest="numRandomEdges",
      default=0,
      help="specify number of random edges to add (default 0)")
  return parser.parse_args()


# Run main function.
if __name__ == "__main__":
  main()

# vim: set expandtab tabstop=2 shiftwidth=2:
