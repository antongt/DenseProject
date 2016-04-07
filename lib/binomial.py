# This function is for calculating the binomial coefficient without
# using the multiple precision library.

import math

def coefficient(n, k):
    return math.factorial(n) / (math.factorial(k)*math.factorial(n-k))

