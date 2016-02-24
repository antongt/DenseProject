for (f in list.files("Rcode",full.names = TRUE)){
  source(f)
}
files = commandArgs(TRUE)
l = graphInput(files)
cat(txtToLp(l[[1]],l[[2]]))