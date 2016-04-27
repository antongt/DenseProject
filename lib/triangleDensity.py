from lib import snap
import sys
import numpy
import gmpy2

def triangleDensity(graph):
    outV = snap.TIntPrV()
    snap.GetTriadParticip(graph,outV)
    triangles = 0.0
    for pair in outV:
        triangles += (pair.GetVal1()*pair.GetVal2())

    triangles=triangles / 3.0 #three triangles per node is added
    print ("number of triangles: "+str(triangles))
    return (triangles/gmpy2.comb(graph.GetNodes(),3))

def badTriangleDensity(graph):
    triangles = numpy.zeros(graph.GetMxNId())
    i = 0
    print("starting triangle density, printing every 100 nodes competed")
    for currentNode in graph.Nodes():
        i = i+1
        if i % 100 == 0:
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
    print "done with triangle density"
    print "number of triangles:  {}".format(ntriangles)
    return ntriangles/gmpy2.comb(graph.GetNodes(), 3)

def loadGraph():
    print("using graph " + sys.argv[1])
    graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
    print(str(graph.GetNodes()) + " nodes and " + str(graph.GetEdges()) + " edges.")
    return graph
