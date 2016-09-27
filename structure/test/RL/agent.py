import math
import numpy
import random
from pybrain.datasets import SupervisedDataSet
from action import *
from state import State
from state import NUMBER_OF_STATE
from actionValue import ActionValue
from replay import Replay
from backprop import RLBackpropTrainer
from constants import ACTION_SELECTION, GENE_SELECTION
from constants import EPSILON_GREEDY
from log import Log, LOG_TEST

SELECTION_BY_MAXIMUM = "selection.maximum"
SELECTION_BY_E_GREEDY = "selection.eGreedy"
SELECTION_BY_SOFT_MAX = "selection.softMax"

class Agent:
    # temporalActionValue : ActionValue
    # targetActionValue : ActionValue
    # backpropTrainer : RLBackpropTrainer
    # replayMemory : List of Replay
    # temperature : float
    # replaySize : int
    # batchSize : int
    # sampleIndex : int

    def __init__(self, params):
        self.temporalActionValue = ActionValue()
        self.targetActionValue = ActionValue()
        self.targetActionValue.copyParameters(self.temporalActionValue)
        self.backpropTrainer = RLBackpropTrainer(self.temporalActionValue, self.targetActionValue, params)
        self.replayMemory = []

        self.temperature = float(params["temperature"])
        self.batchSize = int(params["batch_size"])
        self.replaySize = int(params["replay_size"])

    def setSampleIndex(self, sampleIndex):
        self.sampleIndex = sampleIndex

    def clearReplayMemory(self):
        self.replayMemory = []

    def addReplay(self, replay):
        if len(self.replayMemory) >= self.replaySize:
            self.replayMemory.pop(0)
        self.replayMemory.append(replay)

    def predictTargetValue(self, stateInput, genes):
        maximumValue = -1000
        maximumAction = None 
        maximumGene = None
        for gene in genes:
            #Log.d("predicting Target of " + gene.getName())
            header = gene.getStateHeader(self.sampleIndex)
            results = self.targetActionValue.activate(header + stateInput)
            action = max(results, key = results.get)
            predicted = results[action]
            if predicted >= maximumValue:
                maximumValue = predicted
                maximumAction = action
                maximumGene = gene

        return maximumGene, maximumAction, maximumValue

    def actByGeneSelection(self, stateInput, genes):
        predictedValue = {}
        predictedAction = {}
        for gene in genes:
            #Log.d("predicting " + gene.getName())
            header = gene.getStateHeader(self.sampleIndex)
            action, value = self.act(header + stateInput)
            predictedValue[gene] = value
            predictedAction[gene] = action 

        if GENE_SELECTION == SELECTION_BY_MAXIMUM:
            gene = self.selectByMaximum(predictedValue)
        elif GENE_SELECTION == SELECTION_BY_E_GREEDY:
            gene = self.selectByEpsilonGreedy(predictedValue)
        elif GENE_SELECTION == SELECTION_BY_SOFT_MAX:
            gene = self.selectBySoftMax(predictedValue)
        else:
            Log.e("improper gene selection method")

        return gene, predictedAction[gene], predictedValue[gene]
    
    def act(self, stateInputWithHeader):
        results = self.temporalActionValue.activate(stateInputWithHeader)

        if ACTION_SELECTION == SELECTION_BY_MAXIMUM:
            action = self.selectByMaximum(results)
        elif ACTION_SELECTION == SELECTION_BY_E_GREEDY:
            action = self.selectByEpsilonGreedy(results)
        elif ACTION_SELECTION == SELECTION_BY_SOFT_MAX:
            action = self.selectBySoftMax(results)
        else:
            Log.e("improper action selection method")

        return action, results[action]

    def selectByMaximum(self, results): #results : Dict
        return max(results, key = results.get)

    def selectBySoftMax(self, results): #results : Dict
        prob = [math.exp(r / self.temperature) for r in results.values()]
        total = sum(prob)
        prob = [p/total for p in prob] 
        return numpy.random.choice(results.keys(), p=prob)

    def selectByEpsilonGreedy(self, results): #results: Dict
        prob = [EPSILON_GREEDY, 1 - EPSILON_GREEDY]

        if numpy.random.choice(["random", "greedy"], p=prob) == "greedy":
            return max(results, key = results.get)
        else:
            return numpy.random.choice(results.keys())

    def update(self):
        miniBatch = numpy.random.choice(self.replayMemory, min(self.batchSize, len(self.replayMemory)), replace=False)
        return self.backpropTrainer.train(miniBatch)

    def updateTargetActionValue(self):
        self.targetActionValue.copyParameters(self.temporalActionValue)

        if LOG_TEST:
            Log.t("Update Target Action Value")
            testData = [random.random() for i in xrange(NUMBER_OF_STATE)]
            if str(self.targetActionValue.activate(testData)) == str(self.temporalActionValue.activate(testData)):
                Log.s("Update Target Action Value")
            else:
                Log.e("Update Target Action Value")

    def printOut(self):
        return "===============Temporal ActionValue================="\
            + self.temporalActionValue.printOut()\
            + "===================================================="\
            + "=============== Target ActionValue ================="\
            + self.targetActionValue.printOut()\
            +  "===================================================="\
