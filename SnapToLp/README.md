#translates from a SNAP graph file to CPLEX-lp


translates textfile of the format (see [SNAP Datasets](http://snap.stanford.edu/data/index.html)) :

    # FromCol    ToCol
      i1         j3
      i2         j3

to CPLEX-lp format (see [CPLEX lp format guide](http://lpsolve.sourceforge.net/5.0/CPLEX-format.htm)):

    maximize 
     x_ij + ... + x_nm
    subject to
     x_ij - y_i <= 0
     x_ij - y_j <= 0
     sum y_i <= 1
     x_ij >= 0
     y_i  >= 0
    end

using the library for python provided by SNAP (see [SNAP Documentation](http://snap.stanford.edu/snappy/index.html))

## usage:

The programs prints the lp-format to STDOUT, so when using the programs we recommend that you redirect it to some outputfile, example of usage is given below.

for translating one graph:

    python snapToLp.py <file> > outputfile.lp

for translating two graph:

    python snapToLp2.py <file1> <file2> > outputfile.lp

to solve the lp with CPLEX:

Start cplex with: 

    $ cplex

Run the commands:

    CPLEX> read outputfile.lp lp
    CPLEX> optimize

To display the value of the variables run:

    CPLEX> display solution variables -

## TODO:

* support for more than two file.
* implement greedy and bruteforce algorithm to compare results
