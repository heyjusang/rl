#####################################################
# To reduce the size of network,                    #
# the nodes reachable from pam50 genes are selected #
#####################################################

def select(genes, edges, results):
    neighbors = set()
    for gene in genes:
        neighbors = neighbors | set(edges[gene])
    neighbors = neighbors - set(results)
    results += list(neighbors)

    if len(neighbors) > 0:
        select(list(neighbors), edges, results)

def main():
    results = []

    pam50 = []
    pam50_file = open("../data/pam50.txt", "r")
    for line in pam50_file.readlines():
        node = line.replace("\n", "").replace("\r", "")
        pam50.append(node)
        results.append(node)
    pam50_file.close()

    edges = {}
    edge_file = open("../data/interaction/biogrid_without_ubc.edge", "r")
    edge_file.readline()
    for line in edge_file.readlines():
        nodes = line.replace("\n", "").replace("\r", "").split("\t")
        if nodes[0] not in edges:
            edges[nodes[0]] = []
        edges[nodes[0]].append(nodes[1])
    
        if nodes[1] not in edges:
            edges[nodes[1]] = []
        edges[nodes[1]].append(nodes[0])

    select(pam50, edges, results)
    print(str(len(edges)))
    print(str(len(results)))

    out_file = open("../data/interaction/biogrid_prune_pam50.edge", "w")
    out_file.write(edge_file.readline())

    edge_file.seek(0)    
    for line in edge_file.readlines():
        nodes = line.replace("\n", "").replace("\r", "").split("\t")
        if nodes[0] in results and nodes[1] in results:
            out_file.write(line)

    out_file.close()
    edge_file.close()


main()
