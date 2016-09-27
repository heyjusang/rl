class Edge:

    # geneA : Node
    # geneB : node
    # corr : float
    # accepted : boolean

    def __init__(self, geneA, geneB):
        self.geneA = geneA
        self.geneB = geneB
        self.corr = 0.0
        self.accepted = False

    def setCorrelation(self, corr):
        self.corr = corr

    def getGeneA(self):
        return self.geneA

    def getGeneB(self):
        return self.geneB

    def accept(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

