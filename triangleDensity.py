from lib import snap
import sys
import numpy
import gmpy2


def loadGraph():
    print("using graph " + sys.argv[1])
    graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
    print(str(graph.GetNodes()) + " nodes and " + str(graph.GetEdges()) + " edges.")
    triangles = numpy.zeros(graph.GetMxNId())

    #adjMatrix = numpy.zeros((65536,65536))
    #for e in graph.Edges():
    #    nodes = e.GetId()
    #    adjMatrix[nodes[0], nodes[1]] += 1
    #    adjMatrix[nodes[1], nodes[0]] += 1

    i = 0
    print("nodes completed:")
    for currentNode in graph.Nodes():
        i = i+1
        if i% 100 == 0:
            print(i)
        for neighbourIndex in range(0, currentNode.GetOutDeg()):
            neighbourId = currentNode.GetOutNId(neighbourIndex)
            neighbourNode = graph.GetNI(neighbourId)
            for NNI in range(0, neighbourNode.GetOutDeg()):
                NNID = neighbourNode.GetOutNId(NNI)
                for realNeighbourIndex in range(0, currentNode.GetOutDeg()):
                    realNeighbour = currentNode.GetOutNId(realNeighbourIndex)
                    if NNID == realNeighbour:
                        triangles[currentNode.GetId()] += 1
    ntriangles = numpy.sum(triangles)/6
    print "number of triangles:  {}".format(ntriangles)
    print "triangle density : {}".format(ntriangles/gmpy2.comb(graph.GetNodes(),3))
loadGraph()
