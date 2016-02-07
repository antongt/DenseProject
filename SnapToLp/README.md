#translates from a SNAP graph file to CPLEX-lp

translates textfile of the format(given by SNAP):

    # FromCol    ToCol
      i1         j3
      i2         j3

to(CPLEX-lp format):

    maximize 
     x_ij + ... + x_nm
    subject to
     x_ij - y_i <= 0
     x_ij - y_j <= 0
     sum y_i <= 1
     x_ij >= 0
     y_i  >= 0
    end

## usage:

The programs prints the lp-format to STDOUT, so when using the programs we recommend that you redirect it to some outputfile, example of usage is given below.

for translating one graph:

    python snapToLp.py > outputfile.lp

for translating two graph:

    python snapToLp2.py <file1> <file2> > outputfile.lp

to solve the lp with CPLEX:

* start cplex with 
    $ cplex
* run the commands:
    CPLEX> read outputfile.lp lp
    CPLEX> optimize
* to display the value of the variables run:
    CPLEX> display solution variables -

## TODO:

* support for more than two file.
