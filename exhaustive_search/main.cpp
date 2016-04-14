/*
 * This program performs an exhaustive search to find the densest common
 * subgraph of a set of (undirected) graphs over the same set of nodes.
 *
 * Since exhaustive search is not intended for large graphs, the nodes will be
 * stored in an integer interpreted as a bit vector. If bit N is 1, then node N
 * is in the solution, if the bit is zero the node is not in the solution.
 * That way it is easy to iterate over all possible solutions simply by
 * incrementing the integer until it reaches all ones.
 *
 * Edges are stored as an array of integers, one integer for every node. These
 * integers are also bit vectors indicating which nodes are connected.
 */

#include <iostream>
#include <cstdlib>
#include <climits>
#include <cassert>
#include <fstream>
#include <sstream>

// The maximum numbers of nodes and graphs are hardcoded.
#define MAXNUMNODES 32
#define MAXNUMGRAPHS 32

// Defines which data type is used to hold the nodes.
// This could be changed to unsigned long or unsigned long long for more nodes.
typedef unsigned int bitVector;

bool readGraph(int* graph, char* fileName);
int nodeIdToIndex(int nodeIds[], int id);
bool checkBitvectorSize();
bool checkCommandLineArgs(int argc);

int main(int argc, char** argv)
{
    // Do some initial checks to see that everything(?) is in order.
    if(!checkBitvectorSize() || !checkCommandLineArgs(argc)) {
        std::cerr << "Exiting." << std::endl;
        exit(EXIT_FAILURE);
    }

    // The input graphs may not have nodes numbered 0,1,2,3,...
    // They must be renumbered and this map remembers the original id for
    // when the solution is returned.
    int nodeIds[MAXNUMNODES];
    for(int i=0; i<MAXNUMNODES; ++i)
        nodeIds[i] = INT_MAX; // Initialized to an invalid value.

    // The number of nodes in the input graphs.
    int numNodes = 0;

    // The edge sets.
    // It is a 1-dimensional vector, so if node A is connected to node B
    // in edge set E, then edges[E*MAXNUMNODES+A] & 1 << B is true.
    // Note that the edges are undirected. To avoid problems with
    // redundant data, A <= B.
    bitVector edges[MAXNUMGRAPHS * MAXNUMNODES];
    for(int i=0; i<MAXNUMGRAPHS * MAXNUMNODES; ++i)
        edges[i] = 0;

    // Read files supplied as command line arguments.
    int numGraphs = 0;
    for(int i=1; i<argc; ++i) {
        std::cout << "Reading file " << argv[i];
        if(readGraph(&i, argv[i])) {
            std::cout << "\t\t-- successful" << std::endl;
            ++numGraphs;
        } else {
            std::cout << "\t\t-- failed     (!)" << std::endl;
        }
    }
    std::cout << numGraphs << " read successfully." << std::endl;

}

/*
 * Make sure a bitVector is big enough to hold all the nodes.
 * If not, the program will not be able to run on this computer.
 * Terminates the program if there is a problem.
 */
bool checkBitvectorSize()
{
    if(sizeof(bitVector)*CHAR_BIT < MAXNUMNODES){
        std::cerr << "The maximum number of nodes is too large for this"
           << " architecture and compiler." << std::endl;
        return false;
    }
    return true;
}

/*
 * Check that there aren't too few or too many arguments.
 * Terminates the program if there is a problem.
 */
bool checkCommandLineArgs(int argc)
{
    // Make sure at least one filename is given.
    if(argc<2) {
        std::cerr << "No files supplied." << std::endl
            << "Please provide file names on the command line." << std::endl;
        return false;
    }
    // Make sure the number of graphs is not too many.
    if(argc-1 > MAXNUMGRAPHS) {
        std::cerr << "Too many graphs! This program can only handle "
            << MAXNUMGRAPHS << " graphs" << std::endl;
        return false;
    }
    return true;
}

/*
 * Graphs should be stored in files consisting of comments beginning with #
 * and edges written as two integers (source and destination node id). 
 */
bool readGraph(int* graph, char* fileName)
{
    std::ifstream f(fileName);
    if(!f) {
        return false;
    }
    std::string line;
    while(std::getline(f, line)) {
        if(line[0] != '#') {
            std::istringstream iss(line);
            unsigned int a, b;
            //if(iss >> a >> b)
                //addEdge(a, b);
        }
    }
    return true;
}

/*
 * Use the map nodeIds to find the index of a node. If the node isn't found,
 * a -1 is returned. Always check for this after calling this function!
 */
int nodeIdToIndex(int nodeIds[], int id)
{
    for(int i=0; i<MAXNUMNODES; ++i)
        if(nodeIds[i] == id)
            return i;
    return -1;
}

