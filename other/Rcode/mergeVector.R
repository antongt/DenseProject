graphmetrics <- function(edges){
  library(igraph)
  graph = make_graph(mergeVectors(edges[,1],edges[,2]))
  diameter = igraph::diameter(graph,directed = FALSE,unconnected = TRUE)
  tri = igraph::triangles(graph)
  triangleDensity = (length(tri)/3)/choose(length(unique(unlist(edges))),3)
  return(list(diameter,triangleDensity))
}

mergeVectors <- function(a,b){
  res = vector(length = 2*length(a))
  for(i in 1:length(a)){
    res[2*i-1] = a[i]
    res[2*i] = b[i]
  }
  return(res)
}