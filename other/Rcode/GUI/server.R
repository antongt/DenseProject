function(input, output, session) {
    # Source the partials/<pageName>.R files

  for(file in list.files("UI",full.names = TRUE)){
    source(file,local = TRUE)
  }
  
  for (file in list.files("Controllers",full.names = TRUE)) {
    source(file, local = TRUE)
  }
}