from RL.backprop import RLBackpropTrainer
from RL.replay import Replay
from RL.actionValue import ActionValue
from RL.log import Log
import numpy

def main():
    temporalActionValue = ActionValue()
    targetActionValue = ActionValue()
    targetActionValue.copyParameters(temporalActionValue)
    backpropTrainer = RLBackpropTrainer(temporalActionValue, targetActionValue)

    records = []
    testsetFile = open("testset_clean", "r")
    for line in testsetFile.readlines():
        elements = line.replace("\n", "").split("\t")
        record = map(float, elements)
        records.append(record)
    testsetFile.close()
    
    replaySet = []
    success = 0
    failed = 0
    for i in xrange(len(records)):
        record = records[i] 
        label = int(record.pop())
        results = temporalActionValue.activate(record)
        action = max(results, key = results.get)
        predictedValue = results[action]

        temporalReward = 1 if action == label else -1

        if temporalReward == 1:
            success += 1
        else:
            failed += 1

        print (str(success) + "/" + str(failed))

        if i < len(records) - 1:
            nextRecord = records[i + 1][:-1]
            nextResults = targetActionValue.activate(nextRecord)
            nextAction = max(nextResults, key = nextResults.get)
            nextPredictedValue = nextResults[nextAction]

            errs = []
            for j in xrange(3):
                if j == label:
                    errs.append(1 - results[j + 1])
                else:
                    errs.append(-1 - results[j + 1])
            #print(str(label) + " : " + str(results))
            #print(str(temporalActionValue.getNetworkParams()))

            replay = Replay(record, errs, temporalReward, predictedValue, nextPredictedValue)
            error = backpropTrainer.train([replay])

            #if len(replaySet) >= 50:
            #    replaySet.pop(0)
            #replaySet.append(replay)
            #miniBatch = numpy.random.choice(replaySet, min(len(replaySet), 10), replace=False)
            #error = backpropTrainer.train(miniBatch)


            #Log.i("error : " + str(error))

        #if i % 100 == 0:
           #targetActionValue.copyParameters(temporalActionValue) 
           #Log.i("copy targetActionValue")


if __name__ == "__main__":
    main()
