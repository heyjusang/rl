import argparse
from RL.agent import Agent
from RL.environment import Environment
from RL.state import State
from RL.replay import Replay
from RL.util import Util
from RL.log import Log

# agent : Agent
# environment: Environment
# iterationCount : int

def argParse():
    parser = argparse.ArgumentParser()
    
    # iteration
    parser.add_argument('-es', '--e_step', help="total epoch", required=False, default=2)
    parser.add_argument('-ts', '--t_step', help="total iteration for one epoch", required=False, default=300)
    parser.add_argument('-cs', '--c_step', help="time to copy temporal to target action value", required=False, default=20)
    parser.add_argument('-pi', '--print_interval', help="interval for printing selection result", required=False, default=20)

    # replay memory
    parser.add_argument('-r', '--replay_size', help="size of replay memory", required=False, default=100)
    parser.add_argument('-b', '--batch_size', help="batch size for mini-batch gradient descent", required=False, default=10)

    # gradient descent
    parser.add_argument('-ad', '--alpha_decay', help="alpha decay for gradient descent", required=False, default=0.99)
    parser.add_argument('-l', '--learning_rate', help="learning rate for gradient descent", required=False, default=0.05)
    parser.add_argument('-m', '--momentum', help="momentum for gradient descent", required=False, default=0.0)
    parser.add_argument('-wd', '--weight_decay', help="weight decay for gradient descent", required=False, default=0.1)

    # learning
    parser.add_argument('-d', '--discount_factor', help="discount factor for reinforcement learning", required=False, default=0.5)
    parser.add_argument('-t', '--temperature', help="temperature parameter for soft-max function", required=False, default=1.0)

    # sample dependency
    parser.add_argument('-sd', '--sample_dependency', help="sample-dependent learning", required=False, default=False)

    parser.add_argument('-rt','--reward_threshold', help="reward threshold for termination", required=False, default=0.0)

    # file path
    parser.add_argument('-e', '--edge', help="edge file path", required=True)
    parser.add_argument('-o', '--out_dir', help="path of output directory", required=True)
    parser.add_argument('-n', '--node', help="node file path", required=True)
    parser.add_argument('-tp', '--templete', help="grid templete file path", required=True)

    return vars(parser.parse_args())

def series():
    global agent
    global environment

def epoch(params, sampleIndex, epochStep):
    global agent
    global environment

    environment.initSelectedGenes()

    rewardThreshold = float(params["reward_threshold"])
    cStep = int(params["c_step"])
    tStep = int(params["t_step"])
    printInterval = int(params["print_interval"])

    for t in range(1, tStep + 1):
        Log.i("===== Step " + str(t) + " =====")
        environment.printOut()

        if len(environment.getSelectedGenes()) == 0:
            Log.i("Selected gene list is empty")
            break

        currentState = State(sampleIndex, environment)

        if len(currentState.getCandidateGenes()) == 0:
            Log.i("Candidate gene list is empty")
            agent.updateTargetActionValue() #FIXME
            break

        gene, action, predictedValue = agent.actByGeneSelection(currentState)

        Log.i(Util.actionToString(action) + gene.getName())

        temporalReward = environment.handleAction(gene, action)

        Log.i("temporal reward : " + str(temporalReward))
        Log.i("predicted value : " + str(predictedValue))

        if len(environment.getSelectedGenes()) == 0: #TODO
            Log.i("Selected gene list is empty")
            break
        
        nextState = State(sampleIndex, environment)

        if currentState.getFeatures() == nextState.getFeatures():
            environment.saveActingGenes(gene)
        else:
            environment.clearActingGenes()

        replay = Replay(currentState, gene, action, temporalReward, nextState)
        agent.addReplay(replay)
        error = agent.update()
        Log.i("error : " + str(error))
        Util.log("error : " + str(error) + " temporal reward : " + str(temporalReward) + " predictedValue : " + str(predictedValue))

        if t % cStep == 0: #TODO
            agent.updateTargetActionValue()

        #if t % printInterval == 0: #TODO
        #    Util.result(environment, params, str(sampleIndex) + "_" + str(epochStep) + "_" + str(t), sampleIndex)

        #if temporalReward < rewardThreshold: #FIXME
        #    break

def dependentLearning(params):
    global agent
    global environment

    eStep = int(params["e_step"])

    agent = Agent(params)
    sampleSize = environment.getSampleSize()

    for s in range(0, sampleSize):
        Log.i("learning with Sample " + str(s))
        environment.setSampleIndex(s)
        agent.setSampleIndex(s)
        for e in range(0, eStep):
            Log.i("Start Epoch " + str(e))
            epoch(params, s, e)
            environment.clear()


def independentLearning(params):
    global agent
    global environment

    eStep = int(params["e_step"])

    sampleSize = environment.getSampleSize()

    for s in range(0, sampleSize):
        Log.i("learning with Sample" + str(s))
        environment.setSampleIndex(s)

        agent = Agent(params)
        agent.setSampleIndex(s)

        for e in range(0, eStep):
            Log.i("Start Epoch" + str(e))
            Util.log("Sample" + str(s) + " Epoch " + str(e))
            epoch(params, s, e)
            Util.result(environment, params, str(s) + "_" + str(e), s)
            environment.clear()

def main(params):
    global environment
    global iterationCount

    sampleDependency = bool(params["sample_dependency"])

    Log.i("initializing environment")
    environment = Environment(params)
    iterationCount = 0

    if sampleDependency:
        Log.i("start dependent learning")
        dependentLearning(params)
    else:
        Log.i("start independent learning")
        independentLearning(params)

    Util.result(environment, params)

if __name__ == "__main__":
    params = argParse()
    main(params)
