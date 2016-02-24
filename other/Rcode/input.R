graphInput <- function(locations, sep = "\t"){
  fileList = list(length(locations))
  for (i in 1:length(locations)){
    if (dir.exists(locations[i])){
      fileList[[i]] = list.files(locations[i],full.names = TRUE)
    }else{
      fileList[[i]] = locations[i]
    }
  }
  files = unlist(fileList)
  edgesets = list(length(files))
  for(i in 1:length(files)){
    edgesets[[i]]=read.table(files[i],sep,header = FALSE)
  }
  nodes = unlist(edgesets[[1]])
  if (length(edgesets)>1){
    for( i in 2:length(edgesets)){
      nodes = intersect(nodes,unlist(edgesets[[i]]))
    }
  }else{
    nodes = unique(nodes)
  }
  return(list(nodes,edgesets))
}