#ifndef RVD_PROBLEM_H
#define RVD_PROBLEM_H

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <climits>
#include <bitset>
#include <vector>
#include <algorithm>

// The maximum numbers of nodes and graphs are hardcoded.
#define MAXNUMNODES 32
#define MAXNUMGRAPHS 32

/*
 * Defines which data type is used to hold the nodes.
 * This must be at least one bit for each node in MAXNUMNODES.
 * Most architectures/compilers should have at least 32 bit integers
 * but there is a check when starting the program just in case.
 * The reason to use int rather than bitset is that it's easier
 * to increment by one when stepping through possible solutions.
 * (Each value of this int is a possible solution.)
 */
typedef unsigned int nodeSet;
bool checkBigEnoughIntegers();

/*
 * How many unique edges are there?
 * There are no self edges, and it's an undirectional graph.
 * First node can have N-1 edges, second can have N-2 and so on.
 * Totally N*(N-1)/2 = (N*N-N)/2 edges.
 *
 */
typedef std::bitset< (MAXNUMNODES * MAXNUMNODES - MAXNUMNODES) / 2 > edgeSet;

/*
 * The Problem class describes a DCS (Densest Common Subgraph) problem,
 * consisting of a set of nodes and one or more sets of edges over those
 * nodes.
 */
class Problem {
public:
    Problem();
    bool readGraph(char* fileName);
    const int getNumGraphs();
    void solve();
private:
    // Convert from node id in input data to index in internal data structure.
    int nodeIdToIndex(int id);

    // Add an edge. Also adds the nodes if they don't already exist.
    void setEdge(int from, int to, int graph);

    // Find index of a specific edge.
    int getEdgeIndex(int n1, int n2);

    // Calculate the density for a specific solution.
    double getDensity(nodeSet solution);

    // Get the number of nodes in a specific solution.
    int getNumNodesInSolution(nodeSet solution);

    // Test if node is present in a specific solution.
    bool isNodeInSolution(int node, nodeSet solution);

    // Get the number of edges in a specific solution and edge set.
    int getNumEdges(nodeSet solution, int edgeSetNum);

    // Print the nodes in the solution. Converts index->id and sorts.
    void printNodesInSolution(nodeSet solution);

    // The input graphs may not have nodes numbered 0,1,2,3,...
    // They must be renumbered and this map remembers the original id for
    // when the solution is returned.
    int nodeIds[MAXNUMNODES];

    // The number of nodes in the input graphs.
    int numNodes;
    // The number of graphs in the problem.
    int numGraphs;
    // The edge sets.
    edgeSet edgeSets[MAXNUMGRAPHS];
};

#endif // RVD_PROBLEM_H

