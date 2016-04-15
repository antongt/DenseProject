#ifndef RVD_PROBLEM_H
#define RVD_PROBLEM_H

#include <iostream>
#include <fstream>
#include <sstream>
//#include <cstdlib>
#include <climits>

// The maximum numbers of nodes and graphs are hardcoded.
#define MAXNUMNODES 32
#define MAXNUMGRAPHS 32

// Defines which data type is used to hold the nodes.
// This must be at least one bit for each node in MAXNUMNODES.
// alternatives are unsigned long or unsigned long long.
typedef unsigned int bitVector;

/*
 * The Problem class describes a DCS (Densest Common Subgraph) problem,
 * consisting of a set of nodes and one or more sets of edges over those
 * nodes.
 */
class Problem {
public:
    Problem();
//    ~Problem();
    bool readGraph(char* fileName);
    int nodeIdToIndex(int nodeIds[], int id);
    const int getNumGraphs();
    bool checkBitvectorSize();
private:

    // The input graphs may not have nodes numbered 0,1,2,3,...
    // They must be renumbered and this map remembers the original id for
    // when the solution is returned.
    int nodeIds[MAXNUMNODES];

    // The number of nodes in the input graphs.
    int numNodes;
    // The number of graphs in the problem.
    int numGraphs;

    // The edge sets.
    // It is a 1-dimensional vector, so if node A is connected to node B
    // in edge set E, then edges[E*MAXNUMNODES+A] & 1 << B is true.
    // Note that the edges are undirected. To avoid problems with
    // redundant data, A <= B.
    bitVector edges[MAXNUMGRAPHS * MAXNUMNODES];
};

#endif // RVD_PROBLEM_H

