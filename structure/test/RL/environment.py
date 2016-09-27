import numpy
from network.network import Network
from network.node import Node
from state import State
from action import ACTION_ACCEPT, ACTION_REJECT
from log import Log
from constants import INITIAL_GENE_SELECTION

INITIAL_GENE_SELECTION_BY_PAM50 = "InitialGeneSelection.pam50"
INITIAL_GENE_SELECTION_BY_RANDOM = "InitialGeneSelection.random"

class Environment:
    # network : Network
    # state : State
    # totalReward : float
    # sampleIndex : int
    # actingGenes : List of Node
    # prevStateInput : string

    def __init__(self, params):
        self.network = Network(params["node"], params["edge"])
        self.totalReward = 0.0
        self.sampleIndex = 0
        self.actionGenes = []
        self.initializeState()
        self.prevStateInput = None

    def clearActingGenes(self):
        self.actingGenes = []
        self.prevStateInput = None

    def saveActingGenes(self, gene, stateInput):
        self.actingGenes.append(gene)
        self.prevStateInput = stateInput

    def getPrevStateInput(self):
        return self.prevStateInput

    def initializeState(self):
        self.state = State(self.getInitialGenes())

    def setSampleIndex(self, sampleIndex):
        self.sampleIndex = sampleIndex
        self.state.setSampleIndex(sampleIndex)

    def clear(self):
        self.totalReward = 0.0
        self.state.clear()
        self.initializeState()

    def getNetwork(self):
        return self.network

    def getState(self):
        return self.state

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

    def getCandidateGenes(self):
        neighbors = set(self.state.getSelectedGenes()[-1].getNeighborhood())
        neighbors.difference_update(set(self.actingGenes))

        Log.d("Length of Neighbors : " + str(len(neighbors)))
        return list(neighbors)

    def getCurrentStateAsInput(self):
        return self.state.asInput()

    def handleAction(self, candidate, action):
        if action == ACTION_ACCEPT:
            self.state.handleActionAccept(candidate)
        elif action == ACTION_REJECT:
            self.state.handleActionReject(candidate)
        else:
            Log.e("improper action: " + action)

        return self.getReward()

    def getReward(self):
        reward = self.silhouette()
        temporalReward = reward - self.totalReward
        self.totalReward = reward

        return temporalReward
    
    def silhouette(self): #TODO
        selected = self.state.getSelectedGenes()

        outsider = set()
        for s in selected:
            outsider.update(set(s.getNeighborhood()))
        outsider.difference_update(set(selected))
        
        selectedValues = [abs(s.getValue(self.sampleIndex)) for s in selected]
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
        #Log.i("Total Reward : " + str(self.totalReward))
        self.state.printOut()
