#######################################################
# set genes into grid layout, considering interaction #
#######################################################
import sys
import networkx as nx

x = int(sys.argv[3])

g = nx.Graph()

edge_file = open(sys.argv[1], "r")
edge_file.readline()
for line in edge_file.readlines():
    elements = line.replace("\n", "").split("\t")
    g.add_edge(elements[0], elements[1])

edge_file.close()

#pos = nx.spring_layout(g)
pos = nx.spring_layout(g, iterations=20)

def getX(item):
    return pos[item][0] 

def getY(item):
    return pos[item][1]

def chunk(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

sort_by_y = list(chunk(sorted(pos, key=getY), x))

results = []
for chunk in sort_by_y:
    results.append(sorted(chunk, key=getX)) 

out_file = open(sys.argv[2], "w")

for chunk in results:
    out_file.write("\t".join(chunk) + "\n")

out_file.close()
