**oregons.lp** is the lp formulation of DCS on all 9 oregon-1 graphs from SNAP.

**oregonsol** and **oregonsol2** is the solution files given by cplex after solving oregons.lp.

Both runs where made on chalmers computer via ssh.

more specifically **oregonsol** was solved using the standard dual simplex algorithm and it took cplex 1h+ to find the solution.
**oregonsol2** was solved using the barrier method and cplex found the solution after 73s.

Observe that the result is the same as the results reported in Vinay paper assuming that they rounded up.

Another observation is that the barrier method is quicker.
