fluidPage(
  navbarPage("Finding dense subgraphs"
             ,id = "ui"
             ,type="tabs",
             #the UIs are created in the seperate file but they are all rendered at the same time to
             #bind the input/ui togeather to enable free moving between tabs
             tabPanel("Input", uiOutput("input"))
            )
)


