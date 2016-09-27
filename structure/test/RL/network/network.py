from node import Node
from edge import Edge 

class Network:

    # nodes : Dict of geneName(string)/gene(Node)
    # sampleSize : int
    # edges : List of Edge

    def __init__(self, nodeFilePath, edgeFilePath):
        self.initNode(nodeFilePath) 
        self.initEdge(edgeFilePath)

    def initNode(self, nodeFilePath):
        self.nodes = {}
        nodeFile = open(nodeFilePath, 'r')

        sampleSize = len(nodeFile.readline().split("\t")) - 1
        self.sampleSize = max(0, sampleSize)

        for line in nodeFile.readlines():
            values = line.replace("\n", "").split("\t")
            gene = values.pop(0)
            node = Node(gene, map(float, values))

            self.nodes[gene] = node

        nodeFile.close() 

    def initEdge(self, edgeFilePath):
        self.edges = []
        edgeFile = open(edgeFilePath, 'r')
        edgeFile.readline()
        for line in edgeFile.readlines():
            elements = line.replace("\n", "").split("\t")
            geneAName = elements[0]
            geneBName = elements[1]

            if geneAName in self.getNodes() and geneBName in self.getNodes():
                nodeA = self.getNodes()[geneAName]
                nodeB = self.getNodes()[geneBName]
                edge = Edge(nodeA, nodeB)
                nodeA.addEdge(edge)
                nodeB.addEdge(edge)
                self.edges.append(edge)

        edgeFile.close()

    def getNodes(self):
        return self.nodes

    def getSampleSize(self):
        return self.sampleSize
