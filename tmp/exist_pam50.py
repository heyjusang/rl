pam50File = open("../data/pam50.txt", "r")

pam50 = []
for line in pam50File.readlines():
    pam50.append(line.replace("\n", ""))

pam50File.close()
geneFile = open("../data/fold_change/couple/basal.expr", "r")
count = 0
for line in geneFile.readlines():
    gene = line.split("\t")[0]
    if gene in pam50:
        pam50.remove(gene)
        count += 1
print pam50
geneFile.close()
