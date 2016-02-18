#ifndef RVD_GRAPHGEN_H
#define RVD_GRAPHGEN_H

#include <iostream>
#include <cstdio>
#include <cmath>
#include <random>
#include <vector>
#include "graph.h"
#include "layout.h"

class GraphGenerator{
public:
    GraphGenerator();
    GraphGenerator(unsigned int num);
    Graph g;
    void generate();
    std::pair<int, int> getCoords(Node n);
    bool isInside(Node n);
//    static unsigned int getGridSize(unsigned int numNodes);
//    static unsigned int getMaxNodes(unsigned int gridSize);
    int gridSize;
private:
    Node pickRandomNode() const;
    Node pickRandomNeighbor() const;
    unsigned int numNodes;
    unsigned int maxNodes;
};

#endif //RVD_GRAPHGEN_H
