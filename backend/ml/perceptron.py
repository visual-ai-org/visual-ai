import math

import numpy as np


# Perceptron Class
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def sigmoid(self, x):
        sig = np.vectorize(lambda y:  (1 - 1 / (1 + math.exp(y))) if y < 0 else  (1 / (1 + math.exp(-y))))
        return sig(x)

    def predict(self, inputs):
        # print(self.weights.shape)
        if inputs.ndim == 3:
            # convert 3d to 2d
            print(inputs.shape)
            inputs = inputs[-1]
        print("inputs", inputs, "weights", self.weights, "bias", self.bias)

        return self.sigmoid(np.dot(self.weights, inputs) + self.bias)

    def get_weights(self):
        return self.weights, self.bias

    def update(self, inputs, delta, learning_rate):
        # print("weights:", self.weights)
        # print("lr:", (learning_rate * delta * inputs))
        self.weights = self.weights + (learning_rate * delta * inputs)
        # print("weights new:", self.weights)

    # print("bias:", self.bias)
        # print("lr:", (learning_rate * delta).reshape(-1, 1).T)
        self.bias = self.bias @ (learning_rate * delta).reshape(-1, 1).T
        # print("new bias:", self.bias)
