#include <iostream>
#include "graph.h"
#include "graphGen.h"
#include "svg.h"
#include "layout.h"

void printGraphStats(const Graph& g)
{
    const bool PRINT_NODES = false;
    const bool PRINT_EDGES = false;

    std::cout << "Graph has " << g.getNumNodes() << " nodes and ";
    std::cout << g.getNumEdges() << " edges." << std::endl;
    std::cout << "The density is " << g.getDensity() << std::endl;

    if(PRINT_NODES) {
        std::cout << "Nodes:";
        for(auto node : g.nodes)
            std::cout << std::endl << node.first;
        std::cout << std::endl;
    }

    if(PRINT_EDGES) {
        std::cout << "Edges:";
        for(auto from : g.nodes) {
            std::cout << std::endl << from.first << " ->";
            for(auto to : from.second)
                std::cout << " " << to;
        }
        std::cout << std::endl;
    }
}

int main(int argc, char** argv)
{
    if(argc != 2) {
        std::cout << "Usage: " << argv[0] << " <filename>" << std::endl;
        exit(0);
    }

    auto graph = Graph();
    if(!graph.openFile(argv[1])) {
        std::cerr << "Error loading file " << argv[1] << std::endl;
        exit(1);
    }

    printGraphStats(graph);

    //auto densestSubGraph = graph.getDensestSubgraph();
    //printGraphStats(*densestSubGraph);

    //auto gg = GraphGenerator();
    SVG_Image svg;
    //auto gridSize = getGridSize(graph.getHighestNode());
    auto gridSize = getGridSize(graph.getNumNodes());
    std::cout << gridSize << "sixe" << std::endl;
    svg.drawGraph(graph, gridSize);
    svg.save("out.svg");
}

