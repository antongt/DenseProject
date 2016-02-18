#translates from a SNAP graph file to CPLEX-lp

translates textfile of the format (see [SNAP Datasets](http://snap.stanford.edu/data/index.html)) :

    # FromCol    ToCol
      1          3
      2          3
      .          .
      .          .
      .          .

to CPLEX-lp format where the resulting lp is an lp formulation of DS or DCS (see [CPLEX lp format guide](http://www-01.ibm.com/support/knowledgecenter/SS9UKU_12.4.0/com.ibm.cplex.zos.help/FileFormats/topics/LP.html)):

    maximize 
     x_ij + ... + x_nm
    subject to
     x_ij - y_i <= 0
     x_ij - y_j <= 0
     .
     .
     .
     x_nm - y_n <= 0
     x_nm - y_m <= 0
     x_ij >= 0
     y_i  >= 0
    end

using the library for python provided by SNAP (see [SNAP Documentation](http://snap.stanford.edu/snappy/index.html))

## usage:

The programs prints the lp-format to STDOUT, so when using the programs we recommend that you redirect it to some outputfile, example of usage is given below.

for translating graphs:

    python snapToLp.py <file1> ... <fileN> > outputfile.lp

to solve the lp with CPLEX:

Start cplex with: 

    $ cplex

Run the commands:

    CPLEX> read outputfile.lp lp
    CPLEX> optimize

To display the value of the variables run:

    CPLEX> display solution variables -

To write the solution to a file run:

    CPLEX> write <file> sol

## TODO:

* implement greedy and bruteforce algorithm to compare results
* write a script which takes graphs files and give a solution directly, with the help of cplex libraries.
