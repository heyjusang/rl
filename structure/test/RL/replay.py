from state import State
from action import *

class Replay:
    # stateInput : List of float
    # action : string
    # nextStateInput : List of float
    # temporalReward : float
    # predictedValue : float
    # nextPredictedValue : float

    def __init__(self, stateInput, action, temporalReward, predictedValue, nextPredictedValue):
        self.stateInput = stateInput
        self.action = action
        self.temporalReward = temporalReward 
        self.predictedValue = predictedValue
        self.nextPredictedValue = nextPredictedValue
        #self.nextStateInput = nextStateInput

    def getStateInput(self):
        return self.stateInput
    
    def getAction(self):
        return self.action

    def getTemporalReward(self):
        return self.temporalReward

    def getPredictedValue(self):
        return self.predictedValue

    def getNextStateInput(self):
        return self.nextStateInput

    def getNextPredictedValue(self):
        return self.nextPredictedValue
