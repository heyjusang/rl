import numpy
from network.network import Network
from network.node import Node
from grid import Grid
from action import ACTION_ACCEPT, ACTION_REJECT
from log import Log
from constants import INITIAL_GENE_SELECTION

INITIAL_GENE_SELECTION_BY_PAM50 = "InitialGeneSelection.pam50"
INITIAL_GENE_SELECTION_BY_RANDOM = "InitialGeneSelection.random"

class Environment:
    # network : Network
    # selectedGenes : list of Node
    # actingGenes : list of Node
    # totalReward : float
    # sampleIndex : int
    # templeteGrid : grid of String
    # exprGrid : grid of float

    def __init__(self, params):
        self.network = Network(params["node"], params["edge"])
        self.templeteGrid = Grid.templeteGrid(params["templete"])
        self.totalReward = 0.0
        self.sampleIndex = 0
        self.clearActingGenes()

    def initSelectedGenes(self):
        self.selectedGenes = self.getInitialGenes()

    def clearActingGenes(self):
        self.actingGenes = []

    def saveActingGenes(self, gene):
        self.actingGenes.append(gene)

    def getPrevFeatures(self):
        return self.prevFeatures

    def setSampleIndex(self, sampleIndex):
        self.sampleIndex = sampleIndex
        self.exprGrid = Grid.exprGrid(self.templeteGrid, self.getNetwork().getNodes(), self.sampleIndex)

    def clear(self):
        self.totalReward = 0.0
        self.selectedGenes = []

    def getNetwork(self):
        return self.network

    def getSelectedGenes(self):
        return self.selectedGenes

    def getActingGenes(self):
        return self.actingGenes

    def getInitialGenes(self):
        if INITIAL_GENE_SELECTION == INITIAL_GENE_SELECTION_BY_PAM50:
            return self.pam50InitialGenes()
        elif INITIAL_GENE_SELECTION == INITIAL_GENE_SELECTION_BY_RANDOM:
            return self.randomlyPickInitialGenes(1)
        else:
            Log.e("improper initial gene selection method")

    def pam50InitialGenes(self):
        pam50File = open("/data/home/co9901/RL/data/pam50.txt", 'r')
        nodes = self.getNetwork().getNodes()
        genes = []
        for line in pam50File.readlines():
            gene = line.replace("\n", "")
            if gene in nodes:
                genes.append(nodes[gene])
        pam50File.close()

        Log.i(str(len(genes)) + " genes from pam50 genes were initialized.")
        return genes

    def randomlyPickInitialGenes(self, count): #TODO : multiple genes
        return [numpy.random.choice(self.getNetwork().getNodes().values())]

    def handleAction(self, candidate, action): #TODO
        if action == ACTION_ACCEPT:
            self.handleActionAccept(candidate)

        elif action == ACTION_REJECT:
            self.handleActionReject(candidate)
        else:
            Log.e("improper action: " + action)

        self.saveActingGenes(candidate)
        
        return self.getReward()
    
    def handleActionAccept(self, candidate):
        if candidate not in self.getSelectedGenes():
            self.getSelectedGenes().append(candidate)

    def handleActionReject(self, candidate):
        if candidate in self.getSelectedGenes():
            self.getSelectedGenes().remove(candidate)

    def getReward(self):
        reward = self.silhouette()
        temporalReward = reward - self.totalReward
        self.totalReward = reward

        return temporalReward
    
    def silhouette(self):
        outsider = set()
        for s in self.getSelectedGenes():
            outsider.update(set(s.getNeighborhood()))
        outsider.difference_update(set(self.getSelectedGenes()))
        
        selectedValues = [abs(s.getValue(self.sampleIndex)) for s in self.getSelectedGenes()]
        outsiderValues = [abs(s.getValue(self.sampleIndex)) for s in outsider]
        averages = []
        for v1 in selectedValues:
            dissimilarityIn = numpy.mean([abs(v1 - v2) for v2 in selectedValues]) #TODO: minus 1 ?
            dissimilarityOut = numpy.mean([abs(v1 - v2) for v2 in outsiderValues])
            s = (dissimilarityOut - dissimilarityIn) / max(dissimilarityIn, dissimilarityOut)
            averages.append(s)

        return numpy.mean(averages)

    def getSampleSize(self):
        return self.getNetwork().getSampleSize()

    def printOut(self):
        Log.i("Total Reward : " + str(self.totalReward))
