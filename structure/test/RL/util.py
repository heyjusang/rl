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
    def result(environment, params, index=-1):
        outputPath = params["out_dir"]
        index = "_" + str(index) if index >= 0 else ""
        nodeFile = open(outputPath + "node" + index + ".txt", 'w')

        nodes = environment.getNetwork().getNodes()
        selected = environment.getState().getSelectedGenes()

        nodeFile.write("gene\tvalue\tselected\n")
        for node in nodes.values(): #TODO : sampleIndex
            nodeFile.write(node.getName() + "\t" + str(node.getValue()) + "\t" + ("1" if node in selected else "0") + "\n")

        nodeFile.close()

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
