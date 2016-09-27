from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
import numpy

def main():
    ds = SupervisedDataSet(12, 3)
    records = []

    testsetFile = open("testset_short", "r")
    for line in testsetFile.readlines():
        elements = line.replace("\n", "").split("\t")
        record = map(float, elements)
        records.append(record)
        i = record[12]
        label = []
        if i == 1:
            label = [10, 3, 2]
        elif i == 2:
            label = [1, -5, 3]
        elif i == 3:
            label = [0, 4, 8]
        
        ds.addSample(record[:12], label)
    testsetFile.close()

    net = buildNetwork(12, 6, 3)
    trainer = BackpropTrainer(net, ds)

    trainer.train()
    
    success = 0
    fail = 0
    for i in xrange(len(records)):
        record = records[i]
        label = record.pop()
        results = net.activate(record)

    print(str(success) + "/" + str(fail))

if __name__ == "__main__":
    main()
