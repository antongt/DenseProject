#ifndef RVD_LAYOUT_H
#define RVD_LAYOUT_H

#include <utility>
#include <cmath>
#include <iostream>

typedef std::pair<double, double> Coordinates;
unsigned int getGridSize(unsigned int numNodes);
unsigned int getMaxNodes(unsigned int gridSize);
double getHexagonWidth(unsigned int gridSize);
Coordinates getCoords(unsigned int n, unsigned int gridSize);

#endif // RVD_LAYOUT_H
