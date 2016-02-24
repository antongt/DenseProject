#include "svg.h"

SVG_Image::SVG_Image() : doc(), nodes(), edges(), gridSize(0),
    hexWidth(0), nodeRadius(0), nodeThickness(0), edgeThickness(0)
{}

/*
 * Initialize the SVG file. SVG is just xml. Initialize from a string holding a
 * base SVG tag. Create groups for edges and nodes.
 */
void SVG_Image::init_xml()
{
    doc.load("<svg width=\"9cm\" height=\"7cm\" xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\"></svg>");
    pugi::xml_node rootNode = doc.child("svg");

    // If edges appear first in the document, they will be rendered "below"
    // the nodes for a clean appearance.
    edges = rootNode.append_child("g");
    edges.append_attribute("id") = "edges";
    edges.append_attribute("stroke") = "black";
    edges.append_attribute("stroke-width") = getAttrStr(edgeThickness).c_str();

    nodes = rootNode.append_child("g");
    nodes.append_attribute("id") = "nodes";
    nodes.append_attribute("fill") = "red";
    nodes.append_attribute("stroke") = "black";
    nodes.append_attribute("stroke-width") = getAttrStr(nodeThickness).c_str();
}

/*
 * Traverse the graph and draw all the elements. The order of edges vs nodes
 * doesn't matter here since the groups are already in the correct order.
 */
void SVG_Image::drawGraph(const Graph& g, unsigned int layoutGridSize)
{
    gridSize = layoutGridSize;
    hexWidth = getHexagonWidth(gridSize);
    std::cout << "Drawing a graph, gridsize = " << gridSize << std::endl;
    // Try to come up with good size for nodes and edges.
    nodeRadius = 0.2*hexWidth;
    nodeThickness = 0*nodeRadius;
    edgeThickness = 0.1*nodeRadius;
    init_xml();
    for(auto node : g.nodes) {
        drawNode(node.first);
        for(auto to : node.second) {
            drawEdge(node.first, to);
        }
    }
}

void SVG_Image::drawNode(Node node)
{
    auto nodeXY = getCoords(node, gridSize);
    pugi::xml_node xmlNode = nodes.append_child("circle");
    xmlNode.append_attribute("cx") = getAttrStr(nodeXY.first).c_str();
    xmlNode.append_attribute("cy") = getAttrStr(nodeXY.second).c_str();
    xmlNode.append_attribute("r") = getAttrStr(nodeRadius).c_str();
}

void SVG_Image::drawEdge(Node from, Node to)
{
    auto fromXY = getCoords(from, gridSize);
    auto toXY = getCoords(to, gridSize);
    pugi::xml_node xmlNode = edges.append_child("line");
    xmlNode.append_attribute("x1") = getAttrStr(fromXY.first).c_str();
    xmlNode.append_attribute("y1") = getAttrStr(fromXY.second).c_str();
    xmlNode.append_attribute("x2") = getAttrStr(toXY.first).c_str();
    xmlNode.append_attribute("y2") = getAttrStr(toXY.second).c_str();
}

/*
 * Save to file. Uses the pugixml save function.
 */
void SVG_Image::save(const char* fileName)
{
    if(!doc.save_file(fileName)) {
        std::cerr << "Saving file failed." << std::endl;
    }
}

/*
 * Convert double number to string, of some precision, and add percent-sign.
 */
std::string SVG_Image::getAttrStr(double n) const
{
    std::ostringstream oss;
    oss << std::setprecision(ATTRIBUTE_PRECISION) << n << "%";
    return oss.str();
}

