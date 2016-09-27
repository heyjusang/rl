f = open("../data/interaction/biogrid.edge", "r")

print f.readline()

for line in f.readlines():
    elements = line.replace("\n", "").replace("\r", "").split("\t")
    elements.sort()
    if elements[0] == "UBC" or elements[1] == "UBC":
        continue
    print elements[0] + "\t" + elements[1]
f.close()
    
