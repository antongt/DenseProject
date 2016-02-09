txtToLp <- function(files){
  edgesets = list()
  for (i in 1:length(files)){
    edgesets[[i]]=read.table(files[i],sep = "\t")
  }
  nodes = unlist(edgesets[[1]])
  if (length(edgesets)>1){
    for( i in 2:length(edgesets)){
      nodes = intersect(nodes,unlist(edgesets[[i]]))
    }
  }
  maxN = max(nodes)
  present = vector(length = maxN)
  present[nodes] = TRUE #sets all nodes that have "survived" the intersets to true
  edgetexts = vector(length = length(edgesets)) #vector that saves the strings
  for( f in 1:length(files)){
    seekedEdges = vector(length = length(edgesets[[f]][,1])) #true false vector if we want that edge
    numberOfEdges = 0 #number of edges that we want
    for (i in 1:length(edgesets[[f]][,1])){
      if(present[edgesets[[f]][i,1]]&&present[edgesets[[f]][i,2]]){
        seekedEdges[i] = TRUE
        numberOfEdges = numberOfEdges + 1
      }
    }
   edgetexts[f] = paste("x",f,"_",1:numberOfEdges,"<=","y_",unlist(edgesets[[f]][seekedEdges,]),sep = "",collapse = "\n")
   
  }
  nodetexts = paste("y_",nodes,">=0",sep = "",collapse = "\n") #all the constraints for the nodes
  return(c(edgetexts,nodetexts))
}