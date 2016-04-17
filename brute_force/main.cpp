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
#include "problem.h"

bool checkCommandLineArgs(int argc);

int main(int argc, char** argv)
{
    Problem *problem = new Problem();

    // Do some initial checks to see that everything(?) is in order.
    if( !checkBigEnoughIntegers()) {
        std::cerr << "This architecture or compiler does not have large "
            << "enough integers for this program to run." << std::endl;
        exit(EXIT_FAILURE);
    }
    if( !checkCommandLineArgs(argc) ) {
        exit(EXIT_FAILURE);
    }

    // Read files supplied as command line arguments.
    for(int i=1; i<argc; ++i) {
        std::cout << "Reading file " << argv[i];
        if(problem->readGraph(argv[i])) {
            std::cout << "\t\t-- successful" << std::endl;
        } else {
            std::cout << "\t\t-- failed     (!)" << std::endl;
        }
    }
    std::cout << problem->getNumGraphs() << " read successfully." << std::endl;
    problem->solve();
    delete problem;
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
