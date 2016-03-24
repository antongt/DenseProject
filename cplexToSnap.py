import sys
import os

def usage(): 
  sys.exit("usage: python cplexToSnap.py <cplex.log> <resultGraph.txt>")
if(len(sys.argv) != 3):
  usage()

cName,cExt  = os.path.splitext(sys.argv[1])
sName,sExt  = os.path.splitext(sys.argv[2])
if cExt != ".log":
  usage()
if sExt != ".txt":
  usage()

input = open(sys.argv[1])
output = open(sys.argv[2],"w+")

output.write("# Undirected Dense Subgraph: ")
output.write(sys.argv[2]+"\n")
output.write("# Extracted from the cplex logfile : "+cName+".log\n")
output.write("# Nodes: TODO")
output.write(" Edges: TODO\n")
output.write("# FromNodeId    ToNodeId\n")
line = "y"
while line[0] != 'x':
  line = input.readline()
# Read the rest of the data 
for line in input:
  if line[0] == 'x':
    fr_to = line.split('_',1)[1].split('#',1)
    fr_to[1] = fr_to[1].split(' ',1)[0]
    output.write(fr_to[0]+"	"+fr_to[1]+'\n')

input.close()
output.close()
print("cplexToSnap Completed.")
