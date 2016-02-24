# This function for creating a copy of a graph object is from
# https://stackoverflow.com/questions/23133372/how-to-copy-a-graph-object-in-snap-py

import snap

def copyGraph(graph):
    tmpfile = '.copy.tmp'

    # Saving to tmp file
    FOut = snap.TFOut(tmpfile)
    graph.Save(FOut)
    FOut.Flush()

    # Loading to new graph
    FIn = snap.TFIn(tmpfile)
    graphtype = type(graph)
    new_graph = graphtype.New()
    new_graph = new_graph.Load(FIn)

    return new_graph
