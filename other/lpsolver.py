import sys;
sys.path.append('/chalmers/sw/sup64/cplex-12.1/cplex121/python/x86-64_debian4.0_4.1/')
import cplex;
import fileinput;
import os;

file = open('lpfile.lp','w')
for line in fileinput.input():
  file.write(line)

file.close()

prob = cplex.Cplex()
prob.read("lpfile.lp",filetype="lp")
prob.parameters.lpmethod.set(prob.parameters.lpmethod.values.barrier)
prob.solve()

os.remove('lpfile.lp')
