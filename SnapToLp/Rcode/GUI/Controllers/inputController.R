rawData <- shiny::reactive({
  rawData = GraphInpput(input$filenames)
})
nodes <- shiny::reactive({
  rawData()[[1]]
})
edgesets <- shiny::reactive({
  rawData()[[2]]
})
solution <- shiny::reactive({
  #solution = parseSolution(input$solutionFile)
  #write a solution parser then we can do some nice data manipulation here
})
