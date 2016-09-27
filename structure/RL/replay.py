from state import State
from action import *

class Replay:
    # state: State
    # action : string
    # gene : Node
    # temporalReward : float
    # nextState : State

    def __init__(self, state, gene, action, temporalReward, nextState):
        self.state = state
        self.gene = gene
        self.action = action
        self.temporalReward = temporalReward 
        self.nextState = nextState

    def getState(self):
        return self.state

    def getGene(self):
        return self.gene
    
    def getAction(self):
        return self.action

    def getTemporalReward(self):
        return self.temporalReward

    def getNextState(self):
        return self.nextState
