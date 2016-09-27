import numpy
from pybrain.auxiliary import GradientDescent
from replay import Replay
from action import *

class RLBackpropTrainer:
    # temporalNetwork : ActionValue
    # targetNetwork : ActionValue
    # descent : GradientDescent
    # weightDecay : float
    # discountFactor : float

    def __init__(self, temporalNetwork, targetNetwork, params):
        self.temporalNetwork = temporalNetwork
        self.targetNetwork = targetNetwork 
        
        self.weightDecay = float(params["weight_decay"])
        self.discountFactor = float(params["discount_factor"])

        self.initGradientDescent(params)

    def initGradientDescent(self, params):
        self.descent = GradientDescent()
        self.descent.alpha = float(params["learning_rate"])
        self.descent.momentum = float(params["momentum"])
        self.descent.alphadecay = float(params["alpha_decay"])
        self.descent.init(self.targetNetwork.getNetworkParams())

    def resetNetwork(self):
        self.targetNetwork.reset()
        self.temporalNetwork.reset()
        self.targetNetwork.resetDerivatives()
        self.temporalNetwork.resetDerivatives()

    def train(self, replaySet):
        assert len(replaySet) > 0, "Dataset cannot be empty."
        self.resetNetwork()
        errors = 0.0
        ponderation = 0.0

        for replay in replaySet:
            e = self.calcDerivs(replay)
            errors += e
            ponderation += 1.0

        self.temporalNetwork.setParameters(self.descent(self.targetNetwork.getDerivs()))

        return errors / ponderation

    def calcDerivs(self, replay):
        error = 0.0
        action = replay.getAction()
        # TODO
        #target = replay.getTemporalReward() + self.discountFactor * max(self.targetNetwork.activate(replay.getNextStateInput()).values()) #TODO : implement and case of termination
        target = replay.getTemporalReward() + self.discountFactor * replay.getNextPredictedValue()
        predicted  = replay.getPredictedValue()
        diff = target - predicted 
        
        outerr = []
        for a in actionList:
            if a == action:
                outerr.append(diff)
            else:
                outerr.append(0.0)

        error += 0.5 * sum([err ** 2 for err in outerr])
        #error += 0.5 * sum(outerr ** 2) #FIXME: check validation
        self.temporalNetwork.backActivate(numpy.array(outerr))

        return error
