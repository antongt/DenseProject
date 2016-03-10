from lib import snap;
import sys;
import datetime;
from os import walk;
from os import path;
from os import makedirs;

asUnDir = False
oneGraph = False

if(len(sys.argv) < 2):
  sys.exit("usage: python snap2lp.py <file1> ... <fileN>")

if(len(sys.argv) == 2):
  if sys.argv[1] == "-d":
    sys.exit("no input.")
  oneGraph = True

if(len(sys.argv) == 3 and sys.argv[1] == "-d"):
  asUnDir = True
  oneGraph = True

if(len(sys.argv) > 3 and sys.argv[1] == "-d"):
  asUnDir = True


# Preprocess the graphs by removing all nodes that do not appear in all the
# graphs (keeping only the intersection of the nodes).
def preprocessGraphs(Graphs):
  v = []

  # appends node set for all graphs to v.
  for g in range(0,len(Graphs)):
    a = []
    for n in Graphs[g].Nodes():
      a.append(n.GetId())
    v.append(set(a))

  # take the intersection, giving us all common nodes.
  u = list(set.intersection(*v))
  print >> sys.stderr, "nodes: " + str(len(u))

  # converts to a snap-vector
  w = snap.TIntV()
  for i in u:
    w.Add(i)

  # update graph list with subgraph induced by common nodes.
  for g in range(0,len(Graphs)):
    Graphs[g] = snap.GetSubGraph(Graphs[g],w)

  ng = 0
  print >> sys.stderr, "edges:"
  for g in range(0,len(Graphs)):
    ng = ng + Graphs[g].GetEdges()
    print >> sys.stderr, "  " + str(Graphs[g].GetEdges())
  print >> sys.stderr, "total edges: " + str(ng)



# Create a new directory. The default name is followed by a number, starting with 1.
# If the default one exists, increment the number until a directory does not exist.
def createNewDir():
  defaultName = 'preprocessed_'
  number = 1
  dirPath = ""
  while True:
    # Note: the function zfill pads with leading zeroes.
    dirPath = path.join("data", defaultName + str(number).zfill(2))
    number += 1
    if not path.exists(dirPath):
      break
  try:
    makedirs(dirPath)
    print("Created the directory " + dirPath)
    print("Please rename it something descriptive.")
  except:
    print >> sys.stderr, "Could not create a new directory"
  return dirPath



# Save each graph as a file in the directory specified by dirPath.
# Include a timestamp in the file name, that way you can identify files that
# were preprocessed together by comparing their timestamps, if needed.
def saveGraphs(Graphs, dirPath):
  timestamp = datetime.datetime.now()
  comment = "Preprocessed on " + timestamp.isoformat()
  for i in range(0, len(Graphs)):
    fileName = path.join(dirPath, str(i).zfill(2) + ".txt")
    snap.SaveEdgeList(Graphs[i], fileName, comment)



if(oneGraph):
  print("Preprocessing only makes sense for multiple graphs")
  sys.exit(2) # 2 is sometimes used for command line syntax error.

Graphs = []
if(asUnDir):
  for file in sys.argv[2:]:
    g = snap.LoadEdgeList(snap.PNGraph, file, 0, 1)
    snap.MakeUnDir(g)
    Graphs.append(g)
else:
  for file in sys.argv[1:]:
    Graphs.append(snap.LoadEdgeList(snap.PUNGraph, file, 0, 1))

preprocessGraphs(Graphs)
dirPath = createNewDir()
saveGraphs(Graphs, dirPath)


# vim: set expandtab tabstop=2 shiftwidth=2:
