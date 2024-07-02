# Layer Class
import numpy as np

from .perceptron import Perceptron


class Layer:
    def __init__(self, num_perceptrons, input_size):
        self.perceptrons = [Perceptron(input_size) for _ in range(num_perceptrons)]

    def forward(self, inputs):
        return np.array([perceptron.predict(inputs) for perceptron in self.perceptrons])

    def get_weights(self):
        return [perceptron.get_weights() for perceptron in self.perceptrons]