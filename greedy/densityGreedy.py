from lib import binomial

# Calculate the average degree as density of a single graph.
def density(edges,nodes):
    return edges/float(nodes)

def quasiClique(edges,nodes):
        return edges-(0.334*binomial.coefficient(nodes, 2))

def Clique(edges,nodes):
    return edges/binomial.coefficient(nodes, 2)
