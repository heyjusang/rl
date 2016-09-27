nodes = {}
node_file = open("../data/expr/all.expr", "r")
node_file.readline()
for line in node_file.readlines():
    g = line.split("\t").pop(0)
    nodes[g] = 0
node_file.close()


edge_file = open("../data/BIOGRID-ORGANISM-Homo_sapiens-3.2.102.tab.txt", "r")
edge_file.readline()
print("nodeA\tnodeB")
for line in edge_file.readlines():
    elements = line.replace("\n", "").split("\t")
    g1 = elements[2]
    g2 = elements[3]
    g1_aliases = elements[4]
    g2_aliases = elements[5]

    g1_list = [g1]
    g2_list = [g2]

    if g1_aliases is not "N/A":
        g1_list += g1_aliases.split("|")
    if g2_aliases is not "N/A":
        g2_list += g2_aliases.split("|")

    for g1 in g1_list:
        if g1 in nodes:
            for g2 in g2_list:
                if g2 in nodes:
                    print(g1 + "\t" + g2)
                    #break
            #break

edge_file.close()

