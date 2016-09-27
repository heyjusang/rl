import sys

contained = {}
edge_file = open("../data/interaction/biogrid_without_ubc.edge", "r")
edge_file.readline()
for line in edge_file.readlines():
    nodes = line.replace("\n", "").replace("\r", "").split("\t")
    contained[nodes[0]] = 1
    contained[nodes[1]] = 1
edge_file.close()

node_file = open(sys.argv[1], "r")
out_file = open(sys.argv[2], "w")

header = node_file.readline()
out_file.write(header)
for line in node_file.readlines():
    node = line.split("\t")[0]
    if node in contained:
        out_file.write(line)
out_file.close()
