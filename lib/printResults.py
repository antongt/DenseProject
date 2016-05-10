def save(cplex):
    variables = []
    fullVariables = []
    maxv = max(cplex.solution.get_values())
    for i, name in enumerate(cplex.variables.get_names()):
        value = cplex.solution.get_values(i)
        if (name[0] == "y"):
            if value > (maxv / 100.0):
                fullVariables.append(name[1:] + " " + str(value))
                variables.append(name[1:])
    with open("lp.out", "w") as fo:
        for v in variables:
            fo.write(str(v) + '\n')
    with open("fullLp.out", "w") as fo:
        for v in fullVariables:
            fo.write(str(v) + '\n')
