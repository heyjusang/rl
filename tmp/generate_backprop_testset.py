import numpy
import random

def perm():
    perm = numpy.random.choice([1, 2], p = [1.0, 0.0])
    if perm == 1:
        return "0"
    else:
        return str(random.random())

trueSet = ["1", "1", "1", "1"]
for i in xrange(121212):
    falseSet1 = [perm() for j in xrange(4)]
    falseSet2 = [perm() for j in xrange(4)]

    if i % 3 == 0:
        print("\t".join(trueSet + falseSet1 + falseSet2) + "\t1")
    elif i % 3 == 1:
        print("\t".join(falseSet1 + trueSet + falseSet2) + "\t2")
    else:
        print("\t".join(falseSet1 + falseSet2 + trueSet) + "\t3")
