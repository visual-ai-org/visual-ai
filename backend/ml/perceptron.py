import numpy as np


# Perceptron Class
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):
        # print(inputs, self.weights)
        # ensure dimensions are compatible
        if len(inputs) != len(self.weights):
            raise ValueError("Input size does not match weight size")

        return self.activate(np.dot(inputs.T, self.weights) + self.bias)

    def get_weights(self):
        return self.weights, self.bias