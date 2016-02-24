#include "graphGen.h"

/*
 * The layout uses a hexagonal grid of 2N-1 rows (an odd number of rows). The
 * top row has N nodes, alternating rows have N-1 nodes. The total number of
 * nodes are 2N^2-2N+1 and the nodes are placed with node 1 in the top left
 * corner and increasing to the right and down.
 *
 * The parameter N is stored in the variable gridSize and is calculated
 * such that it is the smallest value that can accommodate the
 * requested number of nodes.
 */

GraphGenerator::GraphGenerator() : GraphGenerator(100)
{}

GraphGenerator::GraphGenerator(unsigned int requestedNumNodes) :
    numNodes(requestedNumNodes)
{
    gridSize = getGridSize(numNodes);
    maxNodes = getMaxNodes(gridSize);
    std::cout << "GridSize " << gridSize << " can accommodate "
        << maxNodes << " nodes." << std::endl;
}

/*
 * To find gridSize, solve the quad equation
 * 2x^2-2x+1=N -> x^2-x+(1-N)/2 = 0
 * Solve using (and ignoring the negative solution of)
 * https://en.wikipedia.org/wiki/Quadratic_equation#Reduced_quadratic_equation
 */
/*
unsigned int GraphGenerator::getGridSize(unsigned int numNodes)
{
    double p = -1;
    double q = (1-numNodes)/2.f;
    double x = 0.5*(-p+std::sqrt(p*p-4*q));
    return std::rint(std::ceil(x));
}
 */
/*
 * Inverse of the function getGridSize, although that function rounds up and
 * this is exact.
 */
/*
unsigned int GraphGenerator::getMaxNodes(unsigned int gridSize)
{
    return 2*gridSize*gridSize-2*gridSize+1;
}
 */

void GraphGenerator::generate()
{
    g = Graph();
}

bool GraphGenerator::isInside(Node n)
{
    return (n>0 && n<=maxNodes);
}

Node GraphGenerator::pickRandomNode() const
{
    std::default_random_engine rng;
    std::uniform_int_distribution<Node> int_distr(0, g.getNumNodes()-1);
    return int_distr(rng);
}

Node GraphGenerator::pickRandomNeighbor() const
{
    std::default_random_engine rng;
    std::uniform_int_distribution<int> int_distr(0, 5);
    int choice = int_distr(rng);
    switch(choice) {
        case 0:
            break;
        case 1:
            break;
        case 2:
            break;
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
    }
    
    return 0;
}

