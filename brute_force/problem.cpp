#include "problem.h"

/*
 * Check that the integer datatype is big enough to hold all the nodes.
 */
bool checkBigEnoughIntegers()
{
    return sizeof(nodeSet)*CHAR_BIT >= MAXNUMNODES;
}

Problem::Problem() : numNodes(0), numGraphs(0)
{
    // Initialized to an invalid value.
    for(int i=0; i<MAXNUMNODES; ++i)
        nodeIds[i] = INT_MAX;

    // Edges initialized to all non-existing.
    //for(int i=0; i<MAXNUMGRAPHS * MAXNUMNODES; ++i)
    //    edges[i] = 0;
}

//Problem::~Problem()
//{}

/*
 * Graphs should be stored in files consisting of comments beginning with #
 * and edges written as two integers (source and destination node id). 
 */
bool Problem::readGraph(char* fileName)
{
    std::ifstream f(fileName);
    if(!f) {
        return false;
    }
    std::string line;
    while(std::getline(f, line)) {
        if(line[0] != '#') {
            std::istringstream iss(line);
            int a, b;
            if(iss >> a >> b)
                setEdge(a, b, numGraphs);
        }
    }
    // TODO: More checks here before it is declared successful?
    //std::cout << "Read complete: " << edgeSets[numGraphs] << std::endl;
    ++numGraphs;
    return true;
}

/*
 * Use the map nodeIds to find the index of a node. If the node isn't found,
 * add it. If there is no more room, returns -1.
 */
int Problem::nodeIdToIndex(int id)
{
    // Exists?
    for(int i=0; i<numNodes; ++i)
        if(nodeIds[i] == id)
            return i;
    // No more room?
    if(numNodes >= MAXNUMNODES) {
        std::cerr << "Too many nodes, can't add node " << id << std::endl;
        return -1;
    }
    // Room to add it.
    nodeIds[numNodes] = id;
    //std::cout << "Adding node " << id << " as index " << numNodes << std::endl;
    return numNodes++; // Return the value before incrementing.
}

const int Problem::getNumGraphs()
{
    return numGraphs;
}

void Problem::setEdge(int from, int to, int graph)
{
    int fromId = nodeIdToIndex(from);
    int toId = nodeIdToIndex(to);
    if(fromId == -1 || toId == -1)
        return; // Error.
    edgeSets[graph].set(getEdgeIndex(fromId, toId));
}

/*
 * How does one figure out which index a specific edge (n1, n2) has?
 * (See figure below)
 * Assume n1 > n2.
 * Choose row n1.
 * First index on that row equals n1*(n1-1)/2 = (n1*n1-n1)/2.
 * Add n2 to get the index.
 *
 *      A   B   C   D   E
 *  A
 *  B   0
 *  C   1   2
 *  D   3   4   5
 *  E   6   7   8   9
 */
int Problem::getEdgeIndex(int n1, int n2)
{
    if(n1 > n2)
        return (n1*n1-n1)/2+n2;
    return (n2*n2-n2)/2+n1;
}

/*
 * Get the minimum density among all the edge sets for a solution.
 */
double Problem::getDensity(nodeSet solution)
{
    // Avoid a division by zero. If no nodes, density is 0.
    if(getNumNodesInSolution(solution) == 0)
        return 0;

    int min = getNumEdges(solution, 0);
    for(int i=1; i<numGraphs; ++i) {
        int density = getNumEdges(solution, i);
        if(density < min)
            min = density;
    }
    return (double)min/getNumNodesInSolution(solution);
}

/*
 * The number of nodes in a solution is the number of bits set to 1.
 * TODO: Is there a smarter way?
 */
int Problem::getNumNodesInSolution(nodeSet solution)
{
    int result = 0;
    for(int i=0; i<MAXNUMNODES; ++i)
        if((solution & (1<<i)) != 0)
            ++result;
    return result;
}

bool Problem::isNodeInSolution(int node, nodeSet solution)
{
    return (solution & (1<<node)) != 0;
}

/*
 * Get the density for a specific edge set and solution.
 * The density is the number of edges divided by number of nodes.
 */
int Problem::getNumEdges(nodeSet solution, int edgeSetNum)
{
    int result = 0;
    for(int n2 = 1; n2<numNodes; ++n2)
        if(isNodeInSolution(n2, solution))
            for(int n1 = 0; n1<n2; ++n1)
                if(isNodeInSolution(n1, solution))
                    if(edgeSets[edgeSetNum].test(getEdgeIndex(n1, n2)))
                        ++result;
    // TODO: it would be faster to iterate over the bitset and keeping track
    // of the values of the nodes?
//    int index = 0;
//    int n2 = 1;
//    while(n2 < numNodes) {
//        n1 = 0;
//        while(n1 < n2) {
//            if(edgeSets[edgeSetNum].test(index))
//                ++result;
//            ++index;
//            ++n1;
//        }
//        ++n2;
//    }
    return result;
}

/*
 * Since this is a brute force solution, iterate through every possible
 * solution and find the best.
 */
void Problem::solve()
{
    nodeSet solution = 0;
    nodeSet lastSolution = (1<<numNodes);
    nodeSet bestSolution = 0;
    double bestDensity = 0;
    while(solution < lastSolution) {
        //std::cout << "Testing solution " << solution;
        double density = getDensity(solution);
        //std::cout << ", density = " << density << std::endl;
        if(density > bestDensity) {
            bestDensity = density;
            bestSolution = solution;
        }
        ++solution;
    }
    std::cout << "Largest density found was " << bestDensity;
    std::cout << " for solution " << bestSolution << std::endl;
    std::cout << "This solution includes the following nodes:" << std::endl;
    printNodesInSolution(bestSolution);
}

/*
 * Given a solution, translate those indexes back to ids in the original input
 * files and print a sorted column of all the nodes in that solution.
 */
void Problem::printNodesInSolution(nodeSet solution)
{
    std::vector<int> nodeVec;
    // Add nodes to the vector.
    for(int i=0; i<numNodes; ++i)
        if(isNodeInSolution(i, solution))
            nodeVec.push_back(nodeIds[i]);
    // Sort the vector.
    std::sort(nodeVec.begin(), nodeVec.end());
    // Print the ids.
    for(std::vector<int>::iterator it=nodeVec.begin(); it!=nodeVec.end(); ++it)
        std::cout << *it << std::endl;
}

