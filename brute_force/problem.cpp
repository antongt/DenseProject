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
int Problem::getEdgeIndex(int n1, int n2) const
{
    if(n1 > n2)
        return (n1*n1-n1)/2+n2;
    return (n2*n2-n2)/2+n1;
}


/*
 * Get the minimum density among all the edge sets for a solution.
 */
double Problem::getDensity(nodeSet solution) const
{
    // Avoid a division by zero. If no nodes, return density as 0.
    if(solution == 0)
        return 0;
    // Find the minimum number of edges among all the edge sets.
    int minEdges = getMinimumEdges(solution);
    return ((double)minEdges)/getNumNodesInSolution(solution);
}


/*
 * Get the minimum number of edges for a solution among all edge sets.
 */
int Problem::getMinimumEdges(nodeSet solution) const
{
    // Results for each edge set stored here.
    int result[numGraphs];
    for(int i=0; i<numGraphs; ++i)
        result[i] = 0;
    // Iterate through every possible edge and update result.
    for(int n2 = 1; n2<numNodes; ++n2) {
        if(!isNodeInSolution(n2, solution))
            continue;
        for(int n1 = 0; n1<n2; ++n1) {
            if(!isNodeInSolution(n1, solution))
                continue;
            for(int ei=0; ei<numGraphs; ++ei)
                if(edgeSets[ei].test(getEdgeIndex(n1, n2)))
                    ++result[ei];
        }
    }
    // Find the smallest value in the array.
    int minimum = INT_MAX;
    for(int i=0; i<numGraphs; ++i)
        if(result[i]<minimum)
            minimum=result[i];
    return minimum;
}


/*
 * The number of nodes in a solution is the number of bits set to 1.
 * This is called the Hamming Weight or popcount.
 * The function calls the GCC built-in function, which should use the CPU
 * built-in function if such a function is available. 
 *
 * Note that if this program is changed to use another nodeSet, such as
 * unsigned long or unsigned long long, the name of the GCC built-in function
 * changes. See https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html
 * For some more on Hamming Weight functions, see also
 * https://stackoverflow.com/questions/109023/how-to-count-the-number-of-set-bits-in-a-32-bit-integer
 */
int Problem::getNumNodesInSolution(nodeSet solution) const
{
    return __builtin_popcount(solution);
}


bool Problem::isNodeInSolution(int node, nodeSet solution) const
{
    return solution & (1<<node);
}


/*
 * Finds the solution by splitting the problem into smaller parts.
 * This allows multiple threads to work on the problem at the same time.
 */
void Problem::solve()
{
    const int numThreads = 4;
    // This array stores the solutions of the subproblems.
    nodeSet candidates[numThreads];
    // Calculate how large each subproblem is.
    nodeSet intervalSize = (1 << numNodes) / numThreads;
    std::thread workers[numThreads];
    for(int t = 0; t<numThreads; ++t) {
        nodeSet from = t*intervalSize + 1;
        nodeSet to = (t+1)*intervalSize;
        // Make sure the last interval is exactly correct, the division might
        // lose some solutions otherwise(?).
        if(t==numThreads-1)
            to = (1 << numNodes)-1;
        std::cout << "Thread " << t <<
            " testing solution " << from << " to " << to << std::endl;
        workers[t] = std::thread(solveSubproblem, this, from, to, &candidates[t]);
    }
    // Wait for all threads to finish.
    for(int t=0; t<numThreads; ++t)
        workers[t].join();
    // Find the best solution among the interval winners.
    nodeSet solution = 0;
    for(int i=0; i<numThreads; ++i)
        if(getDensity(candidates[i]) > getDensity(solution))
            solution = candidates[i];
    std::cout << std::setprecision(12) << "Largest density found was " <<
        getDensity(solution) << " for solution " << solution << "." <<
        std::endl << "This solution includes the following " << 
        getNumNodesInSolution(solution) << " nodes:" << std::endl;
    printNodesInSolution(solution);
}


/*
 * Given a solution, translate those indexes back to ids in the original input
 * files and print a sorted column of all the nodes in that solution.
 */
void Problem::printNodesInSolution(nodeSet solution) const
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


/*
 * Since this is a brute force solution, iterate through every possible
 * solution between firstCandidate and lastCandidate and find the one
 * with the highest density.
 */
nodeSet Problem::solveInterval(nodeSet first, nodeSet last) const
{
    nodeSet best = 0;
    double highestDensity = 0;
    for(nodeSet candidate = first; candidate <= last; ++candidate) {
        double candidateDensity = getDensity(candidate);
        if(candidateDensity > highestDensity) {
            highestDensity = candidateDensity;
            best = candidate;
        }
    }
    return best;
}


void solveSubproblem(Problem *problem, nodeSet first, nodeSet last, nodeSet *best)
{
    *best = problem->solveInterval(first, last);
}

