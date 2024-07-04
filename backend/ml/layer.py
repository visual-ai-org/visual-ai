# Layer Class
import numpy as np

from .perceptron import Perceptron


class Layer:
    def __init__(self, number_of_nodes: int, input_size: int, function: str = "sigmoid"):
        self.perceptrons = [Perceptron(input_size, function) for _ in range(number_of_nodes)]

    @staticmethod
    def derivative(x, function):
        if function == "sigmoid":
            return x * (1 - x)
        elif function == "soft_plus":
            return Perceptron.sigmoid(x)
        elif function == "relu":
            return np.where(x > 0, 1, 0)

    def forward(self, x):
        return np.array([p.activate(x) for p in self.perceptrons])

