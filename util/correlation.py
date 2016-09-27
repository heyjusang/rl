import sys
import math
import scipy.stats as stats
import numpy as np
MODE_PEARSON = "pearson"
MODE_SPEARMAN = "spearman"

mode = sys.argv[1]
exprs = {}

expr_file = open(sys.argv[2], "r")
expr_file.readline()
for line in expr_file.readlines():
    elements = line.replace("\n", "").split("\t")
    gene = elements.pop(0)
    expr = np.array(elements, dtype="float")
    exprs[gene] = expr
expr_file.close()

out_file = open(sys.argv[3], "w")
out_file.write("geneA\tgeneB\tcorr\n")

edge_file = open("../data/interaction/biogrid.edge", "r")
edge_file.readline()
for line in edge_file.readlines():
    elements = line.replace("\n", "").split("\t")
    geneA = elements[0]
    geneB = elements[1]
    if mode is MODE_PEARSON:
        corr = stats.pearsonr(exprs[geneA], exprs[geneB])[0]
    else:
        corr = stats.spearmanr(exprs[geneA], exprs[geneB])[0]
    
    if math.isnan(corr):
        corr = 0.0
    out_file.write(geneA + "\t" + geneB + "\t" + str(corr) + "\n")
out_file.close()
