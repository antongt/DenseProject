#ifndef RVD_GRAPH_H
#define RVD_GRAPH_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <unordered_map>
#include <memory>
#include <climits>

typedef unsigned int Node;
typedef std::set<Node> NodeSet;

class Graph {
public:
    Graph();
    Graph(bool directed);
    Graph(const Graph& g);
    bool openFile(char* fileName);
    unsigned int getNumNodes() const { return nodes.size(); }
    unsigned int getNumEdges() const { return directed ? numEdges : numEdges/2; }
    Node getHighestNode() const;
    double getDensity() const { return (double)getNumEdges()/(double)getNumNodes(); }
    bool isDirectedGraph() const { return directed; }
    unsigned int getDegree(Node n) const;
    unsigned int getSmallestDegree() const;
    void removeSmallestDegreeNode();
    void addNode(Node n);
    void removeNode(Node n);
    void addEdge(Node from, Node to);
    void removeEdge(Node from, Node to);
    std::unique_ptr<Graph> getDensestSubgraph() const;

    std::unordered_map<Node, NodeSet> nodes;
private:
    void addDirectedEdge(Node from, Node to);

    bool directed;
    unsigned int numEdges;
};

#endif // RVD_GRAPH_H
