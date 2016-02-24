#include "layout.h"

/*
 * To find gridSize, solve the quad equation
 * 2x^2-2x+1=N -> x^2-x+(1-N)/2 = 0
 * Solve using (and ignoring the negative solution of)
 * https://en.wikipedia.org/wiki/Quadratic_equation#Reduced_quadratic_equation
 */
unsigned int getGridSize(unsigned int numNodes)
{
    double p = -1.f;
    // The cast to double avoids an overflow problem.
    double q = (1-(double)numNodes)/2.f;
    double x = 0.5*(-p+std::sqrt(p*p-4*q));
    return std::rint(std::ceil(x));
}

/*
 * Inverse of the function getGridSize, although that function rounds up and
 * this is exact.
 */
unsigned int getMaxNodes(unsigned int gridSize)
{
    return 2*gridSize*gridSize-2*gridSize+1;
}

/*
 * The width of a hexagon, expressed in percent of the canvas.
 */
double getHexagonWidth(unsigned int gridSize)
{
    return 100.f/(gridSize-1);
}

Coordinates getCoords(unsigned int n, unsigned int gridSize)
{
    double hexWidth = getHexagonWidth(gridSize);
    // Shift one hex to the left, since nodes start from 1, not 0.
    double x = -hexWidth;
    double y = 0.f;
    // First find row.
    while(true) {
        // Odd rows.
        if(n > gridSize) {
            n -= gridSize;
            y += 0.5*hexWidth;
        } else {
            break;
        }
        // Even rows.
        if(n > gridSize-1) {
            n -= (gridSize-1);
            y += 0.5*hexWidth;
        } else {
            x = -0.5*hexWidth; // x is offset on even rows.
            break;
        }
    }
    // Then find column.
    x += n*hexWidth;
    return std::make_pair(x, y);
}

