from action import ACTION_ACCEPT
from action import ACTION_REJECT

class Util:

    @staticmethod
    def showAgentStatus(agent, index):
        string = agent.printOut()
        return string

    @staticmethod
    def actionToString(action):
        if action == ACTION_ACCEPT:
            return "action : ACCEPT "
        elif action == ACTION_REJECT:
            return "action: REJECT "
        else:
            return "action error"

    @staticmethod
    def result(environment, params, tag, sampleIndex=0):
        outputPath = params["out_dir"]
        nodeFile = open(outputPath + "node_" + tag + ".txt", 'w')

        nodes = environment.getNetwork().getNodes()
        selected = environment.getSelectedGenes()

        nodeFile.write("gene\tvalue\t_selected\n")
        for node in nodes.values():
            nodeFile.write(node.getName() + "\t" + str(node.getValue(sampleIndex)) + "\t" + ("1" if node in selected else "0") + "\n")

        nodeFile.close()

    @staticmethod
    def log(msg):
        import datetime

        logFile = open("log/log", 'a') #TODO: filename
        logFile.write("[" + str(datetime.datetime.now()) + "] " + msg + "\n")
        logFile.close()

    @staticmethod
    def save(agent, environment, params):
        #TODO
        import json

        outputPath = params["out_dir"]

        paramsJSON = json.dumps(params)
        paramsFile = open(outputPath + "params.txt", 'w')
        paramsFile.write(paramsJSON)
        paramsFile.close()

    @staticmethod
    def load():
        #TODO
        import json
