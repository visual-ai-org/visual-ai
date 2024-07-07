import math

import numpy as np

class Perceptron:
    def __init__(self, row_size: int, col_size: int, function: str = "sigmoid"):
        self.weights = np.random.randn(row_size, col_size) * np.sqrt(2 / row_size + col_size)
        # print(self.weights)
        self.bias = np.random.uniform(0, 0)
        self.function = function

    @staticmethod
    def soft_plus(x):
        return np.log(1 + np.exp(x))

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def squash(x, function):
        if function == "sigmoid":
            return Perceptron.sigmoid(x)
        elif function == "soft_plus":
            return Perceptron.soft_plus(x)
        elif function == "relu":
            return Perceptron.relu(x)

    def activate(self, x):
        print(self.weights.shape,
              x.shape)
        z = np.dot(self.weights, x) + self.bias
        return Perceptron.squash(z, self.function)

    def update_weights(self, delta_w, delta_b):
        print("delta w", delta_w)
        print(self.weights)
        self.weights += delta_w
        self.bias += delta_b
