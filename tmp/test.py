from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

net = buildNetwork(3, 2, 3)
dataset = SupervisedDataSet(3,3)

dataset.addSample([1,2,3],[1,2,3])
dataset.addSample([3,2,3],[2,2,2])
dataset.addSample([5,2,3],[1,3,1])
dataset.addSample([1,4,3],[1,4,3])
dataset.addSample([1,2,3],[1,2,5])

trainer = BackpropTrainer(net, dataset=dataset, batchlearning=True, verbose=True)
trainer.train()
