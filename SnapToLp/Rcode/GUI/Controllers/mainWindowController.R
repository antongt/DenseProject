#main window controller

graphStats <- shiny::reactive({
  
})

subgraphSet <- shiny::reactive({
  
  #call to c++/cplex
})

output$generalInfo <-({
  renderPrint("here there will be some general info such as number of nodes and edges etc")
})
output$summary <- ({
  shiny::renderPrint(summary(graphStats()))
})

problemDescription <- reactive({
  problem = txtToLp(nodes(),edgesets())
})