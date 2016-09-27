f = open("biogrid.edge", "r")

genes = {}
for line in f.readlines():
    elements = line.replace("\n" ,"").replace("\r", "").split("\t")
    gene1 = elements[0]
    gene2 = elements[1]

    if gene1 not in genes:
        genes[gene1] = 0
    genes[gene1] += 1
    if gene2 not in genes:
        genes[gene2] = 0
    genes[gene2] += 1

f.close()

for gene in sorted(genes, key=genes.get, reverse=True):
    print gene, genes[gene]
