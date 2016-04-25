#include "problem.h"

/*
 * Defining this causes more output to be printed.
 */
// #define DEBUGPRINTING

/*
 * Check that the integer datatype is big enough to hold all the nodes.
 */
bool checkBigEnoughIntegers()
{
    return sizeof(nodeSet)*CHAR_BIT >= MAXNUMNODES;
}


Problem::Problem() : numNodes(0), numGraphs(0)
{
    for(int i=0; i<MAXNUMNODES; ++i)
        nodeIds[i] = 0;
}


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
    if(fromId == -1 || toId == -1) {
        std::cerr << "Error, invalid node id in edge (" <<
            from << ", " << to << ")" << std::endl;
        return;
    }
    edgeSets[graph].set(getEdgeIndex(fromId, toId));
}


/*
 * The edges are true/false values stored in a matrix such that if there is an
 * edge between A and B, then the cell at row A and column B is true.
 * However, since the graph is undirected, cell AB has the same value as cell
 * BA. Also, since there are no self edges, the diagonal where row = column is
 * also unnecessary. So to avoid wasting memory, the values are stored in a
 * one-dimensional array.
 *
 * How does one figure out which index a specific edge (n1, n2) has?
 * (See figure below)
 * Assume n1 > n2. Row and column numbering start at 0.
 * Choose row n1.
 * First index on that row equals n1*(n1-1)/2 = (n1*n1-n1)/2.
 * Add n2 to get the index.
 *
 *                  n2
 *          0   1   2   3   4
 *        ------------------
 *      0|
 *      1|  0
 *  n1  2|  1   2
 *      3|  3   4   5
 *      4|  6   7   8   9
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
    // Avoid a division by zero. If no nodes, return density as 0.
    if(solution == 0)
        return 0;
    // Find the minimum number of edges among all the edge sets.
    int minEdges = getNumEdges(solution, 0);
    for(int i=1; i<numGraphs; ++i) {
        int edges = getNumEdges(solution, i);
        if(edges < minEdges)
            minEdges = edges;
    }
    return ((double)minEdges)/getNumNodesInSolution(solution);
}


/*
 * The number of nodes in a solution is the number of bits set to 1.
 * TODO: Is there a smarter way?
 */
int Problem::getNumNodesInSolution(nodeSet solution)
{
    int result = 0;
    for(int i=0; i<numNodes; ++i)
        if(isNodeInSolution(i, solution))
            ++result;
    return result;
}


bool Problem::isNodeInSolution(int node, nodeSet solution)
{
    return solution & (1<<node);
}


/*
 * Get the number of edges for a specific edge set and solution.
 *
 * TODO: Instead of iterating over the nodes and calculating an index every
 * time, would it be faster to iterate over the bitset and keeping track of
 * how the values of the nodes change instead?
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
    while(++solution < lastSolution) {
        double density = getDensity(solution);
#ifdef DEBUGPRINTING
        std::cout << "Solution " << solution <<
            " has density " << density << std::endl;
#endif
        if(density > bestDensity) {
            bestDensity = density;
            bestSolution = solution;
        }
    }
    std::cout << "Largest density found was ";
    std::cout << std::setprecision(12) << bestDensity;
    std::cout << " for solution " << bestSolution << "." << std::endl;
    std::cout << "This solution includes the following " << 
        getNumNodesInSolution(bestSolution) << " nodes:" << std::endl;
    printNodesInSolution(bestSolution);
}


/*
 * Given a solution, translate those indexes back to ids in the original input
 * files and print a sorted column of all the nodes in that solution.
 */
void Problem::printNodesInSolution(nodeSet solution)
{
    std::vector<int> nodeVec;
    // Add node ids to the vector.
    for(int i=0; i<numNodes; ++i)
        if(isNodeInSolution(i, solution))
            nodeVec.push_back(nodeIds[i]);
    // Sort and print the ids.
    std::sort(nodeVec.begin(), nodeVec.end());
    for(std::vector<int>::iterator it=nodeVec.begin(); it!=nodeVec.end(); ++it)
        std::cout << *it << std::endl;
}

