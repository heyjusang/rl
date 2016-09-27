import math

normal_file = open("../data/expr/trans/normal.expr.trans", 'r')

header = normal_file.readline()

samples = {}
for line in normal_file.readlines():
    elements = line.replace("\n", "").split("\t")
    sample = elements.pop(0)
    sample = sample.replace("-11", "")
    samples[sample] = elements

normal_file.close()

expr_file_names = ["basal", "her2", "luma", "lumb"]

normal_output = open("../data/expr/trans/cut_pair/normal.expr.trans", 'w')
normal_output.write(header)

for name in expr_file_names:
    expr_file = open("../data/expr/trans/" + name + ".expr.trans", 'r')
    output_file = open("../data/expr/trans/cut_pair/" + name + ".expr.trans", 'w')
    expr_file.readline()
    output_file.write(header)

    for line in expr_file.readlines():
        elements = line.replace("\n", "").split("\t")
        iid = elements.pop(0).split("-")
        iid.pop()
        sample = "-".join(iid)
        if sample in samples:
            output_file.write(sample + "\t" + "\t".join(elements) + "\n")
            normal_output.write(sample + "\t" + "\t".join(samples[sample]) + "\n")

    output_file.close()
    expr_file.close()

normal_output.close()
