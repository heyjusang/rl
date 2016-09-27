import numpy
from network.node import Node
from network.edge import Edge
from log import Log

NUMBER_OF_STATE = 12

#TODO: save input of selected genes
class State:
    # selectedGenes : List of Node
    # sampleIndex : int

    def __init__(self, initialGenes):
        self.selectedGenes = initialGenes
        self.sampleIndex = 0

    def setSampleIndex(self, sampleIndex):
        self.sampleIndex = sampleIndex

    def clear(self):
        self.selectedGenes = []

    def getSelectedGenes(self):
        return self.selectedGenes

    def handleActionAccept(self, candidateGene):
        if candidateGene not in self.selectedGenes:
            self.selectedGenes.append(candidateGene)

    def handleActionReject(self, candidateGene):
        if candidateGene in self.selectedGenes:
            self.selectedGenes.remove(candidateGene)

    #########################################################
    # 0: The number of selected genes                       #
    # 1: Average expr of selected genes                     #
    # 2: Std expr of selected genes                         #
    # 3: The number of 1st neighborhood of selected genes   #
    # 4: Average expr of 1st neighborhood of selected genes #
    # 5: Std expr of 1st neighborhood of selected genes     #
    #########################################################
    def asInput(self):
        result = []

        selectedSize = len(self.selectedGenes)
        result.append(selectedSize) # 0

        selectedStat = self.getNeighborhoodStat(self.selectedGenes)
        result.append(selectedStat[0]) # 1
        result.append(selectedStat[1]) # 2

        selectedNeighborhood = set()
        for g in self.selectedGenes:
            selectedNeighborhood.update(set(g.getNeighborhood()))

        selectedNeighborhoodSize = len(selectedNeighborhood)
        result.append(selectedNeighborhoodSize) # 3

        mean, std = self.getNeighborhoodStat(selectedNeighborhood)
        result.append(mean) # 4
        result.append(std) # 5

        return result

    def getNeighborhoodStat(self, neighborhood):
        mean = 0.0
        std = 0.0
        if len(neighborhood) > 0:
            exprs = [n.getValue(self.sampleIndex) for n in neighborhood]
            mean = numpy.mean(exprs)
            std = numpy.std(exprs)

        return mean, std
    
    def printOut(self):
        Log.i("Current state : " + str([n.getName() for n in self.selectedGenes]))
