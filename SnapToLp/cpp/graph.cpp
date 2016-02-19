#include "graph.h"

Graph::Graph() : Graph(false)
{}

Graph::Graph(bool isDirectedGraph) :
    nodes(),
    directed(isDirectedGraph),
    numEdges(0)
{}

Graph::Graph(const Graph& g) :
    nodes(g.nodes),
    directed(g.directed),
    numEdges(g.numEdges)
{}

/*
 * Load a graph from a file. The file should consist of comment lines starting
 * with '#' and pairs of integers representing an edge. Nodes will be added when
 * they appear as part of an edge description.
 */
bool Graph::openFile(char* fileName)
{
    std::ifstream f(fileName);
    if(!f) {
        return false;
    }
    std::string line;
    while(std::getline(f, line)) {
        if(line[0] != '#') {
            std::istringstream iss(line);
            Node a, b;
            if(iss >> a >> b)
                addEdge(a, b);
        }
    }
    return true;
}

/*
 * Return the densest subgraph.
 * Algorithm:
 * Repeatedly remove the smallest degree node, until all nodes are gone.
 * Each step, remember the density.
 * Finally, return the set that had the highest density.
 */
std::unique_ptr<Graph> Graph::getDensestSubgraph() const
{
    // First pass, find the value of the highest density.
    // Make a copy of the graph so that we can remove nodes.
    Graph g = *this;
    double highestDensity = getDensity();
    while(!g.nodes.empty()) {
        g.removeSmallestDegreeNode();
        if(g.getDensity() > highestDensity)
            highestDensity = g.getDensity();
    }
        
    // Second pass, find the graph with the highest density.
    // Comparing doubles, risk of rounding errors? Should be ok since it's the
    // exact same division.
    g = *this;
    while(!g.nodes.empty()) {
        g.removeSmallestDegreeNode();
        if(g.getDensity() >= highestDensity)
            break;
    }

    return std::make_unique<Graph>(g);
}

/*
 * Return the highest numbered node in the set.
 */
Node Graph::getHighestNode() const
{
    Node result = 0;
    for(auto node : nodes)
        if(node.first > result)
            result = node.first;
    return result;
}

/*
 * This could be made faster by having a sorted map of degree -> node. Whenever
 * a node is removed, only those connected to the removed node needs to be
 * updated. Requires undirected graph, or more bookkeeping for directed graphs.
 */
unsigned int Graph::getSmallestDegree() const
{
    unsigned int smallestDegree = UINT_MAX;
    for(auto node : nodes)
        if(node.second.size() < smallestDegree)
            smallestDegree = node.second.size();
    return smallestDegree;
}

void Graph::removeSmallestDegreeNode()
{
    auto smallestDegree = getSmallestDegree();
    for(auto node : nodes) {
        if(smallestDegree == node.second.size()) {
            removeNode(node.first);
            break;
        }
    }
}

unsigned int Graph::getDegree(Node n) const
{
    auto it = nodes.find(n);
    return it != nodes.end() ? it->second.size() : 0;
}

void Graph::addNode(Node n)
{
    if(nodes.count(n) == 0)
        nodes.insert(std::make_pair(n, NodeSet()));
}

/*
 * Remove a node and all its connected edges.
 * Does not work for directed graphs. Would have to iterate through all nodes to
 * remove edges that end on node n.
 */
void Graph::removeNode(Node n)
{
    if(directed) {
        std::cerr << "removeNode() does not work for directed graphs" << std::endl;
        return;
    }
    auto it = nodes.find(n);
    if(it == nodes.end())
        return;
    while(!it->second.empty()) {
        removeEdge(*it->second.begin(), it->first);
        removeEdge(it->first, *it->second.begin());
    }
    // Do we need to find again? nodes hasn't been modified, but edges has.
    nodes.erase(it);
}

void Graph::addEdge(Node from, Node to)
{
    addDirectedEdge(from, to);
    if(!directed)
        addDirectedEdge(to, from);
}

void Graph::removeEdge(Node from, Node to)
{
    auto it = nodes.find(from);
    if(it == nodes.end())
        return;
    if(it->second.count(to)) {
        it->second.erase(to);
        --numEdges;
    }
}

void Graph::addDirectedEdge(Node from, Node to)
{
    addNode(from);
    addNode(to);

    auto it = nodes.find(from);
    if(it != nodes.end()) {
        auto result = it->second.insert(to);
        if(result.second)
            ++numEdges;
    }
}

