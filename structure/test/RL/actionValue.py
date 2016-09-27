import numpy
from action import *
from state import State, NUMBER_OF_STATE
from constants import NUMBER_OF_UNIT_FIRST, NUMBER_OF_UNIT_SECOND
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from log import Log

class ActionValue:
    # actionValueNetwork : FeedForwardNetwork

    def __init__(self):
        self.initActionValueNetwork()

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
        inLayer = LinearLayer(NUMBER_OF_STATE) 
        firstHiddenLayer = LinearLayer(NUMBER_OF_UNIT_FIRST)
        secondHiddenLayer = LinearLayer(NUMBER_OF_UNIT_SECOND)
        outLayer = LinearLayer(NUMBER_OF_ACTION)

        self.actionValueNetwork = FeedForwardNetwork()
        self.actionValueNetwork.addInputModule(inLayer)
        self.actionValueNetwork.addModule(firstHiddenLayer)
        self.actionValueNetwork.addModule(secondHiddenLayer)
        self.actionValueNetwork.addOutputModule(outLayer)

        in2FirstHidden = FullConnection(inLayer, firstHiddenLayer)
        firstHidden2SecondHidden = FullConnection(firstHiddenLayer, secondHiddenLayer)
        secondHidden2Out = FullConnection(secondHiddenLayer, outLayer)

        self.actionValueNetwork.addConnection(in2FirstHidden)
        self.actionValueNetwork.addConnection(firstHidden2SecondHidden)
        self.actionValueNetwork.addConnection(secondHidden2Out)

        self.actionValueNetwork.sortModules()

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

