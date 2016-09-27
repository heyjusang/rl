import numpy
from action import *
from state import State, NUMBER_OF_STATE
from constants import NUMBER_OF_HIDDEN_LAYER, NUMBER_OF_HIDDEN_UNIT
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import BiasUnit, LinearLayer, ReluLayer, TanhLayer
from pybrain.structure import FullConnection

class ActionValue:
    # actionValueNetwork : FeedForwardNetwork

    def __init__(self):
        self.initActionValueNetwork()

    def getNetwork(self):
        return self.actionValueNetwork

    def getNetworkParams(self):
        return self.actionValueNetwork.params

    def setParameters(self, params):
        self.actionValueNetwork._setParameters(params)

    def copyParameters(self, network):
        self.actionValueNetwork._setParameters(numpy.copy(network.getNetworkParams()))
        if self.actionValueNetwork.hasDerivatives:
            self.resetDerivatives()

    def getDerivs(self):
        return self.actionValueNetwork.derivs

    def initActionValueNetwork(self):
        layers = []
        n = FeedForwardNetwork()

        layers.append(LinearLayer(NUMBER_OF_STATE)) # input layer
        n.addInputModule(layers[0])

        for i in range(0, NUMBER_OF_HIDDEN_LAYER):
            layers.append(ReluLayer(NUMBER_OF_HIDDEN_UNIT)) # hidden layer
            n.addModule(layers[i + 1])
        
        layers.append(TanhLayer(NUMBER_OF_ACTION)) # output layer
        n.addOutputModule(layers[-1])

        bias = BiasUnit()
        n.addModule(bias)
        
        for i in range(0, len(layers) - 1):
            n.addConnection(FullConnection(layers[i], layers[i + 1]))
            n.addConnection(FullConnection(bias, layers[i + 1])) # connect bias to hidden and output layer

        n.sortModules()

        self.actionValueNetwork = n

    def activate(self, stateInput):
        approximated = self.actionValueNetwork.activate(stateInput)
        results = {}
        for index, action in enumerate(actionList):
            results[action] = approximated[index]

        return results

    def backActivate(self, outerr):
        self.actionValueNetwork.backActivate(outerr)

    def reset(self):
        self.actionValueNetwork.reset()

    def resetDerivatives(self):
        self.actionValueNetwork.resetDerivatives()

    def printOut(self):
        return self.printWeights()

    def printWeights(self):
        string = "<Network Weight>\n"
        for module in self.actionValueNetwork.modules:
            for conn in self.actionValueNetwork.connections[module]:
                string += str(conn) + "\n"
                for i in range(len(conn.params)):
                     string += str(conn.whichBuffers(i)) + " " + str(conn.params[i]) + "\n"
        string += "</Network Weight>"
        return string

