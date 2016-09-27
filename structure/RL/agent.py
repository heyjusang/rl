import math
import numpy
import random
from pybrain.datasets import SupervisedDataSet
from action import *
from state import State
from state import NUMBER_OF_STATE
from actionValue import ActionValue
from replay import Replay
from pybrain.supervised.trainers import BackpropTrainer
from constants import ACTION_SELECTION, GENE_SELECTION
from constants import EPSILON_GREEDY
from log import Log, LOG_TEST

SELECTION_BY_MAXIMUM = "selection.maximum"
SELECTION_BY_E_GREEDY = "selection.eGreedy"
SELECTION_BY_SOFT_MAX = "selection.softMax"

class Agent:
    # temporalActionValue : ActionValue
    # targetActionValue : ActionValue
    # replayMemory : List of Replay
    # temperature : float
    # replaySize : int
    # batchSize : int
    # sampleIndex : int
    # discountFactor : float

    ##### BackpropTrainer #####
    # learningRate : float    #
    # alphaDecay : float      #
    # momentum : float        #
    # weightDecay : float     #
    ###########################

    def __init__(self, params):
        self.temporalActionValue = ActionValue()
        self.targetActionValue = ActionValue()
        self.targetActionValue.copyParameters(self.temporalActionValue)
        self.replayMemory = []

        self.temperature = float(params["temperature"])
        self.batchSize = int(params["batch_size"])
        self.replaySize = int(params["replay_size"])
        self.discountFactor = float(params["discount_factor"])

        self.learningRate = float(params["learning_rate"])
        self.alphaDecay = float(params["alpha_decay"])
        self.momentum = float(params["momentum"])
        self.weightDecay = float(params["weight_decay"])

    def setSampleIndex(self, sampleIndex):
        self.sampleIndex = sampleIndex

    def clearReplayMemory(self):
        self.replayMemory = []

    def addReplay(self, replay):
        if len(self.replayMemory) >= self.replaySize:
            self.replayMemory.pop(0)
        self.replayMemory.append(replay)

    def actByGeneSelection(self, state):
        predictedValue = {}
        predictedAction = {}
        features = state.getFeatures()
        genes = state.getCandidateGenes()
        for gene in genes:
            #Log.d("predicting " + gene.getName())
            header = gene.getStateHeader(self.sampleIndex)
            action, value = self.act(header + features)
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
    
    def act(self, featuresWithHeader):
        results = self.temporalActionValue.activate(featuresWithHeader)

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
        miniBatch = self.getMiniBatch()        

        backpropTrainer = BackpropTrainer(self.temporalActionValue.getNetwork(), dataset=miniBatch, learningrate=self.learningRate, lrdecay=self.alphaDecay, momentum=self.momentum, weightdecay=self.weightDecay, batchlearning=True)

        return backpropTrainer.train()

    def getMiniBatch(self):
        miniBatch = numpy.random.choice(self.replayMemory, min(self.batchSize, len(self.replayMemory)), replace=False)
        Log.d("sampling " + str(len(miniBatch)) + " minibatch")

        dataset = SupervisedDataSet(NUMBER_OF_STATE, NUMBER_OF_ACTION)

        for replay in miniBatch:
            stateInput, target = self.convertReplay2Sample(replay)
            dataset.addSample(stateInput, target)

        return dataset

    def convertReplay2Sample(self, replay): # backpropagation for only predicted target
        header = replay.getGene().getStateHeader(self.sampleIndex)
        
        stateInput = header + replay.getState().getFeatures()
        predicted = self.temporalActionValue.activate(stateInput)

        maximumTargetValue = self.predictTargetValue(replay.getNextState())
        targeted = replay.getTemporalReward() + self.discountFactor * maximumTargetValue

        target = []
        for action in actionList:
            if action == replay.getAction():
                target.append(targeted)
            else:
                target.append(predicted[action])

        return stateInput, target

    def predictTargetValue(self, state):
        maximumValue = -100000

        genes = state.getCandidateGenes()
        for gene in genes:
            header = gene.getStateHeader(self.sampleIndex)
            results = self.targetActionValue.activate(header + state.getFeatures())
            predicted = max(results.values())
            if predicted >= maximumValue:
                maximumValue = predicted

        return maximumValue

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
