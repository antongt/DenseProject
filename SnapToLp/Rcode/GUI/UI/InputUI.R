output$input<-{(renderUI(tabPanel("Input",
                         titlePanel("INPUT"),
                         sidebarLayout(
                           sidebarPanel(
                             fileInput(inputId = "fileNames"
                                       ,label = "Input files"
                                       ,multiple = TRUE
                                       ,accept = NULL),
                             fileInput(inputId = "solutionFile",
                                       label = "Input solution file from cplex",
                                       multiple = FALSE,
                                       accept = NULL)
                           ),
                           mainPanel(
                             uiOutput("graphMetrics")
                           )
                         )
                         )
))}