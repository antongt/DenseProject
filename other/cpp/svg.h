#ifndef RVD_SVG_H
#define RVD_SVG_H

#include <pugixml.hpp>
#include <iostream>
#include <iomanip>
#include <sstream>
#include "graph.h"
#include "layout.h"

// Precision of attributes when saving to file. Since numbers are saved as text,
// reducing this can save a lot of space in a big save file.
const int ATTRIBUTE_PRECISION = 4;

typedef std::pair<double, double> Coordinates;

class SVG_Image {
public:
    SVG_Image();
    void drawGraph(const Graph& g, unsigned int gridSize);
    void drawNode(Node node);
    void drawEdge(Node from, Node to);
    void save(const char*);
private:
    void init_xml();
    std::string getAttrStr(double n) const;
    pugi::xml_document doc;
    pugi::xml_node nodes;
    pugi::xml_node edges;
    unsigned int gridSize;
    double hexWidth;
    double nodeRadius;
    double nodeThickness;
    double edgeThickness;
};

#endif // RVD_SVG_H
