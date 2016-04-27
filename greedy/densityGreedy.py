from lib import binomial

# Calculate the average degree as density of a single graph.
def density(edges,nodes):
    return edges/float(nodes)

def quasiClique(edges,nodes):
        return edges-(0.334*(nodes-1)*nodes*0.5)

def clique(edges,nodes):
    return edges/((nodes-1)*nodes*0.5)
            
