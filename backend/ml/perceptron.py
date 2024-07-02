import numpy as np


# Perceptron Class
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):
        return self.activate(np.dot(inputs, self.weights) + self.bias)

    def get_weights(self):
        return self.weights, self.bias