def save(cplex):
    variables = []
    values = []
    names = []
    fullVariables = []
    for i, name in enumerate(cplex.variables.get_names()):
        if (name[0] == "y"):
            values.append(cplex.solution.get_values(i))
            names.append(cplex.variables.get_names(i))
    maxv = max(values)
    for i in range(0, len(values)):
        if values[i] > (maxv / 1000.0):
            fullVariables.append(names[i][1:] + " " + str(values[i]))
            variables.append(names[i][1:])
    with open("lp.out", "w") as fo:
        for v in variables:
            fo.write(str(v) + '\n')
    with open("fullLp.out", "w") as fo:
        for v in fullVariables:
            fo.write(str(v) + '\n')
