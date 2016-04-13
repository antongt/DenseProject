#include <iostream>
#include <cstdlib>
#include <climits>
#include <cassert>
#include <fstream>
#include <sstream>

/*
 * Since exhaustive search is not intended for large graphs, the nodes will be
 * stored in an integer interpreted as a bit vector.
 * Edges are stored as an array of integers, one integer for every node. These
 * integers are also bit vectors indicating which nodes are connected.
 */

#define MAXNUMNODES 32
typedef unsigned int bitVector;

bool readGraph(int* graph, char* fileName);

int main(int argc, char** argv)
{
    // Make sure a bitVector is big enough to hold all the nodes.
    // If not, change the typedef to long or long long or something.
    assert(sizeof(bitVector)*CHAR_BIT >= MAXNUMNODES);

    if(argc<2) {
        std::cerr << "No files supplied. Please provide file names on the ";
        std::cerr << "command line." << std::endl;
        exit(EXIT_FAILURE);
    }

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

