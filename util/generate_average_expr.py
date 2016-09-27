import numpy

expr_file = open("../data/expr/normal.expr", 'r')

expr_file.readline()

output_file = open("../data/expr/average/normal.expr", 'w')
output_file.write("gene\texpr\n")
for line in expr_file.readlines():
    elements = line.replace("\n", "").split("\t")
    gene = elements.pop(0)
    exprs = map(float, elements)
    average = numpy.mean(exprs)
    output_file.write(gene + "\t" + str(average) + "\n")

expr_file.close()
output_file.close()
    
