from edge import Edge
import numpy

class Node:

    # name : string
    # values : List of float
    # edges : Dict of gene(Node)/edge(Edge)
    # states : Dict of index / State input header (List)

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.edges = {}
        self.states = {}

    def addEdge(self, edge):
        if self.name == edge.getGeneA().getName():
            self.edges[edge.getGeneB()] = edge
        elif self.name == edge.getGeneB().getName():
            self.edges[edge.getGeneA()] = edge

    def getName(self):
        return self.name

    def getValue(self, index=0):
        return self.values[index]

    def getEdges(self):
        return self.edges

    def getNeighborhood(self):
        return self.edges.keys()

    def getStateHeader(self, index):
        if index not in self.states:
            self.states[index] = self.createStateHeader(index)
        return self.states[index]

    #########################################################
    # 0: Expr of candidate gene                             #
    # 1: The number of 1st neighborhood of candidate gene   #
    # 2: Average expr of 1st neighborhood of candidate gene #
    # 3: Std expr of 1st neighborhood of candidate gene     #
    # 4: The number of 2nd neighborhood of candidate gene   #
    # 5: Average expr of 2nd neighborhood of candidate gene #
    # 6: Std expr of 2nd neighborhood of candidate gene     #
    #########################################################
    def createStateHeader(self, index):
        header = []

        value = self.getValue(index)
        header.append(value) # 0

        neighborhood = self.getNeighborhood()
        neighborhoodSize = len(neighborhood)
        header.append(neighborhoodSize) # 1

        mean, std = self.getNeighborhoodStat(neighborhood, index)
        header.append(mean) # 2
        header.append(std) # 3

        secondNeighborhood = set()
        for n in neighborhood:
            secondNeighborhood.update(set(n.getNeighborhood()))
        secondNeighborhood.difference_update(set(neighborhood))

        secondSize = len(secondNeighborhood)
        header.append(secondSize) # 4

        secondStat = self.getNeighborhoodStat(secondNeighborhood, index)
        header.append(secondStat[0]) # 5
        header.append(secondStat[1]) # 6

        return header

    def getNeighborhoodStat(self, neighborhood, index):
        mean = 0.0
        std = 0.0
        if len(neighborhood) > 0:
            exprs = [n.getValue(index) for n in neighborhood]
            mean = numpy.mean(exprs)
            std = numpy.std(exprs)

        return mean, std
