#include "problem.h"

Problem::Problem() : numNodes(0), numGraphs(0)
{
    // Initialized to an invalid value.
    for(int i=0; i<MAXNUMNODES; ++i)
        nodeIds[i] = INT_MAX;

    // Edges initialized to all non-existing.
    for(int i=0; i<MAXNUMGRAPHS * MAXNUMNODES; ++i)
        edges[i] = 0;
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
            unsigned int a, b;
            //if(iss >> a >> b)
                //addEdge(a, b);
        }
    }
    // TODO: More checks here before it is declared successful?
    ++numGraphs;
    return true;
}

/*
 * Use the map nodeIds to find the index of a node. If the node isn't found,
 * a -1 is returned. Always check for this after calling this function!
 */
int Problem::nodeIdToIndex(int nodeIds[], int id)
{
    for(int i=0; i<MAXNUMNODES; ++i)
        if(nodeIds[i] == id)
            return i;
    return -1;
}

const int Problem::getNumGraphs()
{
    return numGraphs;
}

/*
 * Make sure a bitVector is big enough to hold all the nodes.
 * If not, the program will not be able to run on this computer.
 * Terminates the program if there is a problem.
 */
bool Problem::checkBitvectorSize()
{
    if(sizeof(bitVector)*CHAR_BIT < MAXNUMNODES){
        std::cerr << "The maximum number of nodes is too large for this"
           << " architecture and compiler." << std::endl;
        return false;
    }
    return true;
}

