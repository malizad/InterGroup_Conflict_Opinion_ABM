"""
Compute Number of Extremists
"""
def CompNoExtremists():
    extreme1 = 0
    extreme2 = 0
    for opinion1 in range(len(op1)):
        if abs(op1[opinion1]) >= 0.9:
            extreme1 += 1
    for opinion2 in range(len(op2)):
        if abs(op2[opinion2]) >= 0.9:
            extreme2 += 1
    NoExtremists = extreme1 + extreme2
    print 'Number of Extremists = ', NoExtremists
