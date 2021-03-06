import numpy as np
import pandas as pd

from aibrite.ml.neuralnet import NeuralNet
from aibrite.ml.neuralnetwithmomentum import NeuralNetWithMomentum
from aibrite.ml.neuralnetwithrmsprop import NeuralNetWithRMSprop
from aibrite.ml.neuralnetwithadam import NeuralNetWithAdam

df = pd.read_csv("./data/ex2data1.csv")

train_set, dev_set, test_set = NeuralNet.split(df.values, 0.8, 0.1, 0.1)

train_x, train_y = train_set[:, 0:-1], train_set[:, -1]
dev_x, dev_y = dev_set[:, 0:-1], dev_set[:, -1]
test_x, test_y = test_set[:, 0:-1], test_set[:, -1]

nn = NeuralNet(train_x, train_y, hidden_layers=(2, 2), iteration_count=6000)

train_result = nn.train(lambda nn, iter: print("{0:.2f}".format(
    iter.cost)) if iter.total_iteration_index % 100 == 0 else None)

result = nn.predict(test_x, expected=test_y)

print("{0}:\n{1}\n".format(
    nn, NeuralNet.format_score(result.score)))
