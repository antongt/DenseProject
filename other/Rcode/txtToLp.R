txtToLp <- function(nodes,edgesets){
  maxN = max(nodes)+1 #R is 1 indexed but we may have node 0
  present = vector(length = maxN)
  present[nodes+1] = TRUE #sets all nodes that have "survived" the intersets to true
  edgeRestrictions = vector(length = length(edgesets)) #vector that saves the strings
  edgeGreaterThan0 = vector(length = length(edgesets))
  edgesums = vector(length = length(edgesets))
  for( f in 1:length(edgesets)){
    seekedEdges = vector(length = length(edgesets[[f]][,1])) #true false vector if we want that edge
    numberOfEdges = 0 #number of edges that we want
    for (i in 1:length(edgesets[[f]][,1])){
      if(present[edgesets[[f]][i,1]+1]&&present[edgesets[[f]][i,2]+1]){
        seekedEdges[i] = TRUE
        numberOfEdges = numberOfEdges + 1
      }
    }
    #xc_ij < yi yj
    edgeRestrictions[f] = paste("x",f,"_",1:numberOfEdges,"-y_",
                                unlist(edgesets[[f]][seekedEdges,]),"<=0",sep = "",collapse = "\n")
    #xc_ij >=0
    edgeGreaterThan0[f] = paste("x",f,"_",1:numberOfEdges,">=0",sep = "",collapse = "\n")
    edgesums[f] = paste(paste("x",f,"_",1:numberOfEdges,sep = "",collapse = "+"),"-t>=0",sep = "")
  }
  #
  #nodes = nodes-1
  nodeGreaterThan0 = paste("y_",nodes,">=0",sep = "",collapse = "\n") #all the constraints for the nodes
  nodesum = paste(paste("y_",nodes,sep = "",collapse = "+"),"<=1")
  return(paste("Maximize t \nSubject to:\n",paste0(edgesums,"\n",edgeRestrictions,"\n",
                                               edgeGreaterThan0,collapse = "\n"),
            "\n",nodesum,"\n",nodeGreaterThan0,"\nend"))
}