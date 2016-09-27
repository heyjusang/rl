import sys
import math


PSEUDO_COUNT = 0.000001

normal_file = open("../data/expr/average/normal.expr", 'r')
normal_file.readline()

normals = {}
for line in normal_file.readlines():
    elements = line.replace("\n", "").split("\t")
    gene = elements.pop(0)
    expr = float(elements.pop(0))
    normals[gene] = expr

normal_file.close()

expr_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w')
header = expr_file.readline()
output_file.write(header)

for line in expr_file.readlines():
    elements = line.replace("\n", "").split("\t")
    gene = elements.pop(0)
    exprs = [str(math.log((float(x) + PSEUDO_COUNT)/(normals[gene] + PSEUDO_COUNT), 2)) for x in elements]
    output_file.write(gene + "\t" + "\t".join(exprs) + "\n")

expr_file.close()
output_file.close()
