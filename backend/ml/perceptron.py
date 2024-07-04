import math

import numpy as np


# Perceptron Class
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):
        # print(self.weights.shape)
        print()
        print("weights", self.weights.shape)
        print("inputs", inputs.shape)

        print("np.dot", np.dot(self.weights, np.squeeze(inputs)).shape)
        print("bias", self.bias.shape)


        return self.activate(np.dot(self.weights, np.squeeze(inputs)) + self.bias)

    def get_weights(self):
        return self.weights, self.bias

    def update(self, inputs, delta, learning_rate):
        self.weights = self.weights @ (learning_rate * delta * inputs)
        self.bias = self.bias + (learning_rate * delta)
        print("Bias update:", self.bias.shape)