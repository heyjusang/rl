import numpy
import copy
from network.node import Node
from network.edge import Edge
from log import Log

NUMBER_OF_STATE = 13

class State:
    # features : List of float
    # candidateGenes : List of Node
    # sampleIndex : int

    def __init__(self, sampleIndex, environment):
        self.sampleIndex = sampleIndex
        self.initFeatures(environment)
        self.initCandidateGenes(environment)

    def getFeatures(self):
        return self.features

    def getCandidateGenes(self):
        return self.candidateGenes

    def initCandidateGenes(self, environment):
        neighbors = set(environment.getSelectedGenes()[-1].getNeighborhood())
        neighbors.difference_update(set(environment.getActingGenes()))

        Log.d("Length of Neighbors : " + str(len(neighbors)))
        self.candidateGenes = list(neighbors)

    #########################################################
    # 0: The number of selected genes                       #
    # 1: Average expr of selected genes                     #
    # 2: Std expr of selected genes                         #
    # 3: The number of 1st neighborhood of selected genes   #
    # 4: Average expr of 1st neighborhood of selected genes #
    # 5: Std expr of 1st neighborhood of selected genes     #
    #########################################################
    def initFeatures(self, environment):
        selectedGenes = environment.getSelectedGenes()
        self.features = []

        selectedSize = len(selectedGenes)
        self.features.append(selectedSize) # 0

        selectedStat = self.getNeighborhoodStat(selectedGenes)
        self.features.append(selectedStat[0]) # 1
        self.features.append(selectedStat[1]) # 2

        selectedNeighborhood = set()
        for g in selectedGenes:
            selectedNeighborhood.update(set(g.getNeighborhood()))

        selectedNeighborhoodSize = len(selectedNeighborhood)
        self.features.append(selectedNeighborhoodSize) # 3

        mean, std = self.getNeighborhoodStat(selectedNeighborhood)
        self.features.append(mean) # 4
        self.features.append(std) # 5

    def getNeighborhoodStat(self, neighborhood):
        mean = 0.0
        std = 0.0
        if len(neighborhood) > 0:
            exprs = [n.getValue(self.sampleIndex) for n in neighborhood]
            mean = numpy.mean(exprs)
            std = numpy.std(exprs)

        return mean, std
    
    def printOut(self): #TODO
        Log.i("Current state : " + str([n.getName() for n in self.selectedGenes]))
